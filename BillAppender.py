from xml.dom import minidom
from bs4 import BeautifulSoup
import json
import requests

def appendJson():
    with open('sponsordata.json', 'r') as f:
        data = json.load(f)
    data.pop(0)
    for item in data:
        bill = item['bill']
        xml = get_details(bill)
        item['title'], item['sponsor'], item['introdate'] = getTitle(xml)
        f = json.dump(data)



def get_details(bill):
    url = 'http://azles.gov/xml/legservice.asmx?op=BillInfo'

    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Header>
    <SOAPLegServiceHeader xmlns="http://azleg.gov/webservices/">
    <UserName>{0}</UserName>
    <Password>{1}</Password>
    </SOAPLegServiceHeader>
    </soap:Header>
    <soap:Body>
    <BillInfo xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    <BillNum>{3}</BillNum>
    </BillInfo>
    </soap:Body>
    </soap:Envelope>""".format('AZCIR',
                               'CIR35yq881cbPJ',
                                115,
                                bill)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/BillInfo"}
            
    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def getTitle(x):
    xml_data = minidom.parseString(x)
    title = xml_data.getElementsByTagName('Short_Title')[0].firstChild.wholeText
    sponsor = xml_data.getElementsByTagName('SPONSOR')[0].attributes['Member_Name'].value
    introdate = xml_data.getElementsByTagName('Introduced_Date')[0].firstChild.wholeText
    return title, sponsor, introdate


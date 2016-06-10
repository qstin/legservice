from xml.dom import minidom
from bs4 import BeautifulSoup
import json
import requests

"""
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
Below are some functions that connect to the LegService SOAP application for
Arizona Legilatured data. Here's what can be requested:

BillInfo:
        details for a given bill

BillsBySessionId:
        All bills from a given session. 52nd legislature is most
        recent.

FloorVotesBySessionId:
        Votes made by floor committees given a session id.
        Includes lawmaker's vote and order in which they voted.

ForAgainstNeutralBySessionID:
        Return data on Request to Speak logs. Includes signee name, position and
        organizaiton if there is one.

MemberById:
        Returns data on a given lawmaker by id. Includes party, committee
        affiliations and party.

MembersBySessionId:
        Returns all members of a given session. Includes same data as MemberById

FloorVotesByBill:
        Votes on a given bill.
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
"""

def BillInfo(bill):
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

def BillsBySessionId():
    url = 'http://azleg.gov/xml/legservice.asmx?op=BillsBySessionID'
    body="""<?xml version="1.0" encoding="utf-8"?>
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
    <BillsBySessionID
    xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    </BillsBySessionID>
    </soap:Body>
    </soap:Envelope>""".format('AZCIR','CIR35yq881cbPJ',
          115)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/BillsBySessionID"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def FloorVotesBySessionId():
    url = 'http://azleg.gov/xml/legservice.asmx?op=FloorVotesBySessionID'

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
   <FloorVotesBySessionID
   xmlns="http://azleg.gov/webservices/">
   <SessionID>{2}</SessionID>
   </FloorVotesBySessionID>
   </soap:Body>
   </soap:Envelope>""".format(
                      'AZCIR',
                      'CIR35yq881cbPJ',
                       115)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/FloorVotesBySessionID"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def ForAgainstNeutralBySessionID():
    url = 'http://azleg.gov/xml/legservice.asmx?op=ForAgainstNeutralBySessionID'
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
    <ForAgainstNeutralBySessionID
    xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    </ForAgainstNeutralBySessionID>
    </soap:Body>
    </soap:Envelope>""".format('AZCIR','CIR35yq881cbPJ',
          115)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/ForAgainstNeutralBySessionID"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def MemberById(memberID):
    url = 'http://azleg.gov/xml/legservice.asmx?op=MemberByID'
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
    <MemberByID
    xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    <MemberID>{3}</MemberID>
    </MemberByID>
    </soap:Body>
    </soap:Envelope>""".format('AZCIR',
            'CIR35yq881cbPJ',
            115,
            memberID)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/MemberByID"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def MembersBySessionId():
    url = 'http://azleg.gov/xml/legservice.asmx?op=MembersBySessionID'
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
    <MembersBySessionID
    xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    </MembersBySessionID>
    </soap:Body>
    </soap:Envelope>""".format('AZCIR','CIR35yq881cbPJ',
          115)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/MembersBySessionID"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

def FloorVotesByBill(bill):
    url = 'http://azleg.gov/webservices/FloorVotesByBill'
    body = """
    <?xml version="1.0" encoding="utf-8"?>
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
    <FloorVotesByBill
    xmlns="http://azleg.gov/webservices/">
    <SessionID>{2}</SessionID>
    <BillNum>{3}</BillNum>
    </FloorVotesByBill>
    </soap:Body>
    </soap:Envelope>""".format(
      'AZCIR',
      'CIR35yq881cbPJ',
       115,
       bill)

    encoded_text = body.encode('utf-8')
    headers = {'Host': 'azleg.gov',
            'Content-Type': 'text/xml; charset=utf-8',
            'Content-Length': len(body),
            'SOAPAction': "http://azleg.gov/webservices/FloorVotesByBill"}

    request = requests.post(url, headers=headers, data=encoded_text, verify=False)
    return request.content

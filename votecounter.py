import requests
import json
from xml.dom import minidom
import legservice


def make_lawmakers():
    xml_data = minidom.parseString(legservice.MembersBySessionId())
    member_dict = {}
    member_dict['lawmakers'] = []
    for node in xml_data.getElementsByTagName('MEMBER'):
        member_dict['lawmakers'].append(
            {"memberId": node.attributes['Member_ID'].value,
            "name": node.attributes['Full_Name'].value,
            "party": node.attributes['Party'].value, 
            "votes": {}})
     
    votes_data = minidom.parseString(legservice.FloorVotesBySessionId())
    for lawmaker in member_dict['lawmakers']:    
        for node in votes_data.getElementsByTagName('TRAN'):
            running_bill = node.attributes['Bill'].value
            for vote_node in node.getElementsByTagName('VOTE'):
                if lawmaker['memberId'] == vote_node.attributes['MemID'].value:
                    lawmaker['votes'][running_bill] = vote_node.attributes['Vote'].value

    with open('lawmakervotes.json', 'w') as jf:
        json.dump(member_dict, jf)
        jf.close()

def make_bill_results():
    xml_data = minidom.parseString(legservice.BillsBySessionId())
    bill_dict = {}
    bill_dict['bills'] = []
    for node in xml_data.getElementsByTagName('Bill'):
        running_bill = node.getElementsByTagName('Bill_Number')[0].firstChild.wholeText
        bill_dict['bills'].append({'bill': running_bill})

    with open('lawmakervotes.json', 'r') as fp:
        member_dict = json.load(fp)

    for bill in bill_dict['bills']:
        running_bill = bill['bill']
        r_yes=r_no=r_nv=r_v=r_ab=r_e=d_yes=d_no=d_nv=d_v=d_ab=d_e=0
        for lawmaker in member_dict['lawmakers']:

            if lawmaker['party'] == 'R':
                if running_bill in lawmaker['votes']:
                    if lawmaker['votes'][running_bill] == 'Y':
                        r_yes += 1
                    if lawmaker['votes'][running_bill] == 'N':
                        r_no += 1
                    if lawmaker['votes'][running_bill] == 'NV':
                        r_nv += 1
                    if lawmaker['votes'][running_bill] == 'V':
                        r_v += 1
                    if lawmaker['votes'][running_bill] == 'AB':
                        r_ab += 1
                    if lawmaker['votes'][running_bill] == 'E':
                        r_e += 1

            if lawmaker['party'] == 'D':
                if running_bill in lawmaker['votes']:
                    if lawmaker['votes'][running_bill] == 'Y':
                        d_yes += 1
                    if lawmaker['votes'][running_bill] == 'N':
                        d_no += 1
                    if lawmaker['votes'][running_bill] == 'NV':
                        d_nv += 1
                    if lawmaker['votes'][running_bill] == 'V':
                        d_v += 1
                    if lawmaker['votes'][running_bill] == 'AB':
                        d_ab += 1
                    if lawmaker['votes'][running_bill] == 'E':
                        d_e += 1

        bill['r_yes'] = r_yes
        bill['r_no'] = r_no
        bill['r_nv'] = r_nv
        bill['r_v'] = r_v
        bill['r_ab'] = r_ab
        bill['r_e'] = r_e

        bill['d_yes'] = d_yes
        bill['d_no'] = d_no
        bill['d_nv'] = d_nv
        bill['d_v'] = d_v
        bill['d_ab'] = d_ab
        bill['d_e'] = d_e

    with open('votes-by-bill.json', 'w') as fp:
        json.dump(bill_dict, fp)
    fp.close()

make_bill_results()

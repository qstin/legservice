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
            "votes": []})

    #this gets the member's vote using FloorVotesBySessionId() and member_dict
    votes_data = minidom.parseString(legservice.FloorVotesBySessionId())
    for lawmaker in member_dict['lawmakers']:
        for node in votes_data.getElementsByTagName('TRAN'):
            running_bill = node.attributes['Bill'].value
            for vote_node in node.getElementsByTagName('VOTE'):
                if lawmaker['memberId'] == vote_node.attributes['MemID'].value:
                    lawmaker['votes'].append(
                    {
                        "bill_number": running_bill,
                        "member_vote": vote_node.attributes['Vote'].value
                    })

    #this creates a dict of bills used to get party vote:
    xml_data = minidom.parseString(legservice.BillsBySessionId())
    bill_dict = {}
    bill_dict['bills'] = []
    for node in xml_data.getElementsByTagName('Bill'):
        running_bill = node.getElementsByTagName('Bill_Number')[0].firstChild.wholeText
        bill_dict['bills'].append({'bill': running_bill})

    for bill in bill_dict['bills']:
        running_bill = bill['bill']
        r_yes=r_no=r_nv=r_v=r_ab=r_e=d_yes=d_no=d_nv=d_v=d_ab=d_e=0
        for lawmaker in member_dict['lawmakers']:

            if lawmaker['party'] == 'R':
                for vote_dict in lawmaker['votes']:

                    if running_bill is vote_dict['bill_number']:
                        if vote_dict['member_vote'] == 'Y':
                            r_yes += 1
                        if vote_dict['member_vote'] == 'N':
                            r_no += 1
                        if vote_dict['member_vote'] == 'NV':
                            r_nv += 1
                        if vote_dict['member_vote'] == 'V':
                            r_v += 1
                        if vote_dict['member_vote'] == 'AB':
                            r_ab += 1
                        if vote_dict['member_vote'] == 'E':
                            r_e += 1

            if lawmaker['party'] == 'D':
                for vote_dict in lawmaker['votes']:
                    if running_bill is vote_dict['bill_number']:
                        if vote_dict['member_vote'] == 'Y':
                            d_yes += 1
                        if vote_dict['member_vote'] == 'N':
                            d_no += 1
                        if vote_dict['member_vote'] == 'NV':
                            d_nv += 1
                        if vote_dict['member_vote'] == 'V':
                            d_v += 1
                        if vote_dict['member_vote'] == 'AB':
                            d_ab += 1
                        if vote_dict['member_vote'] == 'E':
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

    for lawmaker in member_dict['lawmakers']:
        for vote in lawmaker['votes']:
            current_bill = vote['bill_number']
            for bill in bill_dict['bills']:
                running_vote = ''
                if bill['bill'] == current_bill:
                    #iterate through Republicans
                    if lawmaker['party'] == 'R':
                        if bill['r_no'] == 0 and bill['r_yes'] == 0:
                            runnint_vote = 'None'
                        if bill['r_no'] > bill['r_yes']:
                            running_vote = 'N'
                        else:
                            running_vote = 'Y'
                    #Now do Democrats
                    if lawmaker['party'] == 'D':
                        if bill['d_no'] == 0 and bill['d_yes'] == 0:
                            running_vote = 'None'
                        elif bill['d_no'] > bill['d_yes']:
                            running_vote = 'N'
                        else:
                            running_vote = 'Y'

                    vote['party_vote'] = running_vote

    return member_dict

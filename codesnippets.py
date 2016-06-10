for bill in df['bills']:
    republican_vote = ''
    democratic_vote = ''
    if bill['r_no'] == 0 and bill['r_yes'] == 0:
        if bill['d_no'] == 0 and bill['d_yes'] == 0:
            continue
    else:
        if bill['r_no'] > bill['r_yes']:
            republican_vote = 'No ' + str(bill['r_no'])
        else:
                republican_vote = "Yes " + str(bill['r_yes'])
        if bill['d_no'] > bill['d_yes']:
            democratic_vote = 'No ' + str(bill['r_no'])
        else:
            democratic_vote = 'Yes ' + str(bill['r_yes'])
    print(bill['bill'] + ": Republican vote: " +republican_vote + ", Democratic vote: " + democratic_vote)

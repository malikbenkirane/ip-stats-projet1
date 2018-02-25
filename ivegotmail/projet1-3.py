def apparitions(emails):
    compte_mots = dict()
    for email in emails:
        apparait = dict()
        for mot in email.split(' '):
            if mot not in apparait:
                apparait[mot] = 1
        for mot in apparait:
            if mot not in apparait:
                compte_mots[mot] = 0
            compte_mots[mot] += 1
    return compte_mots

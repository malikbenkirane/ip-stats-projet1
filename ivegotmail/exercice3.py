from unidecode import unidecode
import numpy as np

def normalise(emails):
    normed_emails = []
    for email in emails:
        normed_words = []
        for mot in email.split(' '):
            normed_words.append(unidecode(mot).lower())
        normed_emails.append(' '.join(normed_words))
    return normed_emails

def apparitions(emails, norm=True):
    """Compte et retourne le nombre d'emails ou apparait un mot"""
    compte_mots = dict()
    if norm:
        emails = normalise(emails)
    for email in emails:
        apparu = dict()
        for mot in email.split(' '):
            if mot not in compte_mots:
                compte_mots[mot] = 0
            if mot not in apparu:
                compte_mots[mot] += 1
                apparu[mot] = True
    return compte_mots

def histogram_mots(emails):
    comptage = apparitions(emails)
    mots, compteurs = tuple(zip(*[
        (mot, comptage[mot]) 
        for mot in sorted(comptage, key=comptage.get, reverse=True)
    ]))
    frequences = np.asarray(compteurs) / sum(compteurs)
    return mots, compteurs, frequences

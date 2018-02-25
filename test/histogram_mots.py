import numpy as np
from ivegotmail.exercice3 import histogram_mots, apparitions, normalise
from ivegotmail.exercice2 import Model

# mots, compteurs, frequences = histogram_mots(spam)
# sig = frequences.max() - frequences.min() * .05
# mostsig = frequences[frequences > sig]
# lesssig = sum(frequences[frequences < sig])

# def merge(*descriptions):
#     merge = dict()
#     for description in descriptions:
#         for word in description:
#             if word not in merge:
#                 merge[word] = 0
#             merge[word] += description[word]
#     mots, compteurs = tuple(zip(*(
#         (word, merge[word])
#         for word in sorted(merge, key=merge.get, reverse=True)
#     )))
#     return mots, compteurs


# def frac_trailing(mots, freqs, ceil_percentage):
#     assert type(freqs) == type(np.array([]))
#     mots = np.asarray(mots)
#     ceil = ceil_percentage * (freqs.max() - freqs.min())
#     return mots[freqs > ceil], freqs[freqs > ceil]


# def estimate_description(description, n_emails, mots):
#     x = []
#     for word in mots:
#         if word in description:
#             x.append(description[word])
#         else:
#             x.append(0)
#     return np.asarray(x) / n_emails


def description(email, r):
    email = normalise([email])[0]
    mots_email = email.split(' ')
    x = list()
    for word in r:
        if word in mots_email:
            x.append(1)
        else:
            x.append(0)
    return ''.join([str(w) for w in x])


class ModelMots(Model):

    def __init__(self, estimation_spam, estimation_nospam, 
                 proba_spam, proba_nospam, mots):
        self.espam = estimation_spam
        self.enospam = estimation_nospam
        self.pspam = proba_spam
        self.pnospam = proba_nospam
        self.mots = mots

    def estimate(self, x, spam=True):
        x = description(x, self.mots)
        if spam:
            if x not in self.espam:
                return 0.
            return self.espam[x]
        else:
            if x not in self.enospam:
                return 0.
            return self.enospam[x]


def representation(d_spam, card_spam, d_nospam, card_nospam, ceil):
    fusion = dict()
    N = card_spam + card_nospam
    for description in (d_spam, d_nospam):
        for word in description:
            if word not in fusion:
                fusion[word] = 0
            fusion[word] += description[word]
    words, freqs = tuple(zip(*[ 
        (word, fusion[word] / N) 
        for word in sorted(fusion, key=fusion.get, reverse=True) 
    ]))
    words, freqs = np.asarray(words), np.asarray(freqs)
    rate = card_spam / N / 2
    words, freqs = words[freqs < rate], freqs[freqs < rate]
    argceil = ceil * (freqs.max() - freqs.min())
    return words[freqs > argceil], words, freqs


def apprend_modele(r, spam, nospam):

    N = len(spam) + len(nospam)
    apparitions_spam = apparitions(spam)
    apparitions_nospam = apparitions(nospam)

    estimation_ = {} 
    for emails, label in ((spam, +1), (nospam, -1)):
        f = 1 / len(emails)
        estimation = dict()
        for email in emails:
            x = description(email, r)
            if x not in estimation:
                estimation[x] = 0
            estimation[x] += f
        estimation_[label] = estimation

    return ModelMots(
        estimation_spam=estimation_[+1],
        estimation_nospam=estimation_[-1],
        proba_spam=(len(spam)/float(N)),
        proba_nospam=(len(spam)/float(N)),
        mots=r
    )


def predit_email(emails, modele):
    allbin = list()
    for email in emails:
        x = description(email, modele.mots)
        diff = \
            modele.pspam * modele.estimate(x, spam=True) - \
            modele.pnospam * modele.estimate(x, spam=False)
        if diff > 0:
            allbin.append(1)
        else:
            allbin.append(-1)
    return allbin

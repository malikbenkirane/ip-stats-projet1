from ivegotmail.corpus import spam, nospam
import test.histogram_mots as hm
from test.histogram_mots import description
from ivegotmail.exercice3 import apparitions, normalise
import numpy as np

# CEIL = 0.1
# r,w,f = hm.representation(aspam, len(spam), anospam, len(nospam), CEIL)

def representation_plus(d_spam, card_spam, d_nospam, card_nospam):
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
    iecarts = np.where(np.diff(freqs) < 0)[0]
    diff = np.diff(iecarts)
    isig = diff[diff < 10].cumsum()[-1]
    diff[diff > 500]
    inosig = iecarts[np.where(diff > 500)[0] + 1]
    inosig = [(e, inosig[i+1]) for i,e in enumerate(inosig) if i+1 < len(inosig)]
    inosig = [(isig, inosig[0][0])] + inosig + [(inosig[-1][1], len(freqs)-1)]
    sigwords = words[:isig]
    nosigwords = [words[i0:i1] for i0,i1 in inosig]
    return sigwords, nosigwords

# sigwords, nosigwords = representation_plus(aspam, len(spam), anospam, len(nospam))


def description_plus(email, nosigr):
    email = normalise([email])[0]
    x = []
    for group in nosigr:
        n = 0
        for word in group:
            if word in email:
                n += 1
        x.append(n)
    return x


class ModelMotsPlus():

    def __init__(self, sigwords, esig, nosigwords, enosig, plabel):
        """
        sigwords -- w1...wd
        esig -- spam, nospam : estimation vecteur x1...xd
        enosig -- spam, nospam : liste estimations intervalles (freqs)
        nosigwords -- liste de liste des mots pour enosig
        """
        self.sigwords = sigwords
        self.nosigwords = nosigwords
        self.esig = esig
        self.enosig = enosig
        self.plabel = plabel

    def estimate(self, x, spam=True):

        # ESIG
        xsig = description(x, self.sigwords)
        esigspam, esignospam = self.esig[1], self.esig[-1]

        if spam:
            esig = esigspam
        else:
            esig = esignospam

        if xsig in esig:
            psig = np.log(esig[xsig])
        else:
            return 0.

        # ENOSIG
        xnosig = description_plus(x, self.nosigwords)
        enosigspam, enosignospam  = self.enosig[1], self.enosig[-1]

        if spam:
            enosig = enosigspam
        else:
            enosig = enosignospam

        pnosig = 0.
        for ibin, val in enumerate(xnosig):
            for index, (iinf, isup) in enumerate(enosig[ibin][1]):
                if val >= iinf and val < isup:
                    estim = enosig[ibin][0][index]
                    if estim > 0:
                        pnosig += np.log(estim)
                    else:
                        return 0.
                    break

        return np.exp(pnosig + psig)


    def predit(self, x):
        diff = \
            self.plabel[+1] * self.estimate(x, spam=True) - \
            self.plabel[-1] * self.estimate(x, spam=False)
        if diff > 0:
            return 1
        else:
            return -1


import sys
from multiprocessing import Pool
from itertools import product
from functools import partial

# aspam, anospam = apparitions(spam), apparitions(nospam)
# sigwords, nosigwords = \
#     representation_plus(aspam, len(spam), anospam, len(nospam))

def emails_chunks(emails, n):
    chunks = []
    split_size = int(len(emails)/n)
    for i in range(0, len(emails), split_size):
        chunks.append(emails[i:i+split_size])
    split_left = len(spam) % n
    if split_left > 0:
        chunks.append(emails[-split_left:])
    return chunks


def description_plus_parallel(emails, nosigwords, threads=6):
    pool = Pool(threads)
    results = pool.map(
        partial(description_plus, nosigr=nosigwords),
        emails
    )
    return results


def apprend_modele(spam, nospam, threads=1):

    aspam, anospam = apparitions(spam), apparitions(nospam)
    sigwords, nosigwords = \
        representation_plus(aspam, len(spam), anospam, len(nospam))
    
    esig_all = {} 
    print('Apprend ESIG (%i sigwords)' % len(sigwords))
    for emails, label in ((spam, +1), (nospam, -1)):
        f = 1 / len(emails)
        esig = dict()
        for i, email in enumerate(emails):
            sys.stdout.write('\rLabel {} -- {:.0%}'.format(label, i / len(emails)))
            x = description(email, sigwords)
            if x not in esig:
                esig[x] = 0
            esig[x] += f
        print()
        esig_all[label] = esig

    print('Apprend ENOSIG...')
    dplus = {
        +1: np.array(
            description_plus_parallel(
                spam, nosigwords, threads=threads
            )
        ),
        -1: np.array(
            description_plus_parallel(
            nospam, nosigwords, threads=threads
            )
        )
    }
    print('Estimation ENOSIG...')
    enosig_all = {+1: [], -1: []}
    for card, label in ((len(spam), +1), (len(nospam), -1)):
        for ibin in range(dplus[label].shape[1]):
            # sys.stdout.write('\rbin %i/%i ...' % (ibin, dplus[label].shape[1]))
            nbemail, bornes = np.histogram(dplus[label][:,ibin])
            bornes = [
                (binf, bornes[i+1])
                for i, binf in enumerate(bornes) if i + 1 < len(bornes)
            ]
            enosig_all[label].append((nbemail / card, bornes))

    N = len(spam) + len(nospam)
    plabel = {+1: len(spam) / N, -1: len(nospam) / N}

    return ModelMotsPlus(sigwords, esig_all, nosigwords, enosig_all, plabel)

# m = hm.apprend_modele(r, spam, nospam)
def predit_emails(emails, modele):
    N = len(emails)
    predictions = list()
    for i, email in enumerate(emails):
        sys.stdout.write('\rEmail %i/%i' % (i, N))
        predictions.append(modele.predit(email))
    return predictions


def predit_parallel(emails, modele, threads=6):
    pool = Pool(threads)
    chunks = emails_chunks(emails, threads)
    predictions = pool.map(
        partial(predit_emails, modele=modele),
        chunks
    )
    return [p for pp in predictions for p in pp]

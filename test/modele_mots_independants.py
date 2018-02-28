######### Ce modele n'est pas suffisant pour classifier

from test.independance import representation_generale
from test.histogram_mots import description as description_hm
import numpy as np

DMOTS = 10000

class ModeleMotsInde():

    def __init__(self, estimations, plabels, mots):
        self.estimations = estimations
        self.mots = mots
        self.plabels = plabels


    def predit(self, x):
        diff = \
            self.plabels[+1] * self.estimate(x, spam=True) - \
            self.plabels[-1] * self.estimate(x, spam=False)
        if diff > 0:
            return 1
        else:
            return -1

    def description(self, email):
        x = list()
        for ax in description_hm(email, self.mots): 
            x.append(int(ax))
        return np.asarray(x)

    def estimate(self, x, spam=True):
        x = description_hm(x, self.mots)
        if spam:
            estimation = self.estimations[1]
        else:
            estimation = self.estimations[-1]
        pre = [ np.log(estimation[i]) for i, w in enumerate(x) if w != 0 ]
        return np.exp(sum(pre))

from functools import partial
from multiprocessing import Pool

def estimation_worker(email, f, modele):
    x = modele.description(email)
    return  x * f


def apprend_modele(spam, nospam, threads=6):

    words, freqs = representation_generale(spam + nospam)
    mots = words[:DMOTS]

    N = len(spam) + len(nospam)
    plabels = {+1: len(spam) / N, -1: len(nospam) / N}
    modele = ModeleMotsInde(None, plabels, mots)

    pool = Pool(threads)

    estimation = {+1: np.zeros((len(mots),)), -1: np.zeros((len(mots),))}
    for train_set, label in (spam, 1), (nospam, -1):
        f = 1 / len(train_set)
        results = pool.map(
            partial(estimation_worker, f=f, modele=modele),
            train_set
        )
        estimation[label] = sum(results)
        # for email in train_set:
        #     x = modele.description(email)
        #     estimation[label] += x * f

    return ModeleMotsInde(estimation, modele.plabels, modele.mots)

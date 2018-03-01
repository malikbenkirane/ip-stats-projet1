import sys
import numpy as np
from test.modele_mots_independants import DMOTS, apprend_modele
from test.independance import representation_generale as representation
from ivegotmail.projet1 import estimation_erreur
from ivegotmail.corpus import spam, nospam
from ivegotmail.tools import split
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool
from functools import partial

mots, freqs = representation(spam + nospam)

train_spam, test_spam = split(spam, SPLIT)
train_nospam, test_nospam = split(nospam, SPLIT)

SPLIT = .8

def apprenti_worker(decalage, train_spam, train_nospam):
    sys.stdout.write('\rdec:%i' % decalage)
    modele = apprend_modele(train_spam, train_nospam, decalage=decalage, threads=3)
    return modele


def submit_learn():
    decalages = tuple(range(0, len(mots), DMOTS))
    print('Test de %i decalages' % len(decalages))

    pool = ThreadPool(2)
    modeles = pool.map(
        partial(apprenti_worker, train_spam=train_spam, train_nospam=train_nospam),
        decalages
    )
    return modeles

def estimation_erreur_worker(modele, spam, nospam):
    erreurs = 0
    for emails, label in ((spam, 1), (nospam, -1)):
        prediction = np.asarray([
            modele.predit(email) for email in emails
        ])
        erreurs += len(prediction[prediction != label])
    return erreurs / (len(spam) + len(nospam))


def submit_erreur(modeles, threads=7):
    pool = Pool(threads)
    erreurs = pool.map(
        partial(estimation_erreur_worker, spam=test_spam, nospam=test_nospam),
        modeles
    )
    return erreurs

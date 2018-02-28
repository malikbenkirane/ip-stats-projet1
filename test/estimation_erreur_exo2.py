import ivegotmail
from ivegotmail.projet1 import apprend_modele, estimation_erreur
from ivegotmail.corpus import spam, nospam
from ivegotmail.tools import split

import sys


NTEST = 40
SPLIT = .8

erreurs = {
    'test': [],
    'train': []
}

for i in range(NTEST):
    sys.stdout.write('\rtest %i/%i ...' % (i, NTEST))
    spam_test, spam_train = split(spam, SPLIT)
    nospam_test, nospam_train = split(nospam, SPLIT)
    modele = apprend_modele(spam_train, nospam_train)
    erreur_test = estimation_erreur(spam_test, nospam_test, modele)
    erreur_train = estimation_erreur(spam_train, nospam_train, modele)
    erreurs['test'].append(erreur_test)
    erreurs['train'].append(erreur_train)

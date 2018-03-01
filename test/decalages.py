from test.histogram_mots import apprend_modele, predit_email
from test.independance import representation_generale
from test.modele_mots_independants import DMOTS
from ivegotmail.corpus import spam, nospam
from functools import partial
from multiprocessing import Pool

words, freqs = representation_generale(spam + nospam)

def apprenti_worker(decalage, spam, nospam):
    return apprend_modele(words[decalage:DMOTS+decalage], spam, nospam)

DECALAGES = tuple(range(0, len(words), DMOTS))

def submit_learn():
    pool = Pool(7)
    modeles = pool.map(
        partial(apprenti_worker, spam=spam, nospam=nospam),
        DECALAGES
    )
    return modeles

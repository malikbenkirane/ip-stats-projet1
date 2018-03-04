from test.histogram_mots import description as description_h_noind
from ivegotmail.exercice3 import apparitions, normalise
from ivegotmail.corpus import spam, nospam
from test.modele_mots import representation_plus
import numpy as np

"""Hypotheses a tester :
- h_ind : les probas sont independantes on peux faire le produit
- h_noind : les probas ne sont pas independates
J'utilise ses notations en suffixe pour les noms de variables et de fonctions
"""

def representation_generale(emails):
    count_dict = apparitions(emails)
    words, freqs = tuple(zip(*[
        (word, count_dict[word] / len(emails))
        for word in sorted(count_dict, key=count_dict.get, reverse=True)
    ]))
    return words, freqs

# restrictions a une representation r
def representation_arbitraire(words, n0=0, n1=500):
    return words[n0:n1]

def description_h_ind(d_h_noind):
    x = []
    for _x in d_h_noind:
        x.append(int(_x))
    return x

def estimations(emails, r):
    """Retourne le couple (estimation_h_noind, estimation_h_ind) :

        - l'estimation si on suppose non independantes les apparitions des mots
        de r et dans ce cas c'est un dictionnaire avec pour cles x1,...,xn avec
        x_i qui est 0 ou 1

        - l'estimation si on suppose independantes les apparitions des mots de
        r et dans ce cas c'est une liste [f1,...,fn] de l'estimation de
        l'apparition de chaque mot independament

    Arguments:

    emails -- liste emails
    r -- representation i.e. liste de mots
    """
    estimation_h_noind = {}
    estimation_h_ind = np.zeros((len(r),))
    f = 1 / len(emails)
    for email in emails:
        x_h_noind = description_h_noind(email, r)
        x_h_ind  = description_h_ind(x_h_noind)
        if x_h_noind  not in estimation_h_noind:
            estimation_h_noind[x_h_noind] = 0
        estimation_h_noind[x_h_noind] += f
        estimation_h_ind += np.asarray(x_h_ind) * f
    return estimation_h_noind, estimation_h_ind


# base de tests
emails = spam + nospam

words, freqs = representation_generale(emails)
# TODO faire le test sur plusieurs representations 
r = representation_arbitraire(words)
rplus, _ = representation_plus(
    apparitions(spam), len(spam), apparitions(nospam), len(nospam)
)

def erreur_independance(r):
    e_h_noind, e_h_ind =  estimations(emails, r)
    eexp_h_noind = {}
    for x in e_h_noind:
        x_h_ind = description_h_ind(x)
        eexp_h_noind[x] = np.exp(np.sum([np.log(f) for f in x_h_ind]))

    keys = list(e_h_noind.keys())
    e_h_noind = np.asarray(list(e_h_noind.values()))
    eexp_h_noind = np.asarray(list(eexp_h_noind.values()))
    diff = e_h_noind - eexp_h_noind
    diff_index = { x: diff[i] for i, x in enumerate(keys) }
    sorted_diff = [
        (x, diff_index[x]) 
        for x in sorted(diff_index, key=diff_index.get, reverse=True)
    ]
    return tuple(zip(*sorted_diff))


if __name__ == '__main__':
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots(figsize=(12,4))
    x_arbitraire, err_r_arbitraire = erreur_independance(r)
    x_plus, err_plus = erreur_independance(rplus)
    ax.plot(err_r_arbitraire)
    ax.plot(err_plus)
    ax.legend([
        'representation modele (a)', 
        'representation arbitraire 500 premiers mots'
    ])
    ax.set_ylabel('erreur |P(X) - P(X1)...P(Xn)|')
    ax.set_xlabel('x (description)')
    plt.tight_layout()
    fig.savefig('independance.png')

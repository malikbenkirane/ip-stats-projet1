import numpy as np


def unique(lst):
    uni = list()
    for e in lst:
        if e not in uni:
            uni.append(e)
    return uni


def histogram(mail_list, size=1):
    lengths = tuple(sorted([len(mail) for mail in mail_list]))
    _unique_lengths = tuple(unique(lengths))
    # preparing bins
    intervals = list()
    for i, l in enumerate(_unique_lengths):
        if i % size != 0:
            continue
        if i + size < len(_unique_lengths):
            intervals.append(range(l, _unique_lengths[i + size]))
    # filling bins
    bins = [0 for _, _ in enumerate(_unique_lengths)]
    for x in lengths:
        for i, interval in enumerate(intervals):
            if x in interval:
                bins[i] += 1
                break
    return tuple(zip(intervals,bins))


def prepare_bins(a_list, size):
    intervals = list()
    for i, l in enumerate(a_list):
        if i % size != 0:
            continue
        if i + size < len(a_list):
            intervals.append((l, a_list[i+size]))
    return intervals

def fill_bins(a_list, intervals):
    bins = [0 for i in a_list]
    for x in a_list:
        for i, interval in enumerate(intervals):
            if x in range(interval[0], interval[1]):
                bins[i] += 1
                break
    return bins


def histogram1(emails, size=1):
    lengths = tuple(sorted([len(mail) for mail in emails]))
    _unique_lengths = tuple(unique(lengths))
    intervals = prepare_bins(_unique_lengths, size)
    bins = fill_bins(lengths, intervals)
    return intervals, bins


class Model():
    """Le modele est decrit par
    1. la distribution de probabilite des spam
    2. la distribution de probabilite de no spam
    3. les estimations de probabilites pour P(Y=1) ou P(Y=-1)
    Ces distributions sont estimees sur des intervalles autour de chacune des
    donnees d'apprentissage"""

    def __init__(self, estimation_spam, estimation_nospam, proba_spam, proba_nospam):
        self.espam = estimation_spam
        self.enospam = estimation_nospam
        self.pspam = proba_spam
        self.pnospam = proba_nospam

    def estimate(self, x, spam=True):
        if spam:
            intervals = self.espam[0]
        else:
            intervals = self.enospam[0]
        for i, interval in enumerate(intervals):
            if x in range(interval[0], interval[1]):
                break
        if spam:
            return self.espam[1][i]
        else:
            return self.enospam[1][i]


def apprend_modele(spam, nospam):
    intervals_spam, bins_spam = histogram1(spam)
    intervals_nospam, bins_nospam = histogram1(nospam)
    bins_spam = np.asarray(bins_spam) / len(spam)
    bins_nospam = np.asarray(bins_nospam) / len(nospam)
    n = len(spam) + len(nospam)
    return Model(estimation_spam=(intervals_spam, bins_spam),
                 estimation_nospam=(intervals_nospam, bins_nospam),
                 proba_spam=(len(spam)/float(n)),
                 proba_nospam=(len(nospam)/float(n)))


def predit_email(emails, modele):
    allbin = list()
    spambin, nospambin = list(), list()
    for i, email in enumerate(emails):
        x = len(email)
        diff = \
            modele.pspam * modele.estimate(x, spam=True) - \
            modele.pnospam * modele.estimate(x, spam=False)
        if diff > 0:
            spambin.append(i)
            allbin.append(1)
        else:
            nospambin.append(i)
            allbin.append(-1)
    return allbin


def estimation_erreur(spam, nospam, modele):
    erreurs = 0
    for mails, label in ((spam, 1), (nospam, -1)):
        prediction = np.asarray(predit_email(mails, modele))
        erreurs = len(prediction[prediction != label])
    return erreurs / (len(spam) + len(nospam))

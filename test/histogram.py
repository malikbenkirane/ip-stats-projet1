import ivegotmail 
from ivegotmail.corpus import spam, nospam
from ivegotmail.projet1 import histogram

from matplotlib import pyplot as plt
import numpy as np

BINSIZE = 5

plt.close('all')

fig, axes = plt.subplots(nrows=2, sharex=True)


histo_spam = histogram(spam, BINSIZE)
histo_nospam = histogram(nospam, BINSIZE)

#if __name__ == '__main__':

xspam, yspam, xsup_spam = tuple(zip(*(
    (i[0], n, i[-1]) for (i, n) in histogram(spam, BINSIZE)
)))

xnospam, ynospam, xsup_nospam = tuple(zip(*(
    (i[0], n, i[-1]) for (i, n) in histogram(nospam, BINSIZE)
)))

index = (tuple(range(len(xnospam))), tuple(range(len(xspam))))
xsup = (xsup_nospam, xsup_spam)
x, y, label = ((xnospam, xspam), (ynospam, yspam), ('-1', '1'))

if len(x[0]) < len(x[1]):
    imax = 1
else:
    imax = 0

for i in (imax, (imax+1)%2):
    _x, _y, _label, _index = x[i], y[i], label[i], index[i]
    _ycum = np.cumsum(_y)
    ax = axes[(imax+i+1)%2]
    ax.bar(_index, _ycum, .1 * 8)
    ax.plot(_index, _ycum)
    ax.set_ylabel('P(X=x|Y=%s)' % _label)
    #yticks = tuple(range(0, max(_y), 2))
    #ax.set_yticks(yticks)

step = 1
maxticks = 20
if len(index[imax]) > maxticks:
    step = int(len(x[imax]) / maxticks)
xticks = tuple(range(0, len(index[imax]), step))
_xsup = [x[imax][xticks[i+1]] for i in  range(len(xticks)-1)]
_xsup.append(xsup[imax][-1])
xticklabels = ['[%s,%s[' % (x[imax][s], _xsup[i]) for i, s in enumerate(xticks)]
#print (xticks, xticklabels)
axes[1].set_xticks(xticks)
axes[1].set_xticklabels(xticklabels, rotation=45, ha='right')
axes[1].set_xlabel('x')
#ax.set_label('x: longueur(mail)')


plt.tight_layout()
fig.show()

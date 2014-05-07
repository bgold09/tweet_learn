import numpy as np
from sklearn import svm
import pylab as pl

def plot_regularization(clf, ml):
    X = ml[0]
    Y = ml[1]
    C_s = np.logspace(-10, 0, 10)

    scores = list()
    scores_std = list()
    for C in C_s:
        svc.C = C
        this_scores = cross_validation.cross_val_score(svc, X, Y, n_jobs=1)
        scores.append(np.mean(this_scores))
        scores_std.append(np.std(this_scores))

        pl.figure(1, figsize=(4, 3))
        pl.clf()
        pl.semilogx(C_s, scores)
        pl.semilogx(C_s, np.array(scores) + np.array(scores_std), 'b--')
        pl.semilogx(C_s, np.array(scores) - np.array(scores_std), 'b--')
        locs, labels = pl.yticks()
        pl.yticks(locs, map(lambda x: "%g" % x, locs))
        pl.ylabel('CV score')
        pl.xlabel('Parameter C')
        pl.ylim(0, 1.1)
        pl.show()

import os
import numpy as np
from sklearn import svm
import pylab as pl
import random

def cross_validation(n, features, labels, penalty):
    """return the scores for 'n' fold cross validation
    
    Args:
        n: number of folds
        features: feature matrix
        labels: labels for feature matrix
        penalty: penalty parameter for classifier

    Returns:
        scores for this permutation test
    """
    clf = svm.SVC(kernel='linear', C=penalty).fit(features, labels)
    X_folds = np.array_split(features, n)
    y_folds = np.array_split(labels, n)
    scores = list()
    for k in xrange(n):
        X_train = list(X_folds)
        X_test  = X_train.pop(k)
        X_train = np.concatenate(X_train)
        y_train = list(y_folds)
        y_test  = y_train.pop(k)
        y_train = np.concatenate(y_train)
        scores.append(clf.fit(X_train, y_train).score(X_test, y_test))
    return np.array(scores)


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

        import pylab as pl
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

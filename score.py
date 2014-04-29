import os
import numpy as np
from sklearn import svm
import pylab as pl
import random

def cross_validation(n, features, labels, penalty):
    """return the scores for 'n' fold cross validation
    
        Args:
            n: number of folds
            features: feature vector
            labels: labels for feature vectors
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
    return scores

def permutation_test(num_sims, folds, features, labels):
    """Run a permutation test   

        Args:
            num_sims: number of simulations to run
            folds: number of folds to use for cross validation
            features: feature vector
            labels: labels for feature vectors

        Returns: 
            p-value for the permutation test, i.e. how many tests had 
            a test statistic greater than or equal to the original 
            test statistic
    """
    scores = cross_validation(folds, features, labels, 1.0)
    test_stat = scores.mean()
    count = 0
    for p in xrange(0, num_sims):
        random.shuffle(labels)
        s = cross_validation(folds, features, labels, 1.0)
        t = s.mean()
        if t >= test_stat:
            count += 1
    pvalue = count / float(num_sims)
    return pvalue

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


def score_stat(features, labels, test_size, penalty):
    """Train a SVM and get the score of classifying test_size data points

        Args:
            features: feature matrix
            labels: labels for feature matrix
            test_size: size of the testing set
            penalty: penalty parameter for classifier

        Returns:
            accuracy of the model's classification of test_size data points
    """
    clf = svm.SVC(kernel='linear', C=penalty).fit(features[:-test_size], labels[:-test_size])
    score = clf.score(features[-test_size:], labels[-test_size:])
    return score


def permutation_test(num_sims, test_size, features, labels):
    """Run a permutation test   

        Args:
            num_sims: number of simulations to run
            test_size: number of data points to test over
            features: feature matrix
            labels: labels for feature matrix

        Returns: 
            p-value for the permutation test, i.e. how many tests had 
            a test statistic greater than or equal to the original 
            test statistic
    """
    la = labels.copy()
    test_stat = score_stat(features, la, test_size, 1.0)
    count = 0
    for p in xrange(0, num_sims):
        random.shuffle(la)
        t = score_stat(features, la, test_size, 1.0)
        if t >= test_stat:
            count += 1
    pvalue = count / float(num_sims)
    return pvalue

import numpy as np
import pylab as pl
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import roc_curve, auc

def compute_curve(data, targets, test_size):
    """Compute a receiever operating characteristic (ROC) curve 

    Args:
        data: feature matrix of data 
        targets: labels for data
        test_size: size to make the testing set; 0 < test_size < len(data)

    Returns:
        A 3-tuple of the form (tpr, fpr, roc_auc), where
        tpr is a list of true positive rates, 
        fpr is a list of false positive rates, and 
        roc_auc is the area under the ROC curve
    """
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = \
            train_test_split(data, targets, test_size=test_size, random_state=0)

    # Run the classifier
    clf = svm.SVC(kernel='linear', probability=True, random_state=0)
    y_pred = clf.fit(x_train, y_train).predict_proba(x_test)
    fpr, tpr, thresholds = roc_curve(y_test, y_pred[:, 1])
    roc_auc = auc(fpr, tpr)
    return (fpr, tpr, roc_auc)

def display_curve(fpr, tpr, roc_auc):
    """Display an ROC curve

    Args:
        tpr: list of true positive rates for the curve
        fpr: list of false positive rates for the curve
        roc_auc: area under the ROC curve
    """
    pl.clf()
    pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('ROC Curve')
    pl.legend(loc="lower right")
    pl.show()

def compute_display_curve(data, targets, test_size):
    """Compute and display an ROC curve

    Args:
        data: feature matrix of data 
        targets: labels for data
        test_size: size to make the testing set; 0 < test_size < len(data)
    """
    fpr, tpr, roc_auc = compute_curve(data, targets, test_size)
    display_curve(fpr, tpr, roc_auc)


def mult_tests(data, targets, test_sizes):
    """Compute multiple ROC curves and display them on the same plot

    Args:
        data: feature matrix of data 
        targets: labels for data
        test_sizes: list of sizes to make the testing set; 
                    for all i in test_sizes, 0 < test_size[i] < len(data)
    """
    pl.clf()
    results = list()
    for i in xrange(0, len(test_sizes)):
        fpr, tpr, roc_auc = compute_curve(data, targets, test_sizes[i])
        pl.plot(fpr, tpr, label='ROC curve (test size = %d, area = %0.2f)' % \
                (test_sizes[i], roc_auc))

    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('ROC Curves')
    pl.legend(loc="lower right")
    pl.show()


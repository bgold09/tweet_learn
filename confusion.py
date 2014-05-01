from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

import pylab as pl
import numpy as np

tp = (0, 0)   # index of true positive in a confusion table
fn = (0, 1)   # index of false negative in a confusion table
fp = (1, 0)   # index of false positive in a confusion table
tn = (1, 1)   # index of true negative in a confusion table

def generate_matrix(classifier, data, targets, test_size):
    """Generate a confusion matrix for classifier

    Args: 
        classifier: the support vecftor machine to use for classification
        data: feature matrix of data
        targets: labels for the data
        test_size: size of the testing set

    Returns:
        Confusion matrix of classifier's output
    """
    # Split the data into training and testing sets
    x_train, x_test, y_train, y_test = \
            train_test_split(data, targets, test_size=test_size, random_state=0)
    
    # Run the classifier
    y_pred = classifier.fit(x_train, y_train).predict(x_test)
    
    # Compute the Confusion matrix
    cfm = confusion_matrix(y_test, y_pred)
    return cfm

def matrix_to_table(cfm, label):
    """Convert a confusion matrix to a confusion table of 
       true/false positive/negative values

    Args:
        cfm: confusion matrix to convert
        label: label index for the confusion table

    Returns:
        The confusion table of true/false positive/negative values for cfm 
        as a 2x2 numpy array.
    """
    predicfted = cfm[label]
    acftual    = [cfm[i][label] for i in range(len(cfm))]
    true_pos  = predicfted[label]
    false_pos = sum(acftual) - true_pos
    false_neg = sum(predicfted) - true_pos
    total     = sum([sum(i) for i in cfm])
    true_neg  = total - true_pos - false_pos - false_neg
    
    cft = np.array([true_pos, false_neg, false_pos, true_neg]).reshape(2, 2)
    return cft

def accuracy(cft):
    """Compute the accuracy of the classifier with confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        Accuracy of the classifier with confusion table cft.
        type: float
    """
    # Sum the diagonal
    accuracy = (cft[tp] + cft[tn]) / float(np.sum(cft))
    return accuracy

def precision(cft):
    """Compute the precision of the classifier with confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        Precision of the classifier with confusion table cft. 
        type: float
    """
    precision = cft[tp] / float(cft[tp] + cft[fp])
    return precision

def recall(cft):
    """Compute the recall (i.e. true positive rate) of the classifier 
       with confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        Recall of the classifier with confusion table cft. 
        type: float
    """
    recall = cft[tp] / float(cft[tp] + cft[fn])
    return recall

def false_positive(cft):
    """Compute the false positive rate of the classifier with 
       confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        False positive rate of the classifier with confusion table cft. 
        type: float
    """
    false_positive = cft[fp] / float(cft[fp] + cft[tn])
    return false_positive

def specificity(cft):
    """Compute the specificity (i.e. true negative rate) of the classifier 
       with confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        Specificity of the classifier with confusion table cft. 
        type: float
    """
    specificity = cft[tn] / float(cft[tn] + cft[fp])
    return specificity

def confusion_metrics(cft):
    """Compute metrics of the classifier with confusion table cft.

    Args:
        cft: confusion table for the classifier

    Returns:
        False positive rate of the classifier with confusion table cft. 
        type: float
    """
    acc = accuracy(cft)
    prec = precision(cft)
    rec = recall(cft)
    fp = false_positive(cft)
    spec = specificity(cft)
    fmt = "accuracy = %s\nprecision = %s\ntrue positive = %s\n" + \
            "false_positive = %s\ntrue negative = %s"
    print(fmt % (acc, prec, rec, fp, spec))

def confusion_matrix_show(cm):
    """Display confusion matrix cm in a new window
    
    Args: 
        cm: confusion matrix to display
    """
    # Show confusion matrix in a new window
    pl.matshow(cm)
    pl.title('Confusion matrix')
    pl.colorbar()
    pl.xlabel('Predicted class')
    pl.ylabel('True class')
    pl.show()


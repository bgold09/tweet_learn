from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix

import pylab as pl

def gen_confusion_matrix(classifier, data, targets, test_size):
    """Generate a confusion matrix for classifier

    Args: 
        classifier: the support vector machine to use for classification
        data: feature matrix of data
        targets: labels for the data
        test_size: size of the testing set

    Returns:
        Confusion matrix of classifier's output
    """
    # Split the data into training and testing sets
    x_train = data[:-test_size]
    x_test = data[-test_size:]
    y_train = targets[:-test_size]
    y_test = targets[-test_size:]
    
    # Run the classifier
    y_pred = classifier.fit(x_train, y_train).predict(x_test)
    
    # Compute the Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    return cm

def show_confusion_matrix(cm):
    """Display confusion matrix cm in a new window
    
    Args: 
        cm: confusion matrix to display
    """
    # Show confusion matrix in a new window
    pl.matshow(cm)
    pl.title('Confusion matrix')
    pl.colorbar()
    pl.ylabel('True label')
    pl.xlabel('Predicted label')
    pl.show()


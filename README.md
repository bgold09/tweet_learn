# tweet_learn

The purpose of this project is - using machine learning methods - to predict the following about tweets (posts on [twitter](http://twitter.com)):
1. Are tweets informative or non-informative?
2. Will a tweet be re-tweeted by another user? 

## Installation 

### 1. Clone the repository

```sh
git clone https://github.com/bgold09/tweet_learn.git
cd tweet_learn
```

### 2. Install required Python packages

Use your preferred method ([pip](http://pip-installer.org/), apt-get, etc.) to install the following Python packages required by **tweet learn**: 

* [genism](http://radimrehurek.com/gensim/)
* [matplotlib](http://matplotlib.org/)
* [MySQLdb](http://dev.mysql.com/doc/connector-python/en/)
* [NumPy](http://numpy.org/)
* [PyNER](https://github.com/dat/pyner)
* [scikit-learn](http://scikit-learn.org/)
* [SciPy](http://scipy.org/) 

### 3. Install Stanford Named Entity Recognizer (NER)

Download and unpack the [Stanford Named Entity Recognizer](http://nlp.stanford.edu/software/CRF-NER.shtml): 

```sh
wget http://nlp.stanford.edu/software/stanford-ner-2014-01-04.zip
unzip stanford-ner-2014-01-04.zip
```

Start a local NER java server (do this in a separate terminal window, as starting the process in the background will cause the server to function improperly):

```sh
java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/ner-eng-ie.crf-3-all2008-distsim.ser.gz -port 8080 -outputFormat inlineXML 
```

### 4. Create a MySQL database and required tables

```sh
mysql -u <username> -p -e 'CREATE DATABASE twitter;'
mysql -u <username> -p twitter < data/users_backup.sql
```

From a python session:

```python
>>> import tweet_learn as tl
>>> tl.store_initial_data("train_test_set")
>>> tl.add_centrality_feature("train_test_set")
```

### 5. Extract the data and targets

From a python session:

```python
>>> ml = tl.extract_transform_data("train_test_set", 0, 1001)
```

### 6. Run tests

Check out [confusion.py](https://github.com/bgold09/tweet_learn/blob/master/confusion.py), [score.py](https://github.com/bgold09/tweet_learn/blob/master/score.py) and [roc.py](https://github.com/bgold09/tweet_learn/blob/master/roc.py) for various methods for testing the quality of your models. 

## License

Copyright (c) 2014 Scott Bickel, Brian Golden, Stephen Styer

Licensed under the MIT license.

#!/usr/bin/env 

#Author:  Steven Styer
#Date:    Mon 17 Feb 2014 01:48:10 PM EST
#Purpose: Test ML algorithms on our CSV

import csv
import numpy as np
from sklearn import svm
import pylab as pl
import ner
fn1 = "tweetSubset_labeled.csv"
fn2 = "training_data.csv"

def read_tweets():
    fet = list()
    ans = list()
    with open(fn2, 'r') as csvfile:
        tweet_reader = csv.reader(csvfile, delimiter = ',')
        tweet_reader.next()
        print "reading: ", fn2

        for row in tweet_reader:
#            print row
            website = row[4]
            if website == '':
                website = 0
            else:
                website = 1
            ret_cnt = row[7]
            if ret_cnt == '':
                continue
            ret_cnt = int(row[7])
            rep = int(row[8])
            label = row[9]
            if label == 'I':
                label = 1
            elif label == 'C':
                label = 0
            else:
                continue
            num_people = int(row[10])
            num_orgs = int(row[11])
            num_locs = int(row[12])

            print "herp: ", (website, ret_cnt, rep, num_people, num_orgs, num_locs)
            fet.append((website, ret_cnt, rep,  num_people, num_orgs, num_locs))
            ans.append(label)

        print "fet: ", fet
        np_fet = np.array(fet)
        print "ans: ", ans
        np_ans = np.array(ans)

    return (np_fet, np_ans)

def fit_plot():
    ml = read_tweets()
    clf = svm.SVC(kernel='linear')
    clf.fit(ml[0], ml[1])
    w = clf.coef_[0]
    a = -w[0] / w[1]
    xx = np.linspace(-5, 5)
    yy = a * xx - (clf.intercept_[0]) / w[1]
    b = clf.support_vectors_[0]
    yy_down = a * xx + (b[1] - a * b[0])
    b = clf.support_vectors_[-1]
    yy_up = a * xx + (b[1] - a * b[0])
    pl.plot(xx, yy, 'k-')
    pl.plot(xx, yy_down, 'k--')
    pl.plot(xx, yy_up, 'k--')
    
    pl.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1],
               s=80, facecolors='none')
    pl.scatter(ml[0][:, 0], ml[0][:, 1], c=ml[1], cmap=pl.cm.Paired)

    pl.axis('tight')
    pl.show()

def ner_populate():
    """PRE:  java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/ner-eng-ie.crf-3-all2008-distsim.ser.gz -port 8080 -outputFormat inlineXML  --------- MUST BE RUNNING
       POST: populate the NER columns in our dataset"""
    ncols = 9
    tweet_set = list()
    tagger = ner.SocketNER(host='localhost', port=8080)

    with open(fn1, 'r') as csvfile:
        tweet_reader = csv.reader(csvfile, delimiter = ',')
        tweet_reader.next()
        print "reading: ", fn1

        for row in tweet_reader:
            st = row[3]                     #get the text of the tweet
            di = tagger.get_entities(st)
            num_people = num_orgs = num_locs = 0

            if 'PERSON' in di:
                num_people = len(di['PERSON']) 
            if 'ORGANIZATION' in di:
                num_orgs = len(di['ORGANIZATION'])
            if 'LOCATION' in di:
                num_locs = len(di['LOCATION'])

            li = [row[col] for col in xrange(ncols)]
            li.extend([num_people, num_orgs, num_locs])
            tweet_set.append(li)
#            print "li: ", li

    print "subest of tweet_set: ", tweet_set[:10]

    with open(fn2, 'w') as csvfile:
        tweet_writer = csv.writer(csvfile, delimiter = ',')
        for row in tweet_set:
#            print "row: ", row
            tweet_writer.writerow(row)
            
            
            
            
    

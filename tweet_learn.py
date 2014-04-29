#!/usr/bin/env 
#Author:  Steven Styer
#Date:    Mon 17 Feb 2014 01:48:10 PM EST
#Purpose: Test ML algorithms on our CSV

import os
import csv
import numpy as np
from sklearn import svm
import pylab as pl
import ner
import math
import MySQLdb as mdb
#import gensim as gs

tweet_subset = "tweetSubset_danielle.csv"
transformed_set = "features.csv"
train_test_set = "dani_tweets.csv"
    
def classify(ml, c):
    """use a SVM to create a classifier where ml[0] is the feature matrix and ml[1] is the labels. c is the regularization parameter for the trade-off between the separating margin and the number of errors"""

    return svm.SVC(kernel='rbf', C=c)
    
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
def extract_transform_data(tbl_name, a, b):
    """PRE:  java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/ner-eng-ie.crf-3-all2008-distsim.ser.gz -port 8080 -outputFormat inlineXML  --------- MUST BE RUNNING to get the Named-Entity data. 
             The other data comes from the SQL table init_data     
      POST: populate the NER columns in our dataset"""

    con = mdb.connect(host="localhost", user="root", passwd="", db="twitter") 
    cur = con.cursor(mdb.cursors.DictCursor)
    tweet_set = list()
    labels = list()
    tagger = ner.SocketNER(host='localhost', port=8080)

    cur.execute("select * from {0} limit %s, %s".format(tbl_name), (a, b))
    rows = cur.fetchall()

    for row in rows:
        ncols = len(row.keys())
        st = row["tweet"]                     #get the text of the tweet
        di = tagger.get_entities(st)
        num_people = num_orgs = num_locs = 0
            
        if 'PERSON' in di:
            num_people = len(di['PERSON']) 
        if 'ORGANIZATION' in di:
            num_orgs = len(di['ORGANIZATION'])
        if 'LOCATION' in di:
            num_locs = len(di['LOCATION'])

        website = row["website"]
        if website == '':
            website = 0
        else:
            website = 1
        ret_cnt = int(row["raw_retweet_count"])
        #            print "ret_cnt: ", ret_cnt
        if ret_cnt == '':
            continue
        ret_cnt = int(row["raw_retweet_count"])
        tweet = row["tweet"]
        if tweet == "":
            continue
        ret = int(tweet[0].__contains__('@'))
        rep = int(tweet[0:2].__contains__('RT'))
        cent = row["eig_centrality"]
        if cent == None:
            continue
        
        li = [website, ret_cnt, rep, ret, num_people, num_orgs, num_locs, cent]
        label = row["I_c"]

        labels.append(label)
        tweet_set.append(li)
    
    print "subset of features: ", tweet_set[:10]
    
    cur.close()
    con.close()
    return (np.array(tweet_set), np.array(labels))
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def store_features(tweet_set):
    """create and populate a sql table of features"""
    con = mdb.connect(host="localhost", user="root", passwd="", db="twitter") 
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("drop table if exists nght_regime;")
    cur.execute("create table features (website varchar(140), ret_cnt smallint, rep smallint, ret smallint, num_people smallint, num_orgs smallint, num_locs smallint);")
        
    for row in tweet_set:
        cur.execute("insert into features (website, ret_cnt, rep, ret, num_people, num_orgs, num_locs) values (%s, %s, %s, %s, %s, %s, %s, %s)", (row["website"], row["ret_cnt"], row["label"], row["rep"], row["ret"], row["num_people"], row["num_orgs"], row["num_locs"]))

    os.chdir("../")
    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def store_initial_data(tbl_name):
    """populate SQL table 'tbl_name' with CSV 'train_test_set'"""
    con = mdb.connect(host="localhost", user="root", passwd="", db="twitter") 
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("drop table if exists {0};".format(tbl_name))
    cur.execute("create table {0} (tweet_id bigint, source_user_id bigint, rt_user_id bigint, tweet varchar(255), website varchar(140), tweet_time timestamp, raw_retweet_count bigint, I_c smallint);".format(tbl_name))

    with open("data/"+train_test_set, 'r') as csvfile:
        tweet_reader = csv.DictReader(csvfile, delimiter = '\t')
        tweet_reader.next()

        for row in tweet_reader:
            ic = row["I_c"]
            if ic == 'i':                  #informative is 1
                ic = 1                   
            elif ic == 'c':                #conversational is -1
                ic = -1
            else:
                continue
            cur.execute("insert into {0} (tweet_id, source_user_id, rt_user_id, tweet, website, tweet_time, raw_retweet_count, I_c) values (%s, %s, %s, %s, %s, %s, %s, %s)".format(tbl_name), (row["tweet_id"], row["source_user_id"], row["rt_user_id"], row["tweet"], row["website"], row["tweet_time"], row["raw_retweet_count"], ic))

    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def add_centrality_feature(tbl_name):
    con = mdb.connect(host="localhost", user="root", passwd="", db="twitter") 
    cur = con.cursor(mdb.cursors.DictCursor)
    
    cur.execute("alter table {0} add column eig_centrality float".format(tbl_name))
    cur.execute("update {0} id inner join users u on id.source_user_id = u.user_id set id.eig_centrality = u.eigenvector_centrality".format(tbl_name))
    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------            
def get_dict_corpus():
    """return and serialize dictionary and corpus from tweets"""
    con = mdb.connect(host="localhost", user="root", passwd="", db="twitter", charset='utf8') 
    cur = con.cursor(mdb.cursors.DictCursor)

    cur.execute("select tweet from init data")
    rows = cur.fetchall()
    tweets = list()
    for row in rows:
        tweets.append(row['tweet'].split())

    with open("data/stop_words.txt") as f:
        stop_words = np.array(f.read().splitlines())
        
    for tweet in tweets:
        for word in tweet:
            if word in stop_words:
                tweet.remove(word)

    dictionary = gs.corpora.Dictionary(tweets)
    dictionary.save("data/lda.dict")
    corpus = [dictionary.doc2bow(tweet) for tweet in tweets]
    gs.corpora.MmCorpus.serialize("data/lda-corpus.mm", corpus)

    return (dictionary, corpus)
#---------------------------------------------------------------------
#---------------------------------------------------------------------            


    return scores

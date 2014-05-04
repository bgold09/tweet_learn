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
DB_NAME = "twitter"
    
def classify(ml):
    """use a SVM to create a classifier where ml[0] is the feature matrix and ml[1] is the labels. c is the regularization parameter for the trade-off between the separating margin and the number of errors"""

    return svm.SVC(kernel='linear')
    
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------
def extract_features(tbl_name, a, b):
    """PRE:  java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/ner-eng-ie.crf-3-all2008-distsim.ser.gz -port 8080 -outputFormat inlineXML  --------- MUST BE RUNNING to get the Named-Entity data. 
             The other data comes from the SQL table init_data     
      POST: populate the NER columns in our dataset"""

    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
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
        rep = int(tweet[0].__contains__('@'))
        ret = int(tweet[0:2].__contains__('RT'))
        cent = row["eig_centrality"]
        if cent == None:
            continue
        
        li = [website, ret_cnt, rep, ret, num_people, num_orgs, num_locs, cent]
#        li = [rep, ret, ret_cnt]
        label = row["I_c"]

        labels.append(label)
        tweet_set.append(li)
    
    print "subset of features: ", tweet_set[:10]
    
    cur.close()
    con.close()
    return (np.array(tweet_set), np.array(labels))
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def store_features(tt_set, tbl_name):
    """create and populate a sql table 'tbl_name' of features 'tt_set'"""
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("drop table if exists {0};".format(tbl_name))
#    cur.execute("create table {0} (website varchar(140), ret_cnt smallint, rep smallint, ret smallint, num_people smallint, num_orgs smallint, num_locs smallint, eig_centrality float);".format(tbl_name))
    cur.execute("create table {0} (website varchar(140), rep smallint, eig_cent float, ner_count smallint, ret_cnt smallint);".format(tbl_name))
        
    for row in tt_set:
        cur.execute("insert into {0} (website, rep, eig_cent, ner_count, ret_cnt) values (%s, %s, %s, %s, %s)".format(tbl_name), (row[0], row[1], row[2], row[3], row[4]))

    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------
def store_initial_data(tbl_name):
    """populate SQL table 'tbl_name' with CSV 'train_test_set'"""
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
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
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
    cur = con.cursor(mdb.cursors.DictCursor)
    
    cur.execute("alter table {0} add column eig_centrality float".format(tbl_name))
    cur.execute("update {0} id inner join users u on id.source_user_id = u.user_id set id.eig_centrality = u.eigenvector_centrality".format(tbl_name))
    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------            
def sample_testing_data(tbl_name, size):
    """store the testing data into a SQL table 'tbl_name'"""
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("drop table if exists {0};".format(tbl_name))
    cur.execute("create table {0} (tweet_id bigint, source_user_id bigint, rt_user_id bigint, tweet varchar(255), website varchar(140), tweet_time timestamp, raw_retweet_count bigint);".format(tbl_name))

    qry = "insert into {0} (tweet_id, source_user_id, rt_user_id, tweet, website, tweet_time, raw_retweet_count) select tweet_id, source_user_id, rt_user_id, tweet, website, tweet_time, raw_retweet_count from tweets order by RAND() limit %s".format(tbl_name)

    cur.execute(qry, (size))
    con.commit()
    cur.close()
    con.close()
#---------------------------------------------------------------------
#---------------------------------------------------------------------            
def extract_features2(tbl_name, flag):
    """return a training and testing set of features"""
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME, charset='utf8') 
    cur = con.cursor(mdb.cursors.DictCursor)
    
    features = list()
    labels = list()
    tagger = ner.SocketNER(host='localhost', port=8080)
    cur.execute("select * from {0}".format(tbl_name))
    rows = cur.fetchall()
    for row in rows:
        tweet = row["tweet"]
        subfeatures = list()
        if tweet == "":
            continue
        if flag:
            di = tagger.get_entities(tweet)
            num_people = num_orgs = num_locs = 0
            
            if 'PERSON' in di:
                num_people = len(di['PERSON']) 
            if 'ORGANIZATION' in di:
                num_orgs = len(di['ORGANIZATION'])
            if 'LOCATION' in di:
                num_locs = len(di['LOCATION'])
            subfeatures.append([num_people, num_orgs, num_locs])

        website = row["website"]
        if website == '':
            website = 0
        else:
            website = 1
        if row['rt_user_id'] == -1:
            ret = -1
        else:
            ret = 1
        rep = int(tweet[0].__contains__('@'))
#        cent = row["eig_centrality"]
#        if cent == None:
#            continue
        feat_part = [website, rep]
        feat_part.extend(subfeatures)
        features.append(feat_part)
        labels.append(ret)

    print "subset of features: ", features[:10]

    cur.close()
    con.close()
    return (np.array(features), np.array(labels))

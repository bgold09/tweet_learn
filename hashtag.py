import numpy as np
import os
import csv
import string as st
import MySQLdb as mdb
import re

DB_NAME = "twitter"

def get_hashtags(conn):
    """Find all unique hashtags in testing data tweets (case-insensitive)."""
    all_hashtags = set()
    # anything starting with '#' is a hashtag
    r = re.compile(r"([#])(\w+)\b")

    # con = mdb.connect(host="localhost", user="brian", passwd="", db="twitter") 
    curs = conn.cursor()
    curs.execute("SELECT tweet FROM init_data")

    for row in curs.fetchall():
        # EACH row is a 1-tuple containing only the tweet text
        # matches are returned as tuples of the form ('#', 'hashtag text')
        hashtags = r.findall(row[0])   
        hashtags = frozenset([str.lower(x[1]) for x in hashtags])
        all_hashtags = all_hashtags.union(hashtags)
    
    return all_hashtags


def update_hashtag_schema(conn, hashtags):
    """Update the schema init data table with columns for each hashtag in hashtags."""
    curs = conn.cursor()
    curs.execute('SELECT COLUMN_NAME \
                  FROM INFORMATION_SCHEMA.COLUMNS \
                  WHERE TABLE_SCHEMA = "twitter" AND TABLE_NAME = "init_data" \
                    AND COLUMN_NAME LIKE "tag_%"')
    
    # get names of all columns already in the table
    columns = frozenset(curs.fetchall())
    
    # update the table schema
    for tag in hashtags:
        name = 'tag_' + tag
        if name not in columns:
            curs.execute('ALTER TABLE init_data ADD ' + name + ' VARCHAR(64) DEFAULT -1')


def add_ngram_features(data_tbl):
    """add 'size' features from the top 500 most frequently occuring ngrams"""
    con = mdb.connect(host="localhost", user="root", passwd="", db=DB_NAME) 
    cur = con.cursor(mdb.cursors.DictCursor)
     #populate a dictionary of 'size' ngrams
    features = list()
    ngram_feats = dict()
    cur.execute("select nGram from TopHundred")
    rows = cur.fetchall()
    for row in rows:
        ngram_feats[row['nGram']] = 0

#    print "len(ngram_feats):", len(ngram_feats)
    cur.execute("select * from {0}".format(data_tbl))
    rows = cur.fetchall()
    for row in rows:
        qry = "select n.nGram from TopHundred n inner join TopHundredNGrams tns on n.nGram = tns.nGram where tns.tweet_ids = %s"
        #get ngram intersection between tweet and top 'size' most frequent ngrams
        cur.execute(qry, (row['tweet_id']))
        ngs = cur.fetchall()
        for ng in ngs:
            ngram_feats[ng['nGram']] = 1          #set feature to true
            
        features.append(ngram_feats.values())
        for ng in ngs:
            ngram_feats[ng['nGram']] = 0          #reset for next feature
        
    return np.array(features)


import os
import csv
import string as st
import MySQLdb as mdb
import re

def hashtag_list():
    hashtags = ["start"]
    with open("tweetSubset.csv", 'rU') as csvfile:
        tweet_reader = csv.DictReader(csvfile, delimiter = ',', dialect=csv.excel)
        tweet_reader.next()

        for row in tweet_reader:
            tweet = row['tweet']
            start = 0
            while start < len(tweet) and tweet.find('#', start) != -1:
                hashIndex = tweet.find('#', start)
                i = hashIndex + 1
                while i < len(tweet) and st.punctuation.find(tweet[i]) == -1 and tweet[i] != ' ':
                    i += 1
                if hashtags.count(tweet[hashIndex:i]) == 0:
                    hashtags.append(tweet[hashIndex:i])
                start = i + 1
	hashtags.pop(0)
    return hashtags

def hashtag_count(hashtags):
	ht_count = ["start"]
	with open("tweetSubset.csv", 'rU') as csvfile:
		tweet_reader = csv.DictReader(csvfile, delimiter = ',', dialect=csv.excel)
		tweet_reader.next()

		for row in tweet_reader:
			tweet = row['tweet']
			htc = [tweet]
			for hashtag in hashtags:
				if tweet.find(hashtag) != -1:
					htc.append(1)
				else:
					htc.append(0)
			ht_count.append(htc)
	ht_count.pop(0)
	return ht_count  
                
# find all unique hashtags
def get_hashtags():
    all_hashtags = set()
    # anything starting with '#' is a hashtag
    r = re.compile(r"([#])(\w+)\b")

    con = mdb.connect(host="localhost", user="brian", passwd="", db="twitter") 
    curs = con.cursor()
    curs.execute("SELECT tweet FROM init_data")

    for row in curs.fetchall():
        # each row is a 1-tuple containing only the tweet text
        # matches are returned as tuples of the form ('#', 'hashtag text')
        hashtags = r.findall(row[0])   
        hashtags = set([str.lower(x[1]) for x in hashtags])
        all_hashtags = all_hashtags.union(hashtags)
    
    return all_hashtags


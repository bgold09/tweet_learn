import os
import csv
import string as st

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
                

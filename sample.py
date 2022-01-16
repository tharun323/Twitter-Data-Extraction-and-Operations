import tweepy
import time,sched
import urllib
import urllib3
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import tldextract
import collections
import json
import sys
from nltk.corpus import stopwords
import nltk
from collections import Counter
import threading
from nltk.tokenize import word_tokenize
from apscheduler.schedulers.blocking import BaseScheduler,BlockingScheduler
import pycron




#.....................User Credentials.....................
auth = tweepy.OAuthHandler('','')
auth.set_access_token('','')

api = tweepy.API(auth)

#.............Method used for finding URL -Python RegEX............
def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url
#Method Ends here

#.......................Twitter Api Stream Class and Respective Methods................
class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 5  # set your tweet limit Change as per requirement
        self.lst = list()
        self.domain = list()
        self.q = list()
        self.c = 0
        self.str = list()

    def on_status(self, status):
        self.counter += 1
        if self.counter < self.limit:
            self.q.append(status.user.name)
            self.q.append(status.user.statuses_count)
            print(status.text)
        else:
            myStream.disconnect()

    def on_data(self,data):
        self.counter += 1
        if self.counter < self.limit:
            all_data = json.loads(data)
            tweets = all_data["text"]
            self.str.append(tweets)
            user_name = all_data["user"]["screen_name"]  # get user handle
            stc = all_data["user"]["statuses_count"]  # gets status count
            print("username     |     status_count")
            print((user_name, stc))
            url = Find(tweets)
            for x in url:
                z = requests.get(x).url  # expanding of shortned links using requests library
                # print(z)
                self.lst.append(z)  # stores URL in a List for further processing
        if self.counter == self.limit:
            print("-----------BONUS 1:----------")

            self.c = 0
            for i in self.lst:
                self.c += 1
                ext = tldextract.extract(i)
                if ext.domain == 't':  # UNRESOLVED URLS
                    self.domain.append("unresolved")
                else:
                    self.domain.append(ext.domain)
            print("\n")
            print("Total Unique Domains sorted by count: ")
            counter = collections.Counter(self.domain)  # unique domains sorted by Count using collections container
            print(counter)
            print("\n")
            print("total links are :%d " % self.c)  # prints total number of links

            # print("your tweets text is ")
            # print("\n")
            # ..........METHOD FOR FILTERING USEFUL WORDS....
            string = '-'.join(self.str)
            sw = [

                'with', 'at', 'from', 'into', 'during', 'including', 'until', 'against', 'among', 'throughout',
                'despite', 'towards', 'upon', 'concerning', 'of', 'to', 'in', 'for', 'on', 'by', 'about', 'like',
                'through', 'over', 'before', 'between', 'after', 'since', 'without', 'under', 'within', 'along',
                'following', 'across', 'behind', 'beyond', 'plus', 'except', 'but', 'up', 'out', 'around', 'down',
                'off', 'above', '@', ',', '!', ',''', '.', ',', '"', '-', '+', '-', ')', '(', '&', '>', '<', '#',
                '%', '^', '&',
                '*', '[', ']', '{', '}', '?', '~', '`', 'a', 'an', 'the', 'have', 'has', 'had', 'may', 'might',
                'would', 'could',
                'should', 'ought', 'it', 'i', 'other', 'are', "aren't", 'so', 'all', 'who', 'you', 'me', 'she',
                'her', 'it',
                'they', 'them', 'us', 'there', 'your', 'was', 'that', 'and', 'is', 'not', 'why', 'what', 'whose',
                'no', 'yes'
                      'went', 'came', 'got', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'will', 'be',
                'again', 'doing', 'if',
                'because', 'but', 'soom', 'am', 'than', 'more', 'less', 'use', 'used', 'he', 'him', 'she', 'her',
                'every', 'body',
                'thing', 'free', 'we', 'just', 'been', 'or', 'RT', 'TAG', 'can'
            ]
            print("------BONUS 2:----------")
            querywords = string.split()
            resultwords = [word for word in querywords if word.lower() not in sw]
            print("\n")
            print("words after tokenization ")
            print(resultwords)
            # UNIQUE WORDS FIND USING SETS
            print("the number of unique words are : ")
            unique = set(resultwords)
            print(len(unique))
            print("\n")
            counts = Counter(resultwords)
            print("the top 10 words sorted by count are : ")
            # Prints 10 most common words sorted by count
            print(counts.most_common(10))
            print("--------------program ended----------")
            return True
            sys.exit()
# Authentication using Twitter Developer app credentials
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())#add timeout as argument to get tweets as per seconds
#Input from User

#print("------REPORT GENERATION-------")
p = input("Enter the keyword: ")
myStream.filter(track=[p])
print("---REPORT ENDED-----")



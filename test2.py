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
import codecs
import io




#.....................User Credentials.....................
auth = tweepy.OAuthHandler('2ov06JFjpl5Y94q9GPrKbhf4H','KGRDEe4dy0fYtLj6tAKhuD2ogCGVokVolnEljrqLrCt0sMzeME')
auth.set_access_token('1953615295-CRA8NdOxDVahS7vBHNlSZVjbFlq1KwGeE5rSvKi','1rfJNHYSyeQOuflCQtwQs7nEijzOzWGkv1bHR6kNBQ48v')

api = tweepy.API(auth) #access API



#.............Method used for finding URL -Python RegEX............
def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url
#Method Ends here


#<-------------------Tokenization of tweets-------------------->

def TweetsToken(string):
    print("----------------------------BONUS 2:-------------------------------------------")
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
        'thing', 'free', 'we', 'just', 'been', 'or', 'RT', 'TAG', 'can','&amp;','RT',':',''
    ]
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
    print("\n")
    print("the top 10 words sorted by count are : ")
    # Prints 10 most common words sorted by count
    print(counts.most_common(10))




#<------------Twitter Stream class start -------------------------->


class MyStreamListener(tweepy.StreamListener):
    #<------initializing variables --------------->
    def __init__(self, time_limit=50):#setting timelimit
        super(MyStreamListener, self).__init__()
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open('tweepy.json', 'a')
        self.saveFile.write("User_Handle    Status_count")
        self.tweets=list()
        self.ll=list()
        self.ld=list()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            all_data = json.loads(data)
            tweets = all_data["text"]
            user_name = all_data["user"]["screen_name"]  # get user handle
            status_count = all_data["user"]["statuses_count"]
            print(user_name, status_count)
            url = Find(tweets)
            for x in url:
                z = requests.get(x).url
                self.ll.append(z)
                ext = tldextract.extract(z).domain
                if ext == 't':
                    self.ld.append("unresolved")
                else:
                    self.ld.append(ext)
            global counter
            counter = collections.Counter(self.ld)
            # self.saveFile.write("\n List of unique domains after parsing links if available in tweet\n")
            #print("\n unique domains sorted: ")
            # self.saveFile.write("\n"+str(counter))
            #print(" " + s
            self.tweets.append(tweets)
            global string
            string= ''.join(self.tweets)

        else:
            print("-------BASE1 : ------------------------")
            print("all links obtained are : ")
            for i in self.ll:
                print(i)
            print("---------------------------")
            print("all domains sorted by count are : ")
            print(counter)
            print("----END OF BASE 1------")
            TweetsToken(string)
            print("------------REPORT ENDED--------------")
            #self.saveFile.close()
            return False

#<------------Twitter Stream class end ------------------------------------>


#<---------------run every 1 minute untill termination ------------->
while True:
    x = input("Enter the input :  ")
    myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener(time_limit=50))#timer
    myStream.filter(track=[x])
    time.sleep(60)

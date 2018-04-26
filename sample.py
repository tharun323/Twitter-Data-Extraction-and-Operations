import tweepy
import time
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

auth = tweepy.OAuthHandler('2ov06JFjpl5Y94q9GPrKbhf4H','KGRDEe4dy0fYtLj6tAKhuD2ogCGVokVolnEljrqLrCt0sMzeME')
auth.set_access_token('1953615295-CRA8NdOxDVahS7vBHNlSZVjbFlq1KwGeE5rSvKi','1rfJNHYSyeQOuflCQtwQs7nEijzOzWGkv1bHR6kNBQ48v')

api = tweepy.API(auth)

def Find(string):
    # findall() has been used
    # with valid conditions for urls in string
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url


class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 20  #set your tweet limit
        self.q=list()
        self.lst=list()
        self.domain=list()
        self.c=0
    def on_status(self, status):
        self.counter += 1
        if self.counter < self.limit:
            self.q.append(status.user.name)
            self.q.append(status.user.statuses_count)
            #print(status.text)
        else:
            myStream.disconnect()
    def on_data(self, raw_data):
        self.counter += 1
        if self.counter < self.limit:
            all_data = json.loads(raw_data)
            tweets = all_data["text"]
            user_name = all_data["user"]["screen_name"]
            stc=all_data["user"]["statuses_count"]
            print((user_name,stc))
            url=Find(tweets)
            for x in url:
                z=requests.get(x).url #expanding of shortned links using requests library
                print(z)
                self.lst.append(z)
        if self.counter==self.limit:
            self.c=0
            for i in self.lst:
                self.c+=1
                ext = tldextract.extract(i)
                if ext.domain=='t':
                    self.domain.append("unresolved")
                else:
                    self.domain.append(ext.domain)
            counter = collections.Counter(self.domain)#unique domains sorted by Count using collections container
            print(counter)
            print(self.c)#prints total number of links
            sys.exit()


    def on_error(self, status_code):
        print(status_code)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

p=input("Enter the keyword: ")
myStream.filter(track=[p])










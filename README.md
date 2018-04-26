# Twitter-Data-Extraction-and-Operations
# Twiter Data Operations - Pothi

## Used Tweepy and Twitter Streaming API

**Import the following packages**

**Use  pip to install the following packages**

`pip install tweepy`
`pip install tldextract`
`pip install collections`
`pip install json`
`pip install nltk`
`pip install bs4`

**Run the file using Pycharm or any other IDE of choice**
> Details of the Script

### BASE 1:

### Returns:

- List of username and status count  [ no of tweets to retrieve can be SET in the code `self.limit=x`

- Total number of unique Domains sorted by count , where links are extended using tldextract

- Total number of links in the tweets

### BASE 2:
### Returns:

- Total number of Unique Words

- Top 10 words sorted by count while ignoring "stop words - like common pronouns , articles etc "

- Task scheduler to schedule the script timer / CRONJOB for Linux can be used as well

### To Run Task Scheduler Every 5 Minutes
 insert the below link in the command prompt or use Windows Task Scheduler

`schtasks /create /sc minute /mo 5 /tn "TaskName" /tr \\scripts\YOUR_FILE_PATH`


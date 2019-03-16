import csv
import re
import matplotlib.pyplot as plt
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer

def RemoveNonAscii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def tweetCleanup(string): 

    cleaned = RemoveNonAscii(string)
    cleaned = cleaned.lower()

    cleaned = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', 
         cleaned)

    # Fix classic tweet lingo
    cleaned = re.sub(r'\bthats\b', 'that is', cleaned)
    cleaned = re.sub(r'\bive\b', 'i have', cleaned)
    cleaned = re.sub(r'\bim\b', 'i am', cleaned)
    cleaned = re.sub(r'\bya\b', 'yeah', cleaned)
    cleaned = re.sub(r'\bcant\b', 'can not', cleaned)
    cleaned = re.sub(r'\bwont\b', 'will not', cleaned)
    cleaned = re.sub(r'\bid\b', 'i would', cleaned)
    cleaned = re.sub(r'\bwth\b', 'what the hell', cleaned)
    cleaned = re.sub(r'\br\b', 'are', cleaned)
    cleaned = re.sub(r'\bu\b', 'you', cleaned)
    cleaned = re.sub(r'\bk\b', 'OK', cleaned)
    cleaned = re.sub(r'\bsux\b', 'sucks', cleaned)
    cleaned = re.sub(r'\bno+\b', 'no', cleaned)
    cleaned = re.sub(r'\bcoo+\b', 'cool', cleaned)
    
    return cleaned

allTweets = []

#Use the Naive Bayes Analyser instead of the default one
trainedTB = Blobber(analyzer=NaiveBayesAnalyzer())
fileName = "ethereum_ver2_29.csv"

with open(fileName, 'r',encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    reader.__next__()
    for row in reader:

        tweet= dict()
        tweet['date'] = row[0]
        tweet['rawtext'] = row[1]
        
        if re.match(r'^RT.*', tweet['rawtext']):
            continue

        tweet['cleaned'] = tweetCleanup(tweet['rawtext'])        
        tweet['TextBlob'] = trainedTB(tweet['cleaned'])        
       
        allTweets.append(tweet)

for tweet in allTweets:
   
    tweet['PScore'] = tweet['TextBlob'].sentiment.p_pos
    PScore = tweet['PScore']
    print(PScore, tweet['cleaned'] )
    if (PScore)  > 0.7:
        tweet['sentiment'] = 'Bullish'
    elif (PScore)  < 0.5:
        tweet['sentiment'] = 'Bearish'
    else:
        tweet['sentiment'] = 'neutral'

#tweets_sorted = sorted(allTweets, key=lambda k: k['sentiment'])   
tweets_sorted = sorted(allTweets, key=lambda k: k['PScore']) 

print ("\n\nTOP BEARISH TWEETS")
negative_tweets = [d for d in tweets_sorted if d['sentiment'] == 'Bearish']
for tweet in negative_tweets[:10]:
    print( tweet['TextBlob'].sentiment.p_pos, tweet['cleaned'])

print ("\n\nTOP BULLISH TWEETS")
positive_tweets = [d for d in tweets_sorted if d['sentiment'] == 'Bullish']
for tweet in positive_tweets[-10:]:
    print( tweet['TextBlob'].sentiment.p_pos, tweet['cleaned'])

print ("\n\nTOP NEUTRAL TWEETS")
neutral_tweets = [d for d in tweets_sorted if d['sentiment'] == 'neutral']
for tweet in neutral_tweets[0:10]:
    print( tweet['TextBlob'].sentiment.p_pos, tweet['cleaned'])


positive = len(positive_tweets)
neutral = len(negative_tweets)
negative = len(neutral_tweets)
print(fileName, ",", len(allTweets),",",positive,",",neutral,",",negative)
labels = 'Bullish', 'Neutral', 'Bearish'
sizes = [positive, neutral, negative]
print(sizes)
colors = ['yellowgreen', 'gold', 'lightcoral']
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')
plt.show()
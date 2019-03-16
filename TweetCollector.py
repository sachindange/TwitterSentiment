import tweepy
import sys
import csv

auth = tweepy.AppAuthHandler('sHkr3BZVGZ12PoHHwkLy5TC5i'
                , 'rGvT3xFeqOBYQSuIwptP61KlXPe41vwGRIrGITNnQ8bcULhwJC')

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("UNable to login, pls check keys !!")
    sys.exit(-1)

searchQuery = '#Ethereum -filter:retweets since:2018-06-29 until:2018-06-30'
fileName = 'ethereum_ver2_29.csv'   
maxTweets = 1000000 
tweetsPerQuery = 100  
max_id = -1000000

tweetCount = 0
print("Starting download max {0} tweets".format(maxTweets))

with open(fileName, 'a', newline='') as csvFileHandle:
    csvWriter = csv.writer(csvFileHandle)
    
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                new_tweets = api.search(q=searchQuery, count=tweetsPerQuery)
            else:
                new_tweets = api.search(q=searchQuery, count=tweetsPerQuery,
                                            max_id=str(max_id - 1))
            if not new_tweets:
                print("End of Tweets")
                break
            for tweet in new_tweets:
                csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
                print (tweet.created_at, tweet.text)
            tweetCount += len(new_tweets)
            print("Done Downloading {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print("Error while downloading : " + str(e))
            break
    
    print ("Done Downloading {0} tweets, Saved to {1}".format(tweetCount, fileName))

#csvFileHandle.close()

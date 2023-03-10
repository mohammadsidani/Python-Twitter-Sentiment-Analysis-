import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	
	def __init__(self):
		
		mykeys = open('twitterkeys.txt', 'r').read().splitlines()
		consumer_key = mykeys[0]
		consumer_secret = mykeys[1]
		access_token = mykeys[2]
		access_token_secret = mykeys[3]

		
		try:
			
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			
			self.auth.set_access_token(access_token, access_token_secret)
			
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		
		analysis = TextBlob(self.clean_tweet(tweet))
		
		if analysis.sentiment.polarity > 0.23:
			return 'positive'
		elif analysis.sentiment.polarity == 0.23:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		
		tweets = []

		try:
			
			fetched_tweets = self.api.search_tweets(q = query, count = count)

			
			for tweet in fetched_tweets:
				
				parsed_tweet = {}
				
				parsed_tweet['text'] = tweet.text
				
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				
				if tweet.retweet_count > 0:
					
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			
			return tweets

		except tweepy.TweepError as error:
			
			print("Error : " + str(error))

def main():
	
	api = TwitterClient()
	
	tweets = api.get_tweets(query = 'ChatGPT', count = 200)

	
	positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	print("Positive tweets percentage: {} %".format(100*len(positive_tweets)/len(tweets)))
	
	negative_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	print("Negative tweets percentage: {} %".format(100*len(negative_tweets)/len(tweets)))
	
	print("Neutral tweets percentage: {} % \
		".format(100*(len(tweets) -(len( negative_tweets )+len( positive_tweets)))/len(tweets)))

if __name__ == "__main__":
	
	main()

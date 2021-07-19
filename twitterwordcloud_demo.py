import wordcloud_wrapper
import tweepy_wrapper
import argparse

TWITTER_SECRETS_PATH = "./twitter"
INPUT_FOLDER = "./input"
OUTPUT_FOLDER = "./png"
SCREENNAME = "twitter"

def parse_args():
	global SCREENNAME
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--user", help = "The Twitter user's handle")

	args = parser.parse_args()
	if args.user:
		SCREENNAME = args.user

		print("Entered username is: " + args.user)

def tokenize_tweets(tweets):
	tokens = []
	for tweet in tweets:
		tokens.extend(tweet.split())
	return tokens

def main():

	parse_args()

	blacklist = set(["\n"]) #set([" <Media omitted>\n", "\n"])

	wc = wordcloud_wrapper.WordCloudWrapper(INPUT_FOLDER, OUTPUT_FOLDER, blacklist)
	tweepy = tweepy_wrapper.TweepyWrapper(TWITTER_SECRETS_PATH)
	user_model = None

	# Validate that the twitter user exists
	try:
		user_model = tweepy.get_api().get_user(screen_name = SCREENNAME)
	except:
		exit("FATAL: User " + SCREENNAME + " does not exist.")
	

	tweets = tweepy.get_user_timeline(id=SCREENNAME, tweet_mode="extended", include_rts=False, limit=10)
	tokens = tokenize_tweets(tweets)

	
	words, mentions = [], []
	for token in tokens:
		if not wc.is_word_valid(token):
			continue
		token = wc.removeWeirdChars(token)
		if token.startswith("@"):
			mentions += token,
		else:
			words += token,


	wc.generate_wordcloud(SCREENNAME , words)
	wc.generate_wordcloud(SCREENNAME + "_mentions", mentions)
		

if __name__ == "__main__":
	main()
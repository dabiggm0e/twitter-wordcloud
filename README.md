# twitter-wordcloud
A simple Python tool to analyze the word cloud of a specific twitter user timeline.

# Installation
* Install Tweepy python library

  `pip install tweepy`

* Install wordcloud python library

  `pip install wordcloud`

* Install Bidi

  `pip install python-bidi`

* Install Arabic Reshaper (Optional in case you will not deal with Arabic letters)

  `pip install --upgrade arabic-reshaper`

# Running
Run the program by passing the Twitter's handle of the account you are trying to generate the top words and top mentions wordcloud.

  `python twitterwordcloud_demo.py --user USERNAME`

If no --user argument was passed, then default value will be "twitter"
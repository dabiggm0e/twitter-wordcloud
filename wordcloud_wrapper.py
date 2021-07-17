from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
import re

class WordCloudWrapper:
    def __init__(this, INPUT_FOLDER, OUTPUT_FOLDER, blacklist=[]):
        this.OUTPUT_FOLDER = OUTPUT_FOLDER
        this.INPUT_FOLDER = INPUT_FOLDER
        this.blacklist = blacklist
        this.stopwords_path = INPUT_FOLDER + "/" + "stopwords.txt"
        this.stopwords = this.populate_stopwords()

    def populate_stopwords(this):
        stopwords = set()
        f = open(this.stopwords_path, "r")
        words = f.readlines()
        for word in words:
            stopwords.add(word.strip().lower())

        return stopwords.union(STOPWORDS)

    def is_word_valid(this, word):
        word = word.strip().lower()
        #TODO: refactor the blacklist check 
        if word in this.blacklist or word in this.stopwords or word.startswith("http") or word.startswith("www"):
            return False
        return True

    def generate_wordcloud(this, name, words,  bg_color="white", font="./fonts/Amiri-Bold.ttf", font_size=10, h=800, w=800):
        tokens = ' '.join(words)
        tokens = get_display(arabic_reshaper.reshape(tokens))
        wordcloud = WordCloud(width = w, height = h,
                    background_color =bg_color,
                    font_path= font,
                    stopwords = this.stopwords,
                    min_font_size = font_size).generate(tokens)

        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad = 0)
        plt.title(label=name,
            fontsize=40,
            color="green") 	  

        plt.savefig(this.OUTPUT_FOLDER + "/"   + name + ".png")	 

    def removeWeirdChars(this, text):
        weridPatterns = re.compile("["
                                u"\U0001F600-\U0001F64F"  # emoticons
                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                u"\U00002702-\U000027B0"
                                u"\U000024C2-\U0001F251"
                                u"\U0001f926-\U0001f937"
                                u'\U00010000-\U0010ffff'
                                u"\u200d"
                                u"\u2640-\u2642"
                                u"\u2600-\u2B55"
                                u"\u23cf"
                                u"\u23e9"
                                u"\u231a"
                                u"\u3030"
                                u"\ufe0f"
                                u"\u2069"
                                u"\u2066"
                                u"\u200c"
                                u"\u2068"
                                u"\u2067"
                                "]+", flags=re.UNICODE)
        return weridPatterns.sub(r' ', text)

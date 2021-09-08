import pandas as pd
import numpy as np
import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from google_play_scraper import Sort, reviews

from nltk.stem import WordNetLemmatizer
class AppReviewScraper:
    def __init__(self, app_id, n_reviews = 100):
        self.app_id = app_id
        self.n_reviews = n_reviews
        self.app_reviews_df = None
    def get_reviews(self):
        app_reviews = []
        scores = []
        helpfulCount = []
        dates = []
        results, _ = reviews(
            self.app_id,
            count = self.n_reviews
        )
        
        for r in results:
            app_reviews.append(r['content'])
            scores.append(r['score'])
            helpfulCount.append(r['thumbsUpCount'])
            dates.append(r['at'])
            
        self.app_reviews_df = pd.DataFrame({"reviews":app_reviews, "scores":scores, "helpfulCount":helpfulCount, "dates":dates})
        self.app_reviews_df['review_len'] = self.app_reviews_df['reviews'].apply(len)
        self.app_reviews_df['scores'] = self.app_reviews_df['scores'].apply(str)
        self.app_reviews_df['reviews'] = self.app_reviews_df['reviews'].apply(AppReviewScraper.remove_links)
        
    @staticmethod
    def remove_links(text):
        # Creating the corpus
        STOP_WORDS = stopwords.words()


        # Removing RT text in tweets since it won't be useful
        text = text.replace("RT","")

        text = re.sub(r'\d+', "", text)

        # Removing hyperlinks
        text = re.sub('http://\S+|https://\S+', '', text)

        # Removing emojis
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"
                            u"\U0001F680-\U0001F6FF"
                            u"\U0001F1E0-\U0001F1FF"
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        
        # Tokenize the text
        text_tokens = word_tokenize(text)

        # Itertating through the word and if a word is not in the stop words then adding it to the list
        tokens_without_sw = [word for word in text_tokens if not word in STOP_WORDS]
        
        filtered_sentence = (" ").join(tokens_without_sw)

        # Removing some common symbols
        text = re.sub(r'@\w+',  '', text).strip()
        text = re.sub("[^a-zA-Z0-9 ']", "", text)


        
        return text
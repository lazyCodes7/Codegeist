import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from app_store_scraper import AppStore
import re
class AppStoreReviewScraper:
    def __init__(self, app_name, country = 'us'):
        self.country = country
        
        self.app_name = app_name
        self.store_reviews_df = None
        
        
    def get_reviews(self):
            app_reviews = []
            scores = []
            dates = []
            
            results = AppStore(country = self.country, app_name=self.app_name)
            results.review(how_many=50)

            for r in results.reviews:
                app_reviews.append(r['review'])
                scores.append(r['rating'])
                dates.append(r['date'])

            self.store_reviews_df = pd.DataFrame({"reviews":app_reviews, "scores":scores, "dates":dates})
            self.store_reviews_df['review_len'] = self.store_reviews_df['reviews'].apply(len)
            self.store_reviews_df['scores'] = self.store_reviews_df['scores'].apply(str)
            self.store_reviews_df['reviews'] = self.store_reviews_df['reviews'].apply(AppStoreReviewScraper.remove_links)
            
    @staticmethod
    def remove_links(text):
        STOP_WORDS = stopwords.words('english')
        wnl = WordNetLemmatizer()
        # Creating the corpus
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

        # Removing some common symbols
        text = re.sub(r'@\w+',  '', text).strip()
        text = re.sub("[^a-zA-Z0-9 ']", "", text)

        # Using a lemmatizer to get a final text
        text=' '.join([wnl.lemmatize(i) for i in text.lower().split()])

        # Tokenize the text
        text_tokens = word_tokenize(text)

        # Itertating through the word and if a word is not in the stop words then adding it to the list
        tokens_without_sw = [word for word in text_tokens if not word in STOP_WORDS]

        # Getting the filtered sentence
        filtered_sentence = (" ").join(tokens_without_sw)
        text = filtered_sentence

        # Returning the transformed/filtered text

        return text
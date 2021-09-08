import requests
import json
import pandas as pd
import plotly.express as px
import plotly
import seaborn as sns
import matplotlib.pyplot as plt
import json
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from expertai.nlapi.cloud.client import ExpertAiClient
import os
class ReviewScraper:
    def __init__(self, key):
        self.reviews = []
        self.stars = []
        self.total_votes = 0
        self.helpful_votes = 0
        self.key = key
    def get_reviews(self):
        url = "https://marketplace.atlassian.com/rest/2/addons/"+self.key+"/reviews"
        print(url)

        headers = {
        "Accept": "application/json"
        }
        response = requests.request("GET",url,headers=headers)
        result = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
        result = json.loads(response.text)
        print(len(result['_embedded']['reviews']))
        for review_counter in range(len(result['_embedded']['reviews'])):
            self.reviews.append(result['_embedded']['reviews'][review_counter]['review'])
            self.stars.append(result['_embedded']['reviews'][review_counter]['stars'])
            self.total_votes+=result['_embedded']['reviews'][review_counter]['totalVotes']
            self.helpful_votes+=result['_embedded']['reviews'][review_counter]['helpfulVotes']

        reviews_df = pd.DataFrame({"reviews": self.reviews, "stars": self.stars})
        reviews_df['reviews'] = reviews_df['reviews'].apply(ReviewScraper.remove_links)
        
        return reviews_df

    @staticmethod
    def remove_links(text):
        # Creating the corpus
        STOP_WORDS = stopwords.words()

        # Initalizing the lemmatizer
        wnl = WordNetLemmatizer()

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

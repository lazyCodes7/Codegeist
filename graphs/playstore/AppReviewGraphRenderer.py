import pandas as pd
import numpy as np
from dotenv import load_dotenv
from collections import Counter
import plotly.express as px
import plotly.io as pio
from expertai.nlapi.cloud.client import ExpertAiClient
from dotenv import load_dotenv
load_dotenv() 
import os
os.environ["EAI_USERNAME"] = os.environ["EMAIL"]
os.environ["EAI_PASSWORD"] = os.environ["PASSWORD"]
class AppReviewGraphRenderer:
    def __init__(self, app_reviews_df):
        self.app_reviews_df = app_reviews_df
        self.client = ExpertAiClient()
    
    def drawRatingLinePlot(self):
        fig = px.line(
            self.app_reviews_df,
            x='dates',
            y='review_len',
            color='scores'
        )
        return pio.to_json(fig)
    
    def drawRatingHistogram(self):
        ratings_fig = px.histogram(self.app_reviews_df, x = 'scores', color = 'scores')
        return pio.to_json(ratings_fig)
        
    def drawBehavorialEmotionalChart(self):
        review_summation = ""
        taxonomy1 = 'emotional-traits'
        taxonomy2 = 'behavioral-traits'
        taxonomy3 = 'iptc'
        language = 'en'
        behavior_type = []
        detailed_behavior_type = []
        emotion_type = []
        detailed_emotion_type = []
        iptc_type = []

        for app_reviews in self.app_reviews_df['reviews']:
            a_r = " ".join(app_reviews.split(" ")[:20])
            review_summation += a_r
            review_summation += " "
        self.review_summation = review_summation
        
        output1 = self.client.classification(body={"document": {"text":self.review_summation}}, params={'taxonomy': taxonomy2, 'language': language})
        output2 = self.client.classification(body={"document": {"text":self.review_summation}}, params={'taxonomy': taxonomy1, 'language': language})
        output3 = self.client.classification(body={"document": {"text": self.review_summation[0:1500]}}, params={'taxonomy': taxonomy3, 'language': language})

        for category in output1.categories:
            behavior_type.append(category.hierarchy[0])
            detailed_behavior_type.append(category.hierarchy[2])
        
        
        for category in output2.categories:
            emotion_type.append(category.hierarchy[0])
            detailed_emotion_type.append(category.hierarchy[1])

        for category in output3.categories:
            for cat in category.hierarchy:
                iptc_type.append(cat)
            
        e_df = pd.DataFrame({"emotion_type": emotion_type, "detailed_emotion_type": detailed_emotion_type})
        b_df = pd.DataFrame({"detailed_behavioral_type": detailed_behavior_type, "behavioral_type": behavior_type })
        i_df = pd.DataFrame({"iptc_type": iptc_type })

        fig1 = px.bar(b_df, x = 'behavioral_type', color = 'detailed_behavioral_type')

        fig2 = px.bar(e_df, x = 'emotion_type', color = 'detailed_emotion_type')

        fig3 = px.bar(i_df, x = 'iptc_type', color = 'iptc_type')

        
        return (
            pio.to_json(fig1),
            pio.to_json(fig2),
            pio.to_json(fig3)
        )
        
        
        
    def drawTopKeywords(self):
        # Counting 10 most used words from the tweets
        cnt = Counter(" ".join(self.app_reviews_df['reviews']).split()).most_common(10)

        # Converting it to a DataFrame
        word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])

        # Plotting and converting to json
        wordfreq = px.histogram(word_frequency,x="Top Keywords",y="Frequency",color="Top Keywords")


        return pio.to_json(wordfreq)

    def reviews_split(self):
    	positive_reviews = []
    	negative_reviews = []
    	reviews = self.associate_reviews()
    	for review in reviews:
    	    result = self.client.specific_resource_analysis(body={"document": {"text": review}},params={'language': 'en', 'resource': 'sentiment'})
    	    if result.sentiment.overall > 0:
    	        positive_reviews.append(review)
    	    else:
                negative_reviews.append(review)
    	return sorted(positive_reviews),sorted(negative_reviews)

    def associate_reviews(self):
        reviews = self.app_reviews_df.reviews.tolist()
        unique_words = set(reviews)
        freq = {}
        for w in unique_words:
            freq[w] = reviews.count(w)
        sorted_freq = dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
        result = []
        for r in reviews:
            for word in sorted_freq.keys():
                if word in r and len(r) > 10:
                    r.replace('\n','')
                    result.append(r)
        return list(set(result))

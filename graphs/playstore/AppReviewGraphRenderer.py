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
        language = 'en'
        behavior_type = []
        detailed_behavior_type = []
        emotion_type = []
        detailed_emotion_type = []
        for app_reviews in self.app_reviews_df['reviews']:
            review_summation+=app_reviews
            review_summation+=" "
        self.review_summation = review_summation
        
        output1 = self.client.classification(body={"document": {"text":self.review_summation}}, params={'taxonomy': taxonomy2, 'language': language})
        output2 = self.client.classification(body={"document": {"text":self.review_summation}}, params={'taxonomy': taxonomy1, 'language': language})
        for category in output1.categories:
            behavior_type.append(category.hierarchy[0])
            detailed_behavior_type.append(category.hierarchy[2])
        
        
        for category in output2.categories:
            emotion_type.append(category.hierarchy[0])
            detailed_emotion_type.append(category.hierarchy[1])
            
        e_df = pd.DataFrame({"emotion_type": emotion_type, "detailed_emotion_type": detailed_emotion_type})
        b_df = pd.DataFrame({"detailed_behavioral_type": detailed_behavior_type, "behavioral_type": behavior_type })
        
        fig1 = px.bar(b_df, x = 'behavioral_type', color = 'detailed_behavioral_type')

        fig2 = px.bar(e_df, x = 'emotion_type', color = 'detailed_emotion_type')
        
        return (
            pio.to_json(fig1),
            pio.to_json(fig2)
        )
        
        
        
    def drawTopKeywords(self):
        # Counting 10 most used words from the tweets
        cnt = Counter(" ".join(self.app_reviews_df['reviews']).split()).most_common(10)

        # Converting it to a DataFrame
        word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])

        # Plotting and converting to json
        wordfreq = px.histogram(word_frequency,x="Top Keywords",y="Frequency",color="Top Keywords")


        return pio.to_json(wordfreq)
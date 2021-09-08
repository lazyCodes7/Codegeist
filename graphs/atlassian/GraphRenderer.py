import os
from expertai.nlapi.cloud.client import ExpertAiClient
import plotly.express as px
import plotly
import plotly.graph_objects as go
import numpy as  np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from dotenv import load_dotenv
import plotly.io as pio
import json
load_dotenv() 
# Setting up the access keys from the .env file
os.environ["EAI_USERNAME"] = os.environ["EMAIL"]
os.environ["EAI_PASSWORD"] = os.environ["PASSWORD"]
class GraphRenderer:
    def __init__(self, reviews):
        self.reviews = reviews
        self.client = ExpertAiClient()
        self.language = 'en'


    def drawTopKeywords(self):
        # Counting 10 most used words from the tweets
        cnt = Counter(" ".join(self.reviews['reviews']).split()).most_common(10)

        # Converting it to a DataFrame
        word_frequency = pd.DataFrame(cnt, columns=['Top Keywords', 'Frequency'])

        data = [
            go.Bar(
                x = word_frequency["Top Keywords"],
                y = word_frequency["Frequency"]
            )
        ]

        # Plotting and converting to json
        wordfreq = go.Figure(data = data)
        return pio.to_json(wordfreq)

    @staticmethod
    def cleanTraitRate(text):
        rating_text = text.split(" ")[1]
        return rating_text
    @staticmethod
    def getUserTraits(df,client,language):
        # Instantiate the client
        ## Setting up the password to access the expert.ai API
        taxonomy = 'emotional-traits'
        text = ""
        taxonomy_b = 'behavioral-traits'
        user_review_list = []
        emotional_traits = []
        big_5_traits = []
        big_5_trait_rate = []
        final_traits = []

        # Going through the review headers and reviews itself
        try:
            for review in df['reviews']:
                text+=review
                # Getting the emotions and behavorial traits
            output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
            output_b = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy_b, 'language': language})
            for category in output_b.categories:
                print(category.hierarchy)
                big_5_traits.append(category.hierarchy[0])
                big_5_trait_rate.append(category.hierarchy[1])
                final_traits.append(category.hierarchy[2])
            for category in output.categories:
                emotional_traits.append(category.hierarchy[1])
            
            # Saving the traits as found into a dict
            e_dict = {
                "emotional_traits" : emotional_traits
            }
            b_dict = {
                "big_5_traits":big_5_traits,
                "big_5_trait_rate" : big_5_trait_rate,
                "final_traits" : final_traits
            
            }

            # Converting it into a dataframe
            b_df = pd.DataFrame(b_dict)
            b_df['big_5_trait_rate'] = b_df['big_5_trait_rate'].apply(GraphRenderer.cleanTraitRate)

            # Returning the dataframe
            reviews_df = pd.DataFrame(e_dict)
        except Exception as e:
            print(e)

            # Except block if reviews for a company were not found. Then going with a default overview
            emotional_traits = ['Repulsion','Hatred','Happiness','Excitement','Love','Happiness','Excitement']
            big_5_traits = ['Sociality', 'Sociality']
            big_5_trait_rate = ['Sociality low', 'Sociality fair']
            final_traits = ['Asociality', 'Seriousness']
            e_dict = {
                "emotional_traits" : emotional_traits
            }


            b_dict = {
                "big_5_traits":big_5_traits,
                "big_5_trait_rate" : big_5_trait_rate,
                "final_traits" : final_traits
            
            }
            reviews_df = pd.DataFrame(e_dict)
            b_df = pd.DataFrame(b_dict)

            # Return the default dataframe with some sample data
        return (reviews_df,b_df)

    def drawBehavorialEmotionalChart(self):
        # Getting the emotional traits and big 5 traits from the function
        emotional_traits, big5_traits = GraphRenderer.getUserTraits(self.reviews, self.client, self.language)
        # Drawing a Pie Chart for getting the big 5 traits
        big_traits_class, big_traits_count = np.unique(big5_traits.final_traits,return_counts=True)
        big5_traits_graph = go.Figure(data = [go.Pie(labels=big_traits_class,values=big_traits_count,hole=.6,hovertemplate = 'final_traits=%{label}<extra></extra>'+'<br>Percentage=%{percent}',textinfo='label')])
        big5_traits_graph.update_layout(title='Big5 Traits found')
        # Bar Plot for getting the big 5 traits along with a measure of how prevalent each trait is
        big5_traits_val_graph = px.bar(big5_traits, x='big_5_traits', color='big_5_trait_rate',color_discrete_sequence=px.colors.qualitative.Pastel)
        # Drawing the figure for emotional traits
        emotional_traits_class, emotional_traits_count = np.unique(emotional_traits.emotional_traits,return_counts=True)
        emotional_traits_graph = go.Figure(data = [go.Pie(labels=emotional_traits_class,values=emotional_traits_class,hole=.6,hovertemplate = 'emotional_traits=%{label}<extra></extra>'+'<br>Percentage=%{percent}',textinfo='label')])
        emotional_traits_graph.update_layout(title='Emotional Traits found')


        return (
            pio.to_json(big5_traits_graph),
            pio.to_json(big5_traits_val_graph),
            pio.to_json(emotional_traits_graph)
        )

    def starDistribution(self):
    	star , star_counts = np.unique(self.reviews.stars,return_counts = True)
    	star_dist = go.Figure(data = [go.Pie(labels=star,values=star_counts,hole=.6,hovertemplate = 'stars=%{label}<extra></extra>'+'<br>Percentage=%{percent}',textinfo='label')])
    	star_dist.update_layout(title='Distribution of review stars')
    	star_dist.update_traces(hoverinfo='label')
    	return pio.to_json(star_dist)

    def reviews_split(self):
    	positive_reviews = []
    	negative_reviews = []
    	reviews = self.reviews.reviews.tolist()
    	for review in reviews:
    	    result = self.client.specific_resource_analysis(body={"document": {"text": review}},params={'language': self.language, 'resource': 'sentiment'})
    	    if result.sentiment.overall > 0:
    	        positive_reviews.append(review)
    	    else:
                negative_reviews.append(review)
    	return sorted(positive_reviews),sorted(negative_reviews)

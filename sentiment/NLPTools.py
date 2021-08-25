from sklearn.feature_extraction.text import CountVectorizer
from expertai.nlapi.cloud.client import ExpertAiClient
from sklearn.naive_bayes import ComplementNB
import pickle
import joblib
import nltk
import os
class NLPTools:
    def __init__(self,username, password, model_path="sentiment/model.pkl", vector_path="sentiment/vectorizer.pkl"):
        self.model = loaded_model = pickle.load(open(model_path, 'rb'))
        self.vectorizer = joblib.load(vector_path)
        self.username = username
        self.password = password

    def predictSentiment(self,text):
        output_vector = self.vectorizer.transform([text])
        pred = self.model.predict(output_vector)

        return pred

    def predictEmotionalTraits(self, text):
        os.environ["EAI_USERNAME"] = self.username
        os.environ["EAI_PASSWORD"] = self.password

        print(os.environ["EAI_USERNAME"])
        print(os.environ["EAI_PASSWORD"])

        client = ExpertAiClient()
        taxonomy='emotional-traits'
        language='en'
        emotional_traits = []

        output = client.classification(body={"document": {"text": text}}, params={'taxonomy': taxonomy, 'language': language})
        for category in output.categories:
            emotional_traits.append(category.hierarchy[1])

        # Saving as a dict
        emotional_traits_dict = {"emotional_traits":emotional_traits}


        return emotional_traits_dict

    def predictBehavior(self, text):
        os.environ["EAI_USERNAME"] = self.username
        os.environ["EAI_PASSWORD"] = self.password

        client = ExpertAiClient()
        taxonomy='behavioral-traits'
        language='en'
        big_5_traits = []
        big_5_trait_rate = []
        final_traits = []
        output = client.classification(
            body={"document": {"text": text}}, 
            params={'taxonomy': taxonomy, 'language': language}
        )
        for category in output.categories:
            big_5_traits.append(category.hierarchy[0])
            big_5_trait_rate.append(category.hierarchy[1])
            final_traits.append(category.hierarchy[2])

        b_dict = {
        "big_5_traits":big_5_traits,
        "big_5_trait_rate" : big_5_trait_rate,
        "final_traits" : final_traits
    
        }
        
        return b_dict

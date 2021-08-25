from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
import werkzeug
from sentiment.NLPTools import NLPTools
from graphs.GraphRenderer import GraphRenderer
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('text')
tools = NLPTools(username=os.environ['EMAIL'], password=os.environ['PASSWORD'])
class PredictSentiment(Resource):
    
    def get(self):
        
        try:
            args = parser.parse_args()
            user_query = args['text']

            sentiment = tools.predictSentiment(user_query)

            print(sentiment)

            if(sentiment == 1):
                return {"sentiment": "Positive"}


            else:
                return {"sentiment": "Negative"}
        except Exception as e:
            return {"exception" : repr(e)}
        

class PredictTraits(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            user_query = args['text']
            emotional_traits_dict = tools.predictEmotionalTraits(user_query)
            big_5_traits_dict = tools.predictBehavior(user_query)
            renderer = GraphRenderer(emotional_traits_dict, big_5_traits_dict)

            renderer.big5_traits = renderer.big5_traits.apply(renderer.cleanTraitRate)

            emotional_traits_graph, big5_traits_graph, big5_traits_val_graph = renderer.drawBehavorialEmotionalChart()

            return {
                "big5_traits_graph": big5_traits_graph,
                "big5_traits_val_graph": big5_traits_val_graph,
                "emotional_traits_graph": emotional_traits_graph
            }
        except Exception as e:
            print(e)
            return {"exception": repr(e)}
        





        

api.add_resource(PredictSentiment, '/sentiment')
api.add_resource(PredictTraits, '/graphs')

        
if __name__ == '__main__':
    app.run(debug=True)


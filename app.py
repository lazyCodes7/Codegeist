from graphs.GraphRenderer import GraphRenderer
from scraper.ReviewScraper import ReviewScraper
from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
from flask_restful import reqparse, abort, Api, Resource
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
load_dotenv()
import json

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('key')


class SendGraphs(Resource):
    @cross_origin()
    def get(self):
        try:
            args = parser.parse_args()
            user_query = args['key']

            scraper = ReviewScraper(key = user_query)
            reviews = scraper.get_reviews()
            renderer = GraphRenderer(reviews = reviews)

            big5_traits_graph, big5_traits_val_graph, emotional_traits_graph = renderer.drawBehavorialEmotionalChart()

            top_keywords = renderer.drawTopKeywords()

            star_dist = renderer.starDistribution()

            return {
                "big5_traits_graph": big5_traits_graph,
                "big5_traits_val_graph" : big5_traits_val_graph,
                "emotional_traits_graph" : emotional_traits_graph,
                "star_dist" : star_dist,
                "top_keywords" : top_keywords
            }
        except Exception as e:
            return {"exception" : repr(e)}
api.add_resource(SendGraphs, '/graphs')

        
if __name__ == '__main__':
    app.run(debug=True)

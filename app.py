from graphs.atlassian.GraphRenderer import GraphRenderer
from scraper.atlassian.ReviewScraper import ReviewScraper
from flask import Flask, render_template, send_file, make_response, url_for, Response,request,redirect
from flask_restful import reqparse, abort, Api, Resource
from scraper.playstore.AppReviewScraper import AppReviewScraper
from graphs.playstore.AppReviewGraphRenderer import AppReviewGraphRenderer
import os
from dotenv import load_dotenv
from flask_cors import CORS, cross_origin
from scraper.appstore.AppStoreReviewScraper import AppStoreReviewScraper
load_dotenv()
import json

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('appname')
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

            positive_reviews, negative_reviews = renderer.reviews_split()

            return {
                "big5_traits_graph": big5_traits_graph,
                "big5_traits_val_graph" : big5_traits_val_graph,
                "emotional_traits_graph" : emotional_traits_graph,
                "star_dist" : star_dist,
                "top_keywords" : top_keywords,
                "positive_reviews" : positive_reviews,
                "negative_reviews" : negative_reviews
            }
        except Exception as e:
            return {"exception" : repr(e)}
class SendAppReviewGraphs(Resource):
    @cross_origin()
    def get(self):
        try:
            args = parser.parse_args()
            user_query = args['key']
            scraper = AppReviewScraper(app_id = user_query)
            scraper.get_reviews()
            renderer = AppReviewGraphRenderer(scraper.app_reviews_df)
            
            emotional_chart, behavorial_chart = renderer.drawBehavorialEmotionalChart()
            top_keywords_chart = renderer.drawTopKeywords()
            rating_bar_chart = renderer.drawRatingHistogram()
            rating_line_chart = renderer.drawRatingLinePlot()

            return {
                "emotional_chart" : emotional_chart,
                "behavorial_chart" : behavorial_chart,
                "top_keywords_chart" : top_keywords_chart,
                "rating_bar_chart" : rating_bar_chart,
                "rating_line_chart" : rating_line_chart
            }
        except Exception as e:
            return {"exception": repr(e)}
        
class SendAppStoreGraphs(Resource):
    def get(self):
        try:
            args = parser.parse_args()
            user_query = args['key']
            scraper = AppStoreReviewScraper(app_name = user_query)
            scraper.get_reviews()
            renderer = AppReviewGraphRenderer(scraper.store_reviews_df)

            emotional_chart, behavorial_chart = renderer.drawBehavorialEmotionalChart()
            top_keywords_chart = renderer.drawTopKeywords()
            rating_bar_chart = renderer.drawRatingHistogram()
            rating_line_chart = renderer.drawRatingLinePlot()

            return {
                "emotional_chart" : emotional_chart,
                "behavorial_chart" : behavorial_chart,
                "top_keywords_chart" : top_keywords_chart,
                "rating_bar_chart" : rating_bar_chart,
                "rating_line_chart" : rating_line_chart
            }
        except Exception as e:
            return {"exception": repr(e)}  

api.add_resource(SendGraphs, '/atlassian')
api.add_resource(SendAppReviewGraphs, '/playstore')
api.add_resource(SendAppStoreGraphs, '/appstore')

        
if __name__ == '__main__':
    app.run(debug=True)

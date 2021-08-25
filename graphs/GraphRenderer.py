import plotly.express as px
import plotly
import pandas as pd
import plotly.io as pio
class GraphRenderer:
    def __init__(self, emotional_traits_dict, big5_traits_dict):
        self.big5_traits = pd.DataFrame(big5_traits_dict)
        self.emotional_traits = pd.DataFrame(emotional_traits_dict)
    def drawBehavorialEmotionalChart(self):

        # Drawing a Pie Chart for getting the big 5 traits
        big5_traits_graph = px.pie(self.big5_traits, names='final_traits',hole=.6,width=500,height=600)
        
        # Bar Plot for getting the big 5 traits along with a measure of how prevalent each trait is
        big5_traits_val_graph = px.bar(
            self.big5_traits, x='big_5_traits',
            color= 'big_5_trait_rate',
            width=500,
            height=600,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        emotional_traits_graph = px.pie(
            self.emotional_traits, 
            names='emotional_traits',
            hole=.6,
            width=500,
            height=600
        )

        return (
            pio.to_html(emotional_traits_graph), 
            pio.to_html(big5_traits_graph), 
            pio.to_html(big5_traits_val_graph)
        )
    def cleanTraitRate(self, text):
            rating_text = text.split(" ")[1]
            return rating_text


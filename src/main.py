from dataParser import parseData
from rec_algorithm import Recommender
from Gui import run_gui
import pandas as pd

# Read and parse datasets
songs = parseData()

# Prepare the model
features = ["song_popularity", "duration", "explicit", "danceability", "energy", "key", "mode", "loudness", "speechiness",
                    "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
recommender = Recommender(songs, features, 10)

#print(recommender.recommend("Will Anything Happen"))

# Run gui
run_gui(recommender)




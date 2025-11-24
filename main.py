from dataParser import parseData
from rec_algorithm import prep_rec_model, recommend
import pandas as pd

songs = parseData()


model, scaler, features, rec_amount = prep_rec_model(songs)
print(recommend("Will Anything Happen", songs, model, scaler, features, rec_amount))

#pd.set_option('display.max_columns', None)
#print(songs.head(10))
#for c in songs.columns:
#    print(songs[c].isna().sum(), c)



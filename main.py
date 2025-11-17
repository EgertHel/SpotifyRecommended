from dataParser import parseData
import pandas as pd

songs = parseData()

pd.set_option('display.max_columns', None)
print(songs.head(10))
for c in songs.columns:
    print(songs[c].isna().sum(), c)

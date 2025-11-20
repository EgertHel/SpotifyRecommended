import pandas as pd
import numpy as np
import ast
import os

def read_data():
    # Read Song data from 1st dataset
    songs1 = pd.read_csv("./data/rawData/tracks.csv", encoding="utf-8")
    songs1 = songs1.rename(columns = {"id": "song_id",
                            "name": "song_name",
                            "popularity": "song_popularity",
                            "duration_ms": "duration",
                            "explicit": "explicit",
                            "artists": "artists",
                            "id_artists": "artist_id",
                            "release_date": "release_date",
                            "danceability": "danceability",
                            "energy": "energy",
                            "key": "key",
                            "loudness": "loudness",
                            "mode": "mode",
                            "speechiness": "speechiness",
                            "acousticness": "acousticness",
                            "instrumentalness": "instrumentalness",
                            "liveness": "liveness",
                            "valence": "valence",
                            "tempo": "tempo",
                            "time_signature": "time_signature"})
    
    # Get and merge artist popularity into 1st songs songs
    # Read artists data for 1st dataset
    artists1 = pd.read_csv("./data/rawData/artists.csv", encoding="utf-8")
    artists1 = artists1.rename(columns = {"id": "artist_id", "popularity": "artist_popularity"})

    # Convert stringified list into mergeable form
    songs1["artist_id"] = songs1["artist_id"].apply(
        lambda str_list: ast.literal_eval(str_list) if pd.notnull(str_list) else []
    )
    songs1 = songs1.explode("artist_id")

    # Merge artists popularity with songs songs
    songs1 = songs1.merge(artists1[["artist_id", "artist_popularity"]], on="artist_id", how="left")
    agg_dict = {col: "first" for col in songs1.columns if col != "artist_popularity"}
    agg_dict["artist_popularity"] = lambda popularities: list(popularities.dropna())
    songs1 = songs1.groupby(["song_id"], as_index=False).agg(agg_dict)
    

    # Read Song data from 2nd dataset
    songs2 = pd.read_csv("./data/rawData/playlist_2010to2023.csv", encoding="latin1")
    songs2 = songs2.rename(columns = {"track_id": "song_id",
                            "track_name": "song_name",
                            "track_popularity": "song_popularity",
                            "duration_ms": "duration",
                            "artist_name": "artists",
                            "artist_id": "artist_id",
                            "year": "release_year",
                            "danceability": "danceability",
                            "energy": "energy",
                            "key": "key",
                            "loudness": "loudness",
                            "mode": "mode",
                            "speechiness": "speechiness",
                            "acousticness": "acousticness",
                            "instrumentalness": "instrumentalness",
                            "liveness": "liveness",
                            "valence": "valence",
                            "tempo": "tempo",
                            "time_signature": "time_signature",
                            "artist_popularity": "artist_popularity",
                            "artist_genres": "artist_genres",
                            "album": "album",
                            "playlist_url": "playlist_url"})
    
    songs2["artist_popularity"] = songs2["artist_popularity"].apply(lambda popularity: [popularity])


    songs = pd.concat([songs1, songs2])

    return songs


def clean_data(songs: pd.DataFrame) -> pd.DataFrame:
    songs["release_year"] = songs["release_date"].str[:4].astype(float)

    songs = songs.drop(columns=["playlist_url", "album", "release_date", "artist_popularity", "artist_genres"], axis="columns")

    obj_cols = songs.select_dtypes(include="object").columns
    songs[obj_cols] = songs[obj_cols].apply(lambda col: col.str.strip())

    songs = songs.drop_duplicates()
    songs.dropna(subset = ["song_name"], inplace=True)
    songs["explicit"] = songs["explicit"].fillna(0.0)

    return songs


def parseData():
    # Check if data has already been parsed
    if os.path.exists("./data/merged_data.pkl"):
        songs = pd.read_pickle("./data/merged_data.pkl")
        return songs
    
    songs = read_data()
    songs = clean_data(songs)

    songs.to_pickle("./data/merged_data.pkl")

    

    return songs
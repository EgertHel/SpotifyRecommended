from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

def prep_rec_model(songs):
    # Select features for KNN
    features = ["song_popularity", "duration", "explicit", "danceability", "energy", "key", "mode", "loudness", "speechiness",
                "acousticness", "instrumentalness", "liveness", "valence", "tempo", "time_signature"]
    
    songs_KNN = songs[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(songs_KNN)

    rec_amount = 10
    KNN = NearestNeighbors(n_neighbors=rec_amount + 1, metric="euclidean")
    KNN.fit(X_scaled)

    return KNN, scaler, features, rec_amount


def recommend(song_name, songs, model, scaler, features, rec_amount):
    song = songs[songs["song_name"] == song_name]

    if len(song) == 0:
        print("Could not find the song")
        return
    
    song_features = song[features]
    song_scaled = scaler.transform(song_features)

    distances, indices = model.kneighbors(song_scaled, n_neighbors=rec_amount + 1)

    rec_indices = indices[0][1:]

    return songs[["song_id", "song_name"]].iloc[rec_indices]


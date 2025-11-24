from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

class Recommender:
    def __init__(self, songs, features, rec_amount):
        self.songs = songs
        self.features = features
        self.rec_amount = rec_amount
        
        songs_KNN = songs[features]

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(songs_KNN)

        self.model = NearestNeighbors(n_neighbors=self.rec_amount + 1, metric="euclidean")
        self.model.fit(X_scaled)


    def recommend(self, song_name):
        song = self.songs[self.songs["song_name"] == song_name]

        if len(song) == 0:
            print("Could not find the song")
            return
        
        song_features = song[self.features]
        song_scaled = self.scaler.transform(song_features)

        distances, indices = self.model.kneighbors(song_scaled, n_neighbors=self.rec_amount + 1)

        rec_indices = indices[0][1:]

        return self.songs[["song_id", "song_name"]].iloc[rec_indices]


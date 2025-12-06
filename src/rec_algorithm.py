from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans

class Recommender:
    def __init__(self, songs, features, rec_amount):
        self.songs = songs
        self.features = features
        self.rec_amount = rec_amount
        
        songs_KNN = songs[features]

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(songs_KNN)

        clusters_n = 20
        self.kmeans = KMeans(n_clusters=clusters_n)
        self.songs["cluster"] = self.kmeans.fit_predict(X_scaled)

        self.models = {}
        for i in range(clusters_n):
            cluster = X_scaled[self.songs["cluster"] == i]
            knn = NearestNeighbors(n_neighbors=self.rec_amount + 1, metric="euclidean")
            knn.fit(cluster)
            self.models[i] = knn

        #self.model = NearestNeighbors(n_neighbors=self.rec_amount + 1, metric="euclidean")
        #self.model.fit(X_scaled)


    def recommend(self, song_name):
        song = self.songs[self.songs["song_name"] == song_name]

        if len(song) == 0:
            print("Could not find the song")
            return
        
        song_features = song[self.features]
        song_scaled = self.scaler.transform(song_features)

        cluster = self.kmeans.predict(song_scaled)[0]
        songs_in_cluster = self.songs["cluster"] == cluster

        cluster_indices = self.songs.index[songs_in_cluster]
        model = self.models[cluster]

        distances, indices = model.kneighbors(song_scaled, n_neighbors=self.rec_amount + 1)

        rec_indices = cluster_indices[indices[0][1:]]

        return self.songs[["song_id", "song_name", "cluster", "artists"]].iloc[rec_indices]


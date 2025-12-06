from sklearn.decomposition import PCA
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

        self.pca = PCA(n_components=2)
        self.songs["pca_x"], self.songs["pca_y"] = self.pca.fit_transform(X_scaled).T

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

    def initialize_plot(self, ax, canvas):
        ax.clear()
        sample = self.songs.sample(400)  # show subset for readability

        ax.scatter(sample["pca_x"], sample["pca_y"], s=8, alpha=0.3, label="All songs")
        ax.set_title("Song Space (PCA)")
        ax.set_xlabel("PCA 1")
        ax.set_ylabel("PCA 2")

        canvas.draw()

    def update_plot(self, song_name, rec_ids, ax, canvas):
        ax.clear()

        # Background songs
        sample = self.songs.sample(400)
        ax.scatter(sample["pca_x"], sample["pca_y"], s=8, alpha=0.25, color="gray")

        # Input song
        input_song = self.songs[self.songs["song_name"] == song_name]
        ax.scatter(input_song["pca_x"], input_song["pca_y"],
                   color="red", s=150, marker="*", label="Input Song")

        # Recommended songs
        rec_songs = self.songs[self.songs["song_id"].isin(rec_ids)]
        ax.scatter(rec_songs["pca_x"], rec_songs["pca_y"],
                   color="blue", s=50, label="Recommended Songs")

        # Connect lines
        for _, r in rec_songs.iterrows():
            ax.plot([input_song["pca_x"].iloc[0], r["pca_x"]],
                    [input_song["pca_y"].iloc[0], r["pca_y"]],
                    alpha=0.4)

        ax.set_title("Recommended Songs in PCA Space")
        ax.legend()

        canvas.draw()

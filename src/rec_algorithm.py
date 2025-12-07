from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
import pandas as pd

class Recommender:
    def __init__(self, songs, features, rec_amount):
        self.songs = songs
        self.features = features
        self.rec_amount = rec_amount
        
        songs_KNN = songs[features]

        self.scaler = StandardScaler()
        self.X_scaled = pd.DataFrame(self.scaler.fit_transform(songs_KNN), index=self.songs.index, columns=self.features)

        clusters_n = 20
        self.kmeans = KMeans(n_clusters=clusters_n, random_state=42)
        self.songs["cluster"] = self.kmeans.fit_predict(self.X_scaled)

        self.models = {}
        self.cluster_indices = {}
        for i in range(clusters_n):
            idx = self.songs[self.songs["cluster"] == i].index
            cluster_df = self.X_scaled.loc[idx]
            knn = NearestNeighbors(n_neighbors=self.rec_amount + 1, metric="euclidean")
            knn.fit(cluster_df.values)
            self.models[i] = knn
            self.cluster_indices[i] = idx.to_list()

        self.pca = PCA(n_components=2)
        self.songs["pca_x"], self.songs["pca_y"] = self.pca.fit_transform(self.X_scaled).T

    def recommend(self, song_id):
        song = self.songs[self.songs["song_id"] == song_id]

        if len(song) == 0:
            print("Could not find the song")
            return
        
        song_idx = song.index[0]
        song_scaled = self.X_scaled.loc[[song_idx]].values

        cluster = song["cluster"].iloc[0]
        model = self.models[cluster]
        cluster_idxs = self.cluster_indices[cluster]

        distances, indices = model.kneighbors(song_scaled, n_neighbors=self.rec_amount + 1)

        rec_songs = indices[0][1:]
        rec_indices = [cluster_idxs[pos] for pos in rec_songs]

        
        print("Input cluster:", cluster)

        return self.songs.loc[rec_indices, ["song_id", "song_name", "artists", "cluster"]]

    def initialize_plot(self, ax, canvas):
        ax.clear()
        sample = self.songs.sample(400)

        ax.scatter(sample["pca_x"], sample["pca_y"], s=8, alpha=0.3, label="All songs")
        ax.set_title("Song Space (PCA)")
        ax.set_xlabel("PCA 1")
        ax.set_ylabel("PCA 2")

        canvas.draw()

    def update_plot(self, song_id, rec_ids, ax, canvas):
        ax.clear()

        # Background songs
        sample = self.songs.sample(400)
        ax.scatter(sample["pca_x"], sample["pca_y"], c=sample["cluster"], s=8, alpha=0.25)

        # Input song
        input_song = self.songs[self.songs["song_id"] == song_id]
        ax.scatter(input_song["pca_x"], input_song["pca_y"],
                   c=input_song["cluster"], s=150, marker="*", label="Input Song")

        # Recommended songs
        rec_songs = self.songs[self.songs["song_id"].isin(rec_ids)]
        ax.scatter(rec_songs["pca_x"], rec_songs["pca_y"],
                   c=rec_songs["cluster"], s=120, marker=".", label="Recommended Songs")

        print(rec_songs["cluster"])

        # Connect lines
        for _, r in rec_songs.iterrows():
            ax.plot([input_song["pca_x"].iloc[0], r["pca_x"]],
                    [input_song["pca_y"].iloc[0], r["pca_y"]],
                    alpha=0.4)

        ax.set_title("Recommended Songs in PCA Space")
        ax.legend()

        canvas.draw()

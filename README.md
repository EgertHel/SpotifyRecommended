# SpotifyRecommended
**Authors:** Egert Heliste & Kristjan Sild

## Overview

Discovering new music that matches personal taste can be difficult, and existing recommendation systems offer little transparency. The project aims to build a simple, interpretable recommendation engine that suggests similar songs using publicly available Spotify audio features. The goal is to help users explore music through clear logic and visual explanations rather than an opaque black-box system.

## Project structure
```
root/
│
├──data/
│   ├──rawData/   # Original datasets (not included)
│   └──cleaned_data.pkl   # Cached cleaned dataset
│
├──src/
│  ├──main.py   # Project entry point
│  ├──dataParser.py   # Loading, parsing datasets
│  ├──rec_algorithm.py   # KNN recommendation model
│  └──Gui.py   # Tkinter GUI
│
├──requirements.txt   # dependencies
└──README.MD
```
## Running the program

1. Clone the repo
2. Download the datasets
   - [Dataset 1](https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks)
   - [Dataset 2](https://www.kaggle.com/datasets/josephinelsy/spotify-top-hit-playlist-2010-2022)
3. Place the datasets into data/rawData/. The expected files are `artists.csv` and `tracks.csv` from the first dataset and `playlist_2010to2023.csv` from the second dataset.
4. You can install all necessary dependencies using
```
pip install -r requirements.txt
```
5. You can now run main.py

## How to replicate

To reproduce everything we did:
1. Load and clean data
   - Rename columns of the two datasets so that they match
   - Drop rows where song name is NaN
   - Drop columns with NaN values
2. Compute clusters and create KNN models
   - Select features for the KNN model
   - Scale the selected features
   - Compute clusters using KMeans from sklearn.cluster
   - Create a KNN model for each cluster using NearestNeighbors from sklearn.neighbors and euclidean distances
   - Apply PCA using PCA from sklearn.decomposition to later create 2D visualisations
3. Find recommendations using an input song
   - Find the cluster that the input song is in
   - Using the KNN model for this cluster, find n nearest neighbors (n recommendations)
   - Convert recommendations indices to global indices to get all data about the song
4. Visualise the recommendations
   - Create a PCA scatterplot
   - Plot a reduced number of songs from the dataset to increase performance
   - Plot the initial song and recommendations so that they are distinctly marked
   - Color the datapoints based on clustering

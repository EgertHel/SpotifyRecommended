# SpotifyRecommended
**Authors:** Egert Heliste & Kristjan Sild

## Overview

TODO

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

TODO
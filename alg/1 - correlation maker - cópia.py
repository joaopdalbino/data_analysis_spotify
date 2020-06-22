import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np

path = dirname(dirname(abspath(__file__)))

non_numerical_columns = [
		'mode',
		'key',
		'genre',
		'artist_name',
		'track_name',
		'track_id',
		'time_signature'
	]

def load_database():
	return pd.read_csv(path + '/data/SpotifyFeatures.csv')

def cleans_df(df):

	df = df.iloc[:,4:]

	for i in non_numerical_columns:
		try:
			df = df.drop([i], axis=1)
		except:
			pass
	return df

if __name__ == "__main__":

	df_raw = load_database()

	df_cleaned = cleans_df(df_raw)

	df_cleaned.to_csv(path+'/results/data/4 - spotify_numerical_features_only.csv',index=False)
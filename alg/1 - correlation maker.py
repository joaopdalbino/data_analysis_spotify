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

def person_correlation(df, y, y_name):
	data = df
	df = df.drop([y_name], axis=1)	
	cor_list = pd.DataFrame(columns=['column', 'correlation'])
	for i in df.columns.tolist():
		cor = np.corrcoef(df[i], y)[0, 1]
		cor_list = cor_list.append({
			'column': i, 
			'correlation': cor
		}, ignore_index=True)
	
	print(cor_list)
	cor_list.to_csv(path+'/results/data/correlation_of_numerical_features.csv',index=False)
	df = cor_list.loc[abs(cor_list['correlation']) >= 0.6]
	if(df.empty == False):
		print('---- using ' + y_name + ' as y. columns with correlation equal or greather than 0.6 p')
		print(df)
		print('---- using ' + y_name + ' as y. columns with correlation equal or greather than 0.6 p')

		for i in data.columns.tolist():
			if(i not in list(df['column']) and i != y_name):
				data = data.drop([i], axis=1)
	else:
		print('---- using ' + y_name + ' as y. there are no columns with correlation equal or greather than 0.6 p')

	return data

if __name__ == "__main__":

	df_raw = load_database()

	df_cleaned = cleans_df(df_raw)

	df_after_cor = person_correlation(df_cleaned, df_cleaned['popularity'], 'popularity')
	if(df_after_cor.equals(df_cleaned) == True):
		df_after_cor.to_csv(path+'/results/data/spotify_numerical_features_only.csv',index=False)
		print('... finished. saving numerical features only')
	else:
		df_after_cor.to_csv(path+'/results/data/spotify_correlations_greater_than_6.csv',index=False)
		print('... finished. saving greather than 0.6 cor')
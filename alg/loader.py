import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt

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

def load_data_base():
	return pd.read_csv(path + '/data/SpotifyFeatures.csv')

def correlacao_pearson_acima_de_06(df, y, y_name):
	base = df
	df = df.drop([y_name], axis=1)
	print(list(df))
	for i in non_numerical_columns:
		try:
			df = df.drop([i], axis=1)
		except:
			pass
	print(list(df))
	cor_lista = pd.DataFrame(columns=['coluna', 'correlacao'])
	for i in df.columns.tolist():
		cor = np.corrcoef(df[i], y)[0, 1]
		cor_lista = cor_lista.append({
			'coluna': i, 
			'correlacao': cor
		}, ignore_index=True)
	
	df = cor_lista.loc[abs(cor_lista['correlacao']) >= 0.6]
	print('---- usando ' + y_name + ' como base. as colunas com mais 0.6 p')
	print(df)
	print('---- usando ' + y_name + ' como base. as colunas com mais 0.6 p\n\n')
	for i in base.columns.tolist():
		if(i not in list(df['coluna']) and i != y_name):
			base = base.drop([i], axis=1)

	return base

if __name__ == "__main__":

	base_crua = load_data_base()

	print(correlacao_pearson_acima_de_06(base_crua.iloc[:,4:], base_crua['popularity'], 'popularity'))
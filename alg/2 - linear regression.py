import matplotlib.pyplot as plt
from scipy import stats
import os
from os.path import dirname, abspath
import pandas as pd
import numpy as np
import csv

path = dirname(dirname(abspath(__file__)))

def get_indicators_of_linear_regression(x, y):
	return stats.linregress(x, y)

def load_database():
	return pd.read_csv(path + '/results/data/spotify_numerical_features_only.csv')

def create_plot(slope, intercept, x, y, x_title, y_title):
	plt.plot(x, y, 'o', label='original data')
	plt.plot(x, intercept + slope*x, 'r', label='fitted line')
	plt.title('linear regression of ' + x_title + ' and ' + y_title)
	plt.savefig(path+'/results/linear regression/' + x_title + '.png')
	plt.clf()

def get_all_indicators_by_column(y, df):

	data = pd.DataFrame(columns=['y', 'x', 'slope', 'intercept', 'r_value', 'p_value', 'std_err'])

	for column in df.columns.tolist():
		if(column != y):
			print('Column: ' + column)
			slope, intercept, r_value, p_value, std_err = get_indicators_of_linear_regression(pd.Series(df[column]).array, pd.Series(df[y]).array)

			create_plot(slope, intercept, df[column], df[y], column, y)

			data = data.append({
				'y': y, 
				'x': column,
				'slope': slope, 
				'intercept': intercept, 
				'r_value': r_value, 
				'p_value': p_value, 
				'std_err': std_err
			}, ignore_index=True)

	return data

def get_all_correlations(df):


	with open(path + '/results/linear regression/2 - all correlations to be compared.csv', mode='w') as correlation_file:

		correlation_writer = csv.writer(correlation_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		columns = df.columns.tolist()

		columns.insert(0,'')

		correlation_writer.writerow(columns)

		del columns[0]

		l = len(columns)

		while(len(columns) > 0):

			n = columns[0]

			del columns[0]

			x = get_all_features_correlations_from_given_y(n, columns, df)

			while (len(x) < l):
				x.insert(0,0)

			x.insert(0,n)

			correlation_writer.writerow(x)

def get_all_features_correlations_from_given_y(y, columns, df):
	
	x = []

	x.insert(0,1)

	for column in columns:
		x.append(np.corrcoef(df[y], df[column])[0, 1])

	return x

if __name__ == "__main__":

	print('loading database...')
	df = load_database()

	y = 'popularity'

	print('creating linear regression indicators based on ' + y + ' ...')
	get_all_indicators_by_column(y, df).to_csv(path+'/results/linear regression/2 - linear_regression_indicators.csv',index=False)

	print('checking all correlations...')
	get_all_correlations(df)

	print('... finishing.')
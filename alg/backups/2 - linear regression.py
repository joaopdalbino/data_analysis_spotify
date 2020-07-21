import matplotlib.pyplot as plt
from scipy import stats
import os
from os.path import dirname, abspath
import pandas as pd
import numpy as np
import csv
import statsmodels.api as sm
from statsmodels.tools.eval_measures import rmse

path = dirname(dirname(abspath(__file__)))

#columns_collinearity = ['energy', 'loudness']
columns_collinearity = ['energy', 'loudness']

if(len(columns_collinearity)): 
	title = '_without'
else:
	title = ''

for f in columns_collinearity: title =  title + '_' + f 

def get_indicators_of_linear_regression(x, y):
	return stats.linregress(x, y)

def load_database():
	return pd.read_csv(path + '/results/data/spotify_numerical_features_only.csv')

def get_best_columns_with_forward_selection(indicators):
	# ordering by smallest p value
	# and selection only p values with 5% of significance
	indicators = indicators.sort_values(by=['p_value'], ascending=True)

	return indicators.loc[indicators['p_value'] <= 0.05]

def create_plot(slope, intercept, x, y, x_title, y_title):
	plt.plot(x, y, 'o', label='original data')
	plt.plot(x, intercept + slope*x, 'r', label='fitted line')
	plt.title('linear regression of ' + x_title + ' and ' + y_title)
	plt.savefig(path+'/results/linear regression/imgs/features_' + x_title + title + '.png')
	plt.clf()

def get_all_indicators_by_column(y, df):
	data = pd.DataFrame(columns=['y', 'x', 'slope', 'intercept', 'r_value', 'p_value', 'std_err'])

	for column in df.columns.tolist():
		if(column != y):
			print('Column: ' + column)
			slope, intercept, r_value, p_value, std_err = get_indicators_of_linear_regression(pd.Series(df[column]).array, pd.Series(df[y]).array)

			if(len(columns_collinearity) == 0): 
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
	with open(path + '/results/linear regression/data/2 - all correlations to be compared' + title + '.csv', mode='w') as correlation_file:

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

	return pd.read_csv(path + '/results/linear regression/data/2 - all correlations to be compared' + title + '.csv')

def get_all_features_correlations_from_given_y(y, columns, df):
	
	x = []

	x.insert(0,1)

	for column in columns:
		x.append(np.corrcoef(df[y], df[column])[0, 1])

	return x

def get_which_one_is_the_best_linear_regression_for_this_problem(df, indicators, y):

	indicators = get_best_columns_with_forward_selection(indicators)

	col = 0

	data = df[ [y, indicators['x'].iloc[col]]]

	flag = False
	max_p_value = 0

	while(len(data.columns.tolist()) < len(indicators['x']) + 1):
		
		X = sm.add_constant(data.drop(columns = [y], axis=1))

		est = sm.OLS(data[y], X)
		est = est.fit()

		results_summary = est.summary()

		max_p_value = est.pvalues.max()

		if(max_p_value >= 0.05):

			X = sm.add_constant(data.drop(columns = [y, indicators['x'].iloc[col]], axis=1))
			est = sm.OLS(data[y], X)
			est = est.fit()
			results_summary = est.summary()
			text_file = open(path + '/results/linear regression/data/3 - forward_selection' + title + '.csv', mode='w')
			text_file.write(results_summary.as_csv())
			text_file.close()
			return est
		else:
			col+=1
			data = data.join(df[indicators['x'].iloc[col]])

	X = sm.add_constant(data.drop(columns = [y], axis=1))
	est = sm.OLS(data[y], X)
	est = est.fit()
	results_summary = est.summary()
	text_file = open(path + '/results/linear regression/data/3 - forward_selection' + title + '.csv', mode='w')
	text_file.write(results_summary.as_csv())
	text_file.close()
	return est
		
def get_columns_to_be_dropped_as_they_have_collinearity(all_correlations):
	
	cor = pd.read_csv(path + '/results/data/correlation_of_numerical_features.csv')
	cor = cor.reindex(cor.correlation.abs().sort_values(ascending=True).index)

	data = pd.DataFrame(columns=['c1', 'c2'])

	columns = all_correlations.drop(columns = ['Unnamed: 0'], axis=1).columns.tolist()

	r_columns = []

	for column in all_correlations.drop(columns = ['Unnamed: 0'], axis=1).columns.tolist():
		aux = all_correlations.loc[(all_correlations[column].abs() >= 0.7) & (all_correlations[column].abs() < 1.0)]

		if(len(aux[column])):
			h_1 = column
			h_2 = columns[aux[column].index[0]]
			print('h 1 = ' + h_1)
			print('h 2 = ' + h_2)
			for c in cor['column']:
				if(c == h_1):
					r_columns.append(h_1)
					break
				if(c == h_2):
					r_columns.append(h_2)
					break

	return r_columns

def predict(model):

	X = pd.read_csv(path + '/results/data/4 - spotify_numerical_features_only - predict.csv')

	y_trained = X['popularity'] 

	columns = []

	for key in model.params.iteritems():
		columns.append(key[0])

	X['const'] = 1

	X = X[columns]

	y = model.predict(X)

	X['y_hat'] = y
	X['y'] = y_trained

	X.to_csv(path+'/results/linear regression/data/4 - final_result ' + title + '.csv',index=False)

	with open(path + '/results/linear regression/data/5 - MSE.csv', mode='a') as MSE_File:

		MSQ_writer = csv.writer(MSE_File, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		columns.append(str(rmse(X['y'], X['y_hat'])))

		line = columns

		MSQ_writer.writerow(line)

if __name__ == "__main__":

	print('loading database...')
	df = load_database()

	y = 'popularity'

	df = df.drop(columns = columns_collinearity, axis=1)

	print('creating linear regression indicators based on ' + y + ' ...')
	linear_regression_indicators = get_all_indicators_by_column(y, df)
	linear_regression_indicators.to_csv(path+'/results/linear regression/data/1 - linear_regression_indicators' + title + '.csv',index=False)

	print('checking all correlations...')
	all_correlations = get_all_correlations(df)

	columns_to_be_dropped = get_columns_to_be_dropped_as_they_have_collinearity(all_correlations)

	print('get the best fit for linear regression...')
	r = get_which_one_is_the_best_linear_regression_for_this_problem(df, linear_regression_indicators, y)

	predict(r)

	print('... finishing.')	
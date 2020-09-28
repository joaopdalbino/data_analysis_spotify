import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import ast 
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from sklearn.model_selection import train_test_split

pd.options.mode.chained_assignment = None  # default='warn'

backlash = '/'

# Loads CSV file as Dataframe
def data_load_csv(file, path):
	try:
		return pd.read_csv(path + backlash + file)
	except:
		return None

# Saves a dataframe file
def save_df_to_csv(df, path, file):
	df.to_csv(path + backlash + file + '.csv',index=False)

# Remove duplicates from dataframe
def data_remove_duplicates_from_df(df, key):
	return df.drop_duplicates(subset=[key], keep=False)

# Normalizes to binary
def data_normalizer(row, column, value):
	if row[column] == value: return 1
	else: return 0

# Drops column
def data_drop_column(df, column):
	return df.drop(column, axis=1)

# Creates normalized 
def data_create_columns_on_df(df, column, value):
	df['n_'+str(column)+'_'+str(value)] = df.apply(lambda row: data_normalizer(row, column, value), axis=1)
	return df

# Gets only numerical values 
def data_clean_categorical_values(df):
	df = df.iloc[:,3:]
	return df

# Converts string to list
def string_to_list(string):
	return ast.literal_eval(string)

# Sorts by the best features indicators
def sort_by_best_features(df, model):

	if(model == 'linear'):
		df = df.sort_values(by=['adjusted_r^2', 'r^2'], ascending=False)
		df = df.sort_values(by=['BIC', 'AIC', 'RSS'], ascending=True)

	return df

# Shuffles Data from dataframe
def shuffle_data(df):
	return df.sample(frac=1).reset_index(drop=True)

# * ------ FUNCTIONS TO DEAL WITH DATASET * --------
def forward_stepwise_selection(X, y):

	# we want lowest BIC and AIC, but highest Adjusted R2

	data = pd.DataFrame(columns=['y', 'x', 'r^2', 'RSS', 'BIC', 'AIC'])

	len_features = len(X.columns.tolist())

	max_len = len_features

	while(len_features > 0):
		
		if(max_len != len_features):
			columns = X.columns.tolist()
			columns = list(set(columns) - set(collumns_to_be_in_model))
		else:
			columns = X.columns.tolist()

		print(len(columns))

		if(max_len == len_features):
			r_squared, rss, adjusted_r_squared, collumns_to_be_in_model, AIC, BIC = find_best_model(X, y, None, None)
		else:
			r_squared, rss, adjusted_r_squared, collumns_to_be_in_model, AIC, BIC = find_best_model(X, y, collumns_to_be_in_model, columns)

		data = data.append({
			'y': y.columns.tolist(), 
			'x': collumns_to_be_in_model, 
			'r^2': r_squared,
			'adjusted_r^2': adjusted_r_squared,
			'RSS': rss,
			'BIC': BIC, 
			'AIC': AIC
		}, ignore_index=True)

		len_features -= 1

	return data

def find_best_model(X, y, collumns_to_be_in_model, columns):

	r_squared = 0
	r_aux = 0

	if(columns == None):
		best_columns = None
		columns = X.columns.tolist()
	else:
		X_func = X[collumns_to_be_in_model]
		best_columns = collumns_to_be_in_model

	for column in columns:
		if(best_columns == None):
			X_func = X[[column]]
		else:
			X_func[column] = X[[column]]

		model = linear_regression(X_func, y)

		r_aux = rsquared(model)

		if(r_aux > r_squared):
			r_squared = r_aux 
			rss = RSS(model)
			adjusted_r_squared = adjusted_rsquared(model)
			best_columns = X_func.columns.tolist()
			AIC = linear_regression_AIC(model)
			BIC = linear_regression_BIC(model)

		X_func = data_drop_column(X_func, column)

	return r_squared, rss, adjusted_r_squared, best_columns, AIC, BIC

def create_blocks_cross_validations(df, k_size):
	if(k_size < 2):
		print('K fold must be greater or equal to 2')
		return 0, 0

	df_size = len(df)

	block_size = int(df_size/k_size)

	indexes = []

	aux = 0

	for i in range(1, k_size+1):
		if(i > 2):
			aux += block_size
		elif(i == 2):
			aux += block_size-1
		indexes.append(aux)

	return block_size, indexes


# * ------ FUNCTIONS TO DEAL WITH DATASET * --------


# * ------ FUNCTIONS TO DEAL WITH CROSS VALIDATION * --------
def get_data_from_K(X, y, portion):
	return train_test_split(X, y, test_size=portion)
# * ------ FUNCTIONS TO DEAL WITH CROSS VALIDATION * --------


# * ------ FUNCTION TO USE LINEAR REGRESSION * --------
# Creates OLS object of Linear Regression
def RSS(model):
	return model.mse_model

def rsquared(model):
	return model.rsquared

def adjusted_rsquared(model):
	return model.rsquared_adj

def linear_regression(X, y):
	return OLS(y, add_constant(X)).fit()

def linear_regression_AIC(model):
	return model.aic

def linear_regression_BIC(model):
	return model.bic
# * ------ FUNCTION TO USE LINEAR REGRESSION * --------


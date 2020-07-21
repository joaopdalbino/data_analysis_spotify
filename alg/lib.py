import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

pd.options.mode.chained_assignment = None  # default='warn'

backlash = '/'

# Loads CSV file as Dataframe
def data_load_csv(file, path):
	try:
		return pd.read_csv(path + file)
	except:
		return None

# Saves a dataframe file
def save_df_to_csv(df, path, file):
	df.to_csv(path + backlash + file + '.csv',index=False)

# Remove duplicates from dataframe
def data_remove_duplicates_from_df(df, key):
	return df.drop_duplicates(subset=[key], keep=False)

# Binary normalizador
def data_normalizer(row, column, value):
	if row[column] == value: return 1
	else: return 0

# Drop column
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
			'adjusted_r_r^2': adjusted_rsquared,
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

	return r_squared, adjusted_r_squared, rss, best_columns, AIC, BIC
# * ------ FUNCTIONS TO DEAL WITH DATASET * --------



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


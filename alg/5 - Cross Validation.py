import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
import lib

root_working_directory_path = dirname(dirname(abspath(__file__)))
file = 'forward_stepwise_selection_models_and_indicators.csv'
value_to_predicted = 'popularity'
best_model = 26
k = 10

def data_loader(data):
	print('reading data...')
	if data == 'features':
		return lib.data_load_csv('forward_stepwise_selection_models_and_indicators.csv', root_working_directory_path + '/results/linear regression/data')
	if data == 'data':
		return lib.data_load_csv('SpotifyFeatures_normalized_data.csv', root_working_directory_path + '/data')

def get_axis(df): 
	print('getting X and y')

	df = lib.sort_by_best_features(df, 'linear')

	X = lib.string_to_list(df.iloc[0, 1])
	y = lib.string_to_list(df.iloc[0, 0])[0]

	return X, y

def set_scenario_for_cross_validation(df):

	df = lib.shuffle_data(df)

	block_size, starters_indexes = lib.create_blocks_cross_validations(df, k)

	return df, block_size, starters_indexes

def start_cross_validation():


if __name__ == '__main__':

	best_features = data_loader('features')
	
	X, y = get_axis(best_features)

	print('X = ' + str(X))
	print('y = ' + str(y))

	df = data_loader('data')

	df, k_size, k_indexes = set_scenario_for_cross_validation(df)

	moddel = get_best_model_w_cross_validation(df, X, y, k_size, k_indexes)
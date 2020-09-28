import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
import lib

root_working_directory_path = dirname(dirname(abspath(__file__)))
file = 'SpotifyFeatures_normalized_data.csv'
value_to_predicted = 'popularity'


def data_loader():
	print('reading data')
	df = lib.data_load_csv(file, root_working_directory_path + '/data')

	return df

def get_axis(df):
	print('getting X and y')
	y_column_name = value_to_predicted

	X = lib.data_drop_column(df, y_column_name)
	y = df[[y_column_name]]

	return X, y

def save_df(df):
	print('saving de models')
	lib.save_df_to_csv(df, root_working_directory_path + '/results/linear regression/data', 'forward_stepwise_selection_models_and_indicators')

if __name__ == '__main__':

	df = data_loader()

	X, y = get_axis(df)

	results = lib.forward_stepwise_selection(X, y)

	save_df(results)
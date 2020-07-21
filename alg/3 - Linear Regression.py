import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
import lib

root_working_directory_path = dirname(dirname(abspath(__file__)))
file = 'SpotifyFeatures_normalized_data.csv'

def normalizer(df):

	return df

if __name__ == "__main__":

	print('reading data')
	df = lib.data_load_csv(file, root_working_directory_path + '/data/')

	df = lib.data_clean_categorical_values(df)

	y_column_name = 'popularity'

	X = lib.data_drop_column(df, y_column_name)
	y = df[[y_column_name]]

	results = lib.forward_stepwise_selection(X, y)

	print('saving de models')
	lib.save_df_to_csv(results, root_working_directory_path + '/results/linear regression/data', 'forward_stepwise_selection_models_and_indicators')
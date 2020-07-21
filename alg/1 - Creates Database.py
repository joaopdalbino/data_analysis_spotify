import pandas as pd
from pathlib import Path
import os
from os.path import dirname, abspath
import numpy as np
import lib

file = 'SpotifyFeatures.csv'
root_working_directory_path = dirname(dirname(abspath(__file__)))
new_file = 'SpotifyFeatures_normalized_data.csv'

def normalizer(df):

	data_categorical_metadata = ['key', 'mode', 'time_signature']
	data_key = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
	data_mode = ['Minor', 'Major']
	data_time_signature = ['0/4', '1/4', '2/4', '3/4', '4/4', '5/4']

	data_categorical = [data_key] + [data_mode] + [data_time_signature]

	count = 0

	while(count < len(data_categorical_metadata)):
		for value in data_categorical[count]:
			print('checking = ' + str(data_categorical_metadata[count]) + ' of ' + str(value))
			df = lib.data_create_columns_on_df(df, data_categorical_metadata[count], value)

		df = lib.data_drop_column(df, data_categorical_metadata[count])
		count += 1

	return df

if __name__ == "__main__":

	print('reading raw data')
	df = lib.data_load_csv(file, root_working_directory_path + '/data/')

	df = lib.data_remove_duplicates_from_df(df, 'track_id')

	df = normalizer(df)

	df = lib.data_drop_column(df, 'genre')

	print('saving normalized data')
	df.to_csv(root_working_directory_path+'/data/'+new_file,index=False)
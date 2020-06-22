import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd
from os.path import dirname, abspath

key_pitch = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
mode_pitch = ['Minor', 'Major']
# playlists = 37i9dQZEVXbMDoHDwVN2tF, 23RpCJSzRh0gRHULsCtfFG, 37i9dQZEVXbLiRSasKsNU9 
p_id = '37i9dQZEVXbMXbN3EUUhlg'
g_playlist = 'Brazil Pop'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

path = dirname(dirname(abspath(__file__)))

def get_artists(artists):
	
	cont_artist = 0
	artists_names = ''

	for artist in artists:
		if(cont_artist>0):
			artists_names = ', ' + artists_names
		artists_names = artists[cont_artist]['name'] + artists_names
		cont_artist+=1

	return artists_names

def get_popularity_name_artists_from_playlist(id):


	data = pd.DataFrame(columns=['name', 'popularity', 'artists'])


	j = sp.playlist_tracks('37i9dQZEVXbMDoHDwVN2tF')

	cont = 0

	for i in j['items']:
		name = j['items'][cont]['track']['name']
		popularity = j['items'][cont]['track']['popularity']
		artists = j['items'][cont]['track']['artists']

		artists_names = get_artists(artists)

		print('name = ' + name)
		print('popularity = ' + str(popularity))
		print('artists = ' + artists_names)

		data = data.append({
			'name': y, 
			'popularity': column,
			'artists': artists_names
		}, ignore_index=True)

		cont+=1

	return data

def get_track_ids_from_playlist(id_playlist):

	song_ids = []


	j = sp.playlist_tracks(id_playlist)

	for i in j['items']:
		song_ids.append(i['track']['id'])

	return song_ids

def struct_data_song_to_df(id, feature, df):

	track_id = id

	danceability = feature['danceability']
	energy = feature['energy']
	key = key_pitch[feature['key']]
	loudness = feature['loudness']
	mode = mode_pitch[feature['mode']]
	speechiness = feature['speechiness']
	acousticness = feature['acousticness']
	instrumentalness = feature['instrumentalness']
	liveness = feature['liveness']
	valence = feature['valence']
	tempo = feature['tempo']
	type_track = feature['type']
	duration_ms = feature['duration_ms']
	time_signature = str(feature['time_signature']) + '/4'

	track  = sp.track(id)

	artists = get_artists(track['artists'])

	popularity = track['popularity']

	genre = g_playlist

	track_name = track['name']

	return df.append({
		'genre' : genre,
		'artist_name' : artists,
		'track_name' : track_name,
		'track_id' : track_id,
		'popularity' : popularity,
		'acousticness' : acousticness,
		'danceability' : danceability,
		'duration_ms' : duration_ms,
		'energy' : energy,
		'instrumentalness' : instrumentalness,
		'key' : key,
		'liveness' : liveness,
		'loudness' : loudness,
		'mode' : mode,
		'speechiness' : speechiness,
		'tempo' : tempo,
		'time_signature' : time_signature,
		'valence' : valence
	}, ignore_index=True)

def get_songs_and_save_it_on_csv():

	try:
		data = pd.read_csv(path + '/results/data/3 - dataset spotify songs.csv')
	except:
		data = pd.DataFrame(
			columns=['genre',	'artist_name',	'track_name',	'track_id',	'popularity',	'acousticness',	
			'danceability',	'duration_ms',	'energy',	'instrumentalness',	'key',	'liveness',	'loudness',	
			'mode',	'speechiness',	'tempo',	'time_signature',	'valence']
		)

	print('getting ids...')
	ids = get_track_ids_from_playlist(p_id)
	print('getting checked...')

	features = sp.audio_features(ids)

	print('features checked...')

	cont = 0

	for id in ids:

		print('getting ' + str(cont + 1) + ' ...')

		data = struct_data_song_to_df(id, features[cont], data)
		cont += 1

	data.to_csv(path + '/results/data/3 - dataset spotify songs.csv', index=False)

if __name__ == "__main__":

	get_songs_and_save_it_on_csv()
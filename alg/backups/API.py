import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd

key_pitch = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
mode_pitch = ['Minor', 'Major']

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

	print(list(j['items'][0]['track']))

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

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# print(sp.audio_features('0aym2LBJBk9DAYuHHutrIl'))
# print('-------- track -------\n\n\n\n\n')
# print(sp.track('0aym2LBJBk9DAYuHHutrIl'))

if __name__ == "__main__":

	data = pd.DataFrame(
		columns=['genre',	'artist_name',	'track_name',	'track_id',	'popularity',	'acousticness',	
		'danceability',	'duration_ms',	'energy',	'instrumentalness',	'key',	'liveness',	'loudness',	
		'mode',	'speechiness',	'tempo',	'time_signature',	'valence']
	)

	track_id = '0aym2LBJBk9DAYuHHutrIl'

	features = sp.audio_features(track_id)

	danceability = features[0]['danceability']
	energy = features[0]['energy']
	key = key_pitch[features[0]['key']]
	loudness = features[0]['loudness']
	mode = mode_pitch[features[0]['mode']]
	speechiness = features[0]['speechiness']
	acousticness = features[0]['acousticness']
	instrumentalness = features[0]['instrumentalness']
	liveness = features[0]['liveness']
	valence = features[0]['valence']
	tempo = features[0]['tempo']
	type_track = features[0]['type']
	duration_ms = features[0]['duration_ms']
	time_signature = str(features[0]['time_signature']) + '/4'

	track = sp.track(track_id)

	artists = get_artists(track['artists'])

	popularity = track['popularity']

	genre = ''

	track_name = track['name']


	data = data.append({
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

	data.to_csv()


# results = sp.search(q='Os Últimos Escolhidos do Futebol', limit=20)
# for idx, track in enumerate(results['tracks']['items']):
#     print(idx, track['name'])
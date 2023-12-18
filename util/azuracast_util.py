import requests
from util.error_util import AzuracastError, ErrorType

def get_stations(base_url):
    with requests.get(f'{base_url}/stations') as response:
        if response.status_code != 200:
            return AzuracastError(ErrorType.FailedToFetchStations, response.text)
        
        return response.json()

def get_requestable_songs(base_url, station_id):
    with requests.get(f'{base_url}/station/{station_id}/requests') as response:
        if response.status_code != 200:
            return AzuracastError(ErrorType.FailedToFetchRequestableSongs, response.text)
        
        return response.json()

def send_request(base_url, station_id, song_request):
    requestable_songs = get_requestable_songs(base_url, station_id)
    if isinstance(requestable_songs, AzuracastError):
        return requestable_songs

    song_artist = song_request.split('-')[0].strip().lower()
    song_title = song_request.split('-')[1].strip().lower()

    for song_obj in requestable_songs:
        if (
            song_title == song_obj['song']['title'].strip().lower() and
            song_artist == song_obj['song']['artist'].strip().lower()
            ):
            with requests.post(f"{base_url}/station/{station_id}/request/{song_obj['request_id']}") as response:
                if response.status_code != 200:
                    return AzuracastError(ErrorType.FailedToRequestSong, response.text)
                
            return True
        
    return AzuracastError(ErrorType.SongIsNotRequestable, 'This song cannot be requested.')

def get_nowplaying(base_url):
    with requests.get(f'{base_url}/nowplaying') as response:
        if response.status_code != 200:
            return AzuracastError(ErrorType.FailedToFetchCurrentlyPlayingSong, response.text)
        
        return response.json()
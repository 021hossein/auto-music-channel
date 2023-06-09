import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import client_id, client_secret, proxies, playlist_uri
from logger import get_module_logger

logger = get_module_logger('spotify')


def filter_recently_added_tracks(playlist_uri, last_checked_time, limit=100):
    # Set up Spotify client credentials manager
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, proxies=proxies)

    logger.info("Getting playlist items...")

    # Retrieve the first 100 tracks from the playlist
    results = spotify.playlist_items(playlist_uri, limit=limit)

    total_tracks = results['total']
    if total_tracks > limit:
        offset = max(0, total_tracks - limit)

        logger.info(f"Getting the last {limit} items from the playlist...")

        # Retrieve the last 100 tracks from the playlist
        results = spotify.playlist_items(playlist_uri, offset=offset)

    logger.info("Checking playlist for new items...")

    filtered_items = [
        track for track in results['items']
        if datetime.datetime.strptime(track['added_at'], "%Y-%m-%dT%H:%M:%SZ") > last_checked_time
    ]

    new_tracks = []

    for track in filtered_items:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        url = track['track']['external_urls']['spotify']
        file_name = f"{artist_name} - {track_name}.mp3".replace('"', "'")

        album_name = track['track']['album']['name']
        duration_ms = track['track']['duration_ms']
        popularity = track['track']['popularity']
        release_date = track['track']['album']['release_date']
        track_id = track['track']['id']
        preview_url = track['track']['preview_url']
        external_ids = track['track']['external_ids']
        additional_artists = [artist['name'] for artist in track['track']['artists'][1:]]
        cover_url = track['track']['album']['images'][0]['url']

        t = {
            'track_name': track_name,
            'artist_name': artist_name,
            'url': url,
            'file_name': file_name,
            'album_name': album_name,
            'duration_ms': duration_ms,
            'popularity': popularity,
            'release_date': release_date,
            'track_id': track_id,
            'preview_url': preview_url,
            'external_ids': external_ids,
            'additional_artists': additional_artists,
            'cover_url': cover_url,
        }

        new_tracks.append(t)

    return new_tracks


def test():
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    limit = 10

    tracks = filter_recently_added_tracks(playlist_uri, last_checked_time, limit)
    for track in tracks:
        print(track)


import datetime
import spotipy
from spotdl import Song
from spotipy.oauth2 import SpotifyClientCredentials

from config import client_id, client_secret, proxies, playlist_uris, tracks_limit
from logger import get_module_logger

logger = get_module_logger('spotify')


def filter_recently_added_tracks(playlist_uri, last_checked_time, limit=tracks_limit):
    # Set up Spotify client credentials manager
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, proxies=proxies)

    logger.info(f"Getting playlist items... {playlist_uri[-4:]}")

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

    for item in filtered_items:
        track = item['track']
        song = Song(
            name=track["name"],
            artists=[artist["name"] for artist in track["artists"]],
            artist=track["artists"][0]["name"],
            album_id=track['album']["id"],
            album_name=track['album']["name"],
            album_artist=track['album']["artists"][0]["name"],
            copyright_text=None,
            genres=track.get('genres') or [],
            disc_number=track["disc_number"],
            disc_count=int(track["disc_number"]),
            duration=track["duration_ms"] / 1000,
            year=int(track['album']["release_date"][:4]),
            date=track['album']["release_date"],
            track_number=track["track_number"],
            tracks_count=track['album']["total_tracks"],
            isrc=track.get("external_ids", {}).get("isrc"),
            song_id=track["id"],
            explicit=track["explicit"],
            publisher=track['album'].get('label') or '',
            url=track["external_urls"]["spotify"],
            popularity=track["popularity"],
            cover_url=max(
                track['album']["images"], key=lambda i: i["width"] * i["height"]
            )["url"]
            if track['album']["images"]
            else None,
        )

        new_tracks.append(song)

    return new_tracks


if __name__ == '__main__':
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(days=1)
    limit = 10

    tracks = filter_recently_added_tracks(playlist_uris[0], last_checked_time, limit)
    for track in tracks:
        print(track)


import asyncio
import datetime

import spotipy
from spotdl import Song
from spotipy import SpotifyClientCredentials

from src.config import client_id, client_secret, proxies, tracks_limit

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, proxies=proxies)


class PlayListItem:
    def __init__(self, song, added_at):
        self.song = song
        self.added_at = added_at


async def async_playlist_item(playlist_uri, limit=tracks_limit, offset=0):
    response = await asyncio.to_thread(
        spotify.playlist_items,
        playlist_id=playlist_uri,
        limit=limit,
        offset=offset
    )
    return response['total'], get_playlist_items(response)


def get_playlist_items(results):
    playlist_items = []

    for item in results['items']:
        track = item['track']
        added_at = datetime.datetime.strptime(item['added_at'], "%Y-%m-%dT%H:%M:%SZ")
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

        playlist_items.append(PlayListItem(song, added_at))

    return playlist_items



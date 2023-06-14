import asyncio
import datetime

import spotipy
from spotdl import Song
from spotipy import SpotifyClientCredentials

from src.config import CLIENT_ID, CLIENT_SECRET, PROXIES, TRACKS_LIMIT

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager, proxies=PROXIES)


class PlayListItem:
    def __init__(self, song, added_at, offset, total):
        self.song = song
        self.added_at = added_at
        self.offset = offset
        self.total = total


async def async_playlist_item(playlist_uri, limit=TRACKS_LIMIT, offset=0) -> list[PlayListItem]:
    response = await asyncio.to_thread(
        spotify.playlist_items,
        playlist_id=playlist_uri,
        limit=limit,
        offset=offset
    )
    return get_playlist_items(response)


def get_playlist_items(results) -> list[PlayListItem]:
    offset = results['offset']
    playlist_items = []
    for item in results['items']:
        offset += 1
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

        playlist_items.append(
            PlayListItem(
                song=song,
                added_at=added_at,
                offset=offset,
                total=results['total']
            )
        )

    return playlist_items



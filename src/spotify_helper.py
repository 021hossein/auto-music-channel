import datetime

from config import playlist_uris, tracks_limit
from logger import get_module_logger
from src.playlist import async_playlist_item, PlayListItem

logger = get_module_logger('spotify')


async def get_latest_playlist_items(playlist_uri, limit) -> list[PlayListItem]:
    # Retrieve the first 100 tracks from the playlist
    items = await async_playlist_item(playlist_uri, limit=limit)
    total_tracks = items[0].total

    if total_tracks > limit:
        offset = max(0, total_tracks - limit)

        logger.info(f"Getting the last {limit} items from the playlist...")

        # Retrieve the last 100 tracks from the playlist
        items = await async_playlist_item(playlist_uri, offset=offset)

    return items


async def get_recently_added_tracks(playlist_uri, last_checked_time, limit=tracks_limit):

    logger.info(f"Getting playlist items... {playlist_uri[-4:]}")

    items: list[PlayListItem] = await get_latest_playlist_items(playlist_uri, limit=limit)

    filtered_items = [
        item for item in items
        if item.added_at > last_checked_time
    ]
    return filtered_items


if __name__ == '__main__':
    tracks = get_recently_added_tracks(
        playlist_uri=playlist_uris[0],
        last_checked_time=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        limit=10
    )

    for track in tracks:
        print(track)


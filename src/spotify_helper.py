import asyncio
import datetime

from config import PLAYLIST_URIS, TRACKS_LIMIT
from logger import get_module_logger
from src.playlist import async_playlist_item, PlayListItem

logger = get_module_logger('spotify')


async def get_latest_playlist_items(playlist_uri, offset, limit) -> list[PlayListItem]:
    limit = max(10, limit)

    page_size = limit * 2
    offset = max(0, offset - limit)

    items = await async_playlist_item(playlist_uri, page_size=page_size, offset=offset)
    total_tracks = items[0].total

    if offset == 0 and total_tracks > page_size:
        offset = max(0, total_tracks - page_size)

        logger.info(f"Getting the last {page_size} items from the playlist...")

        items = await async_playlist_item(playlist_uri, page_size=page_size, offset=offset)

    return items


async def get_recently_added_tracks(playlist_uri, last_checked_time, offset=0, limit=TRACKS_LIMIT):

    logger.info(f"Getting playlist items... {playlist_uri[-4:]}")

    items: list[PlayListItem] = await get_latest_playlist_items(playlist_uri=playlist_uri, offset=offset, limit=limit)

    filtered_items = [
        item for item in items
        if item.added_at > last_checked_time
    ]
    return filtered_items


async def test():
    tracks = await get_recently_added_tracks(
        playlist_uri=PLAYLIST_URIS[0],
        last_checked_time=datetime.datetime.utcnow() - datetime.timedelta(days=1),
        limit=10
    )

    print(len(tracks))
if __name__ == '__main__':
    asyncio.run(test())


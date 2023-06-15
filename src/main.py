import asyncio
import datetime
import itertools

from config import INTERVAL, MAX_CONCURRENT_TASKS, PLAYLIST_URIS, LOGGING_INTERVAL
from logger import get_module_logger
from spotify_helper import get_recently_added_tracks
from task import perform_task

# Get the logger for the current module or script
logger = get_module_logger(__name__)

# Global task queue
task_queue = asyncio.Queue()
running_tasks = set()


async def check_recently_added_tracks(playlist_uri, interval, limit=5):
    last_added_at_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    last_offset = 0  # caching last offset for skipping unnecessary first request to Spotify
    # todo: can't skip that if new_items is empty
    while True:
        try:
            new_items = await get_recently_added_tracks(playlist_uri, last_added_at_time, offset=last_offset)

            # limit: The maximum number of recently added tracks to process per iteration.
            for item in itertools.islice(new_items, limit):
                logger.info(f"Recently added track: {item.offset} - {item.song.name}")
                last_added_at_time = item.added_at
                last_offset = item.offset
                await task_queue.put(item.song)  # Enqueue the task

            await asyncio.sleep(interval)

        except Exception as e:
            logger.error(f"An error occurred in check_recently_added_tracks: {str(e)}")


async def process_tasks(max_concurrent_tasks):
    while True:
        if len(running_tasks) < max_concurrent_tasks and not task_queue.empty():
            song = await task_queue.get()  # Dequeue the task

            task = asyncio.create_task(perform_task(song))
            running_tasks.add(task)
            task.add_done_callback(lambda t: running_tasks.remove(t))

        await asyncio.sleep(0)  # Allow other tasks to run


async def log_pending_task_count(checking_interval=LOGGING_INTERVAL):
    while checking_interval > 0:
        pending_task_size = task_queue.qsize()
        if pending_task_size == 0:
            logger.info(f"Running tasks: {len(running_tasks)}")
        else:
            logger.info(f"Pending tasks: {pending_task_size}")

        await asyncio.sleep(checking_interval)  # Allow other tasks to run


def run_bot(playlist_uris, interval, max_concurrent_tasks):
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(log_pending_task_count())

        # Start the task processing coroutine
        loop.create_task(process_tasks(max_concurrent_tasks))

        # Start the check_recently_added_tracks() coroutine for each playlist
        for playlist_uri in playlist_uris:
            loop.create_task(check_recently_added_tracks(playlist_uri, interval))

        loop.run_forever()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully stop the execution
        pass
    finally:
        # Clean up resources
        loop.stop()
        loop.close()


if __name__ == '__main__':
    run_bot(PLAYLIST_URIS, INTERVAL, MAX_CONCURRENT_TASKS)

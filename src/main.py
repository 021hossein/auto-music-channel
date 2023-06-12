import asyncio
import datetime

from config import interval, max_concurrent_tasks, playlist_uris, logging_interval
from logger import get_module_logger
from spotify_helper import get_recently_added_tracks
from task import perform_task

# Get the logger for the current module or script
logger = get_module_logger(__name__)

# Global task queue
task_queue = asyncio.Queue()
running_tasks = set()


async def check_recently_added_tracks(playlist_uri, interval):
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    while True:
        logger.info("Getting playlist items...")
        try:
            new_songs = await get_recently_added_tracks(playlist_uri, last_checked_time)
            last_checked_time = datetime.datetime.utcnow()

            for song in new_songs:
                logger.info(f"Recently added track: {song.display_name}")
                await task_queue.put(song)  # Enqueue the task

            await asyncio.sleep(interval)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")


async def process_tasks(max_concurrent_tasks):
    while True:
        if len(running_tasks) < max_concurrent_tasks and not task_queue.empty():
            song = await task_queue.get()  # Dequeue the task

            task = asyncio.create_task(perform_task(song))
            running_tasks.add(task)
            task.add_done_callback(lambda t: running_tasks.remove(t))

        await asyncio.sleep(0)  # Allow other tasks to run


async def logging_pending_count(checking_interval=logging_interval):
    while checking_interval > 0:
        pending_task_size = task_queue.qsize()
        if pending_task_size == 0:
            logger.info(f"Running tasks: {len(running_tasks)}")
        else:
            logger.info(f"Pending tasks: {task_queue.qsize()}")

        await asyncio.sleep(checking_interval)  # Allow other tasks to run


def run_bot(playlist_uris, interval, max_concurrent_tasks):
    loop = asyncio.get_event_loop()

    try:
        loop.create_task(logging_pending_count())

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
    run_bot(playlist_uris, interval, max_concurrent_tasks)

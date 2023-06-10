import asyncio
import datetime

from config import interval, max_concurrent_tasks, playlist_uris
from logger import get_module_logger
from spotify_helper import filter_recently_added_tracks
from task import perform_task


# Get the logger for the current module or script
logger = get_module_logger(__name__)

# Global task queue
task_queue = asyncio.Queue()


async def check_recently_added_tracks(playlist_uri, interval):
    last_checked_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=interval)
    while True:
        logger.info("Getting playlist items...")
        try:
            new_tracks = filter_recently_added_tracks(playlist_uri, last_checked_time)
            last_checked_time = datetime.datetime.utcnow()

            for track in new_tracks:
                logger.info(f"Recently added track: {track['track_name']}")
                await task_queue.put(track)  # Enqueue the task

            await asyncio.sleep(interval)

        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")


async def process_tasks(max_concurrent_tasks):
    running_tasks = set()
    while True:
        logger.info(f"Pending tasks: {task_queue.qsize()}  Running tasks: {len(running_tasks)}")

        if len(running_tasks) < max_concurrent_tasks and not task_queue.empty():
            track = await task_queue.get()  # Dequeue the task

            task = asyncio.create_task(perform_task(track))
            running_tasks.add(task)
            task.add_done_callback(lambda t: running_tasks.remove(t))

        await asyncio.sleep(1)  # Allow other tasks to run


def run_bot(playlist_uris, interval, max_concurrent_tasks):
    loop = asyncio.get_event_loop()

    try:
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

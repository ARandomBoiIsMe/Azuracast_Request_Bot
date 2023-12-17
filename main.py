import time
from util import config_util, reddit_util, command_handler_util, logging_util, database_util

logging_util.initialize_logger()

DATABASE_CONNECTION = database_util.connect_to_db()

LOGGER = logging_util.get_logger(__name__)

CONFIG = config_util.load_config()
REDDIT = reddit_util.initialize_reddit(CONFIG)

SUBMISSION_ID = CONFIG['VARS']['THREAD_ID']

BASE_URL = f"{CONFIG['AZURACAST']['SITE_URL']}/api"
STATION_ID = CONFIG['AZURACAST']['STATION_ID']

if __name__ == '__main__':
    last_comment = None

    MINUTES = 2
    SLEEP_DURATION = MINUTES * 60

    # Processes new comments every 'MINUTES' minutes
    while True:
        LOGGER.info(f'Awake and ready to process comments!')

        # Parses processed comments and gets all comment IDs from them.
        processed_comment_ids = [item[0] for item in database_util.retrieve_processed_comments(DATABASE_CONNECTION)]

        try:
            comments = reddit_util.get_new_comments(REDDIT, SUBMISSION_ID, last_comment)
            last_comment = comments[-1]

            for comment in comments:
                if comment.id in processed_comment_ids:
                    LOGGER.info(f'Previously processed comment found - {comment.id}: {comment.author.name} - {comment.body}')
                    continue

                command_handler_util.process_comment(comment, BASE_URL, STATION_ID, DATABASE_CONNECTION)

        except Exception as e:
            LOGGER.error(f"An error occurred: {e}")

        LOGGER.info(f'Sleeping for about {MINUTES} minute(s)...')
        time.sleep(SLEEP_DURATION)

# Add database to store processed comments - Done
# Improve logic and error handling for commands - Done
# Add logging - Done
# MAYBE, add threading/async
# Add more descriptive/specific errors for azuracast request function - Done
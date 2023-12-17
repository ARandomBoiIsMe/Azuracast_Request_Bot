import sqlite3
from sqlite3 import Error
import threading
from util.logging_util import get_logger

LOGGER = get_logger(__name__)

# This ensures that only one thread can write/commit changes to the database at a time.
# Gotta avoid those race conditions.
DB_LOCK = threading.Lock()

def connect_to_db():
    try:
        connection = sqlite3.connect('bot_database.db', check_same_thread=False)
        connection.execute("""
                    CREATE TABLE IF NOT EXISTS processed_comments (
                        comment_id TEXT NOT NULL
                    );
                    """)
        
        connection.commit()

        LOGGER.info('Database successfully created.')

        return connection
    except Error as e:
        LOGGER.error(f'Database Error: {e}.')

        raise

def insert_processed_comment(connection, comment_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM processed_comments WHERE comment_id = ?", (comment_id,))
    result = cursor.fetchone()
    
    if not result:
        with DB_LOCK:
            connection.execute("INSERT INTO processed_comments (comment_id) VALUES (?)", (comment_id,))
            connection.commit()

def retrieve_processed_comments(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM processed_comments")

    return cursor.fetchall()

def remove_processed_comment(connection, comment_id):
    with DB_LOCK:
        connection.execute("DELETE FROM processed_comments WHERE comment_id = ?", (comment_id,))
        connection.commit()

# Self-explanatory. This comment isn't needed, but I ain't deleting it.
def close_connection(connection):
    connection.close()

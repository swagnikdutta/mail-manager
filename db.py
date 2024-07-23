import logging
import sqlite3

DATABASE_NAME = "store.db"

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY, 
    subject TEXT,
    sender TEXT, 
    receiver TEXT, 
    datetime TEXT
)
"""

INSERT_INTO_MESSAGES = """
INSERT INTO messages (id, subject, sender, receiver, datetime)
VALUES (?, ?, ?, ?, ?)
"""

logger = logging.getLogger(__name__)


def setup():
    conn = None

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        logger.info(f"Sqlite version: {sqlite3.sqlite_version}")
        create_schema(conn)
        return conn

    except sqlite3.Error as e:
        logger.error(f"Error creating database connection: Error: {e}")
        if conn:
            conn.close()
        return None


def create_schema(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_MESSAGES_TABLE)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error creating schema. Error: {e}")


def insert_message(conn, message):
    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_INTO_MESSAGES,
                       (message.id, message.subject, message.sender, message.receiver, message.datetime))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting record into table 'messages'")

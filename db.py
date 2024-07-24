import json
import logging
import sqlite3

from models.message import Message
from models.rules import Rule

DATABASE_NAME = "store.db"

CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY, 
    sender TEXT, 
    receiver TEXT, 
    subject TEXT,
    body TEXT,
    datetime TEXT
)
"""
INSERT_INTO_MESSAGES = "INSERT INTO messages (id, sender, receiver, subject, body, datetime) VALUES (?, ?, ?, ?, ?, ?)"
GET_ALL_MESSAGES = "SELECT * FROM messages"

CREATE_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY,
    apply_predicate TEXT,
    conditions TEXT,
    actions TEXT
)
"""
INSERT_INTO_RULES = "INSERT INTO rules (apply_predicate, conditions, actions) VALUES (?, ?, ?)"
GET_ALL_RULES = "SELECT * FROM rules"

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
        cursor.execute(CREATE_RULES_TABLE)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error creating schema. Error: {e}")


def insert_message(conn, message):
    try:
        cursor = conn.cursor()
        cursor.execute(INSERT_INTO_MESSAGES,
                       (message.id, message.sender, message.receiver, message.subject, message.body, message.datetime))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting record into table 'messages'")


def get_all_messages(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_MESSAGES)
        rows = cursor.fetchall()
        results = []

        for row in rows:
            results.append(Message(
                id=row[0],
                sender=row[1],
                receiver=row[2],
                subject=row[3],
                body=row[4],
                datetime=row[5],
            ))
        return results

    except sqlite3.Error as e:
        logger.error(f"Error getting messages. Error: {e}")


def insert_rule(conn, rule):
    try:
        r = rule.serialize()
        cursor = conn.cursor()
        cursor.execute(INSERT_INTO_RULES,
                       (r["apply_predicate"], json.dumps(r["conditions"]), json.dumps(r["actions"])))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting record into table: 'rule'")


def get_all_rules(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(GET_ALL_RULES)
        rows = cursor.fetchall()
        results = []

        for row in rows:
            results.append(Rule(
                apply_predicate=row[1],
                conditions=json.loads(row[2]),
                actions=json.loads(row[3])
            ))
        return results

    except sqlite3.Error as e:
        logger.error(f"Error getting rules. Error: {e}")

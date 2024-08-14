import json
import logging
import sqlite3

from database import query
from database.query import DROP_TABLE_MESSAGES, DROP_TABLE_RULES
from models.message import Message
from models.rules import Rule

logger = logging.getLogger(__name__)


def setup(path):
    conn = None

    try:
        conn = sqlite3.connect(path)
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
        cursor.execute(query.CREATE_MESSAGES_TABLE)
        cursor.execute(query.CREATE_RULES_TABLE)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error creating schema. Error: {e}")


def insert_message(conn, message):
    try:
        cursor = conn.cursor()
        cursor.execute(query.INSERT_INTO_MESSAGES,
                       (message.id, message.sender, message.receiver, message.subject, message.body, message.datetime))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting record into table 'messages'. Error {e}")


def get_all_messages(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query.GET_ALL_MESSAGES)
        rows = cursor.fetchall()
        results = []

        for row in rows:
            results.append(Message(
                id=row[0],
                sender=row[1],
                receiver=row[2],
                subject=row[3],
                body=row[4],
                msg_datetime=row[5],
            ))
        return results

    except sqlite3.Error as e:
        logger.error(f"Error getting messages. Error: {e}")


def insert_rule(conn, rule):
    try:
        r = rule.serialize()
        cursor = conn.cursor()
        cursor.execute(query.INSERT_INTO_RULES,
                       (json.dumps(r["conditions"]), json.dumps(r["actions"])))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error inserting record into table 'rule'. Error: {e}")


def get_all_rules(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(query.GET_ALL_RULES)
        rows = cursor.fetchall()
        results = []

        for row in rows:
            r = Rule().deserialize({
                "conditions": json.loads(row[1]),
                "actions": json.loads(row[2]),
            })
            results.append(r)
        return results

    except sqlite3.Error as e:
        logger.error(f"Error getting rules. Error: {e}")


def clean(conn):
    cursor = conn.cursor()
    cursor.execute(DROP_TABLE_MESSAGES)
    cursor.execute(DROP_TABLE_RULES)
    conn.commit()
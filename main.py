import json
import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages
from auth.authenticate import authenticate
from db import setup, insert_message, insert_rule
from models.rules import Rule

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def run():
    conn = setup()
    if not conn:
        return

    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    # Fetching messages
    message_count = 5
    messages = list_messages(svc, message_count)

    # Putting messages into database
    for msg in messages:
        insert_message(conn, msg)

    # Processing rules and putting them into database
    process_rules(conn)

    # Applying rules on messages
    apply_rules(conn)

    # teardown
    teardown(conn)


def process_rules(conn):
    with open("rules.json") as rules_file:
        rules = json.load(rules_file)

    for rule in rules:
        rule_obj = Rule().deserialize(rule)
        insert_rule(conn, rule_obj)


def apply_rules(conn):
    pass


def teardown(conn):
    conn.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    run()

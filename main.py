import json
import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages
from auth.authenticate import authenticate
from db import setup, insert_message
from models.rules import Rule

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def run():
    conn = setup()
    if not conn:
        return

    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    message_count = 1
    messages = list_messages(svc, message_count)

    for msg in messages:
        insert_message(conn, msg)

    process_rules()
    teardown(conn)


def process_rules():
    # rules = []
    with open("rules.json") as rules_file:
        rules = json.load(rules_file)

    for rule in rules:
        rule_obj = Rule().deserialize(rule)
        # Insert the rule object in the db


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

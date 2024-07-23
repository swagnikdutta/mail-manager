import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages
from auth.authenticate import authenticate
from db import setup, insert_message

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

    teardown(conn)


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

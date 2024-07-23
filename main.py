from googleapiclient.discovery import build

from api.gmail_api import list_messages
from auth.authenticate import authenticate

# If modifying these scopes, delete the file token.json
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def run():
    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    message_count = 1
    messages = list_messages(svc, message_count)


if __name__ == "__main__":
    run()

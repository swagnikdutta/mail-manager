import logging
from datetime import datetime, timezone

from models import constants
from models.constants import CONDITION_FIELDS_STRING, CONDITION_FIELDS_DATETIME, UNINITIALIZED_TIMESTAMP
from utils.util import translate_field_to_header


class Message:
    def __init__(
            self,
            id=None,
            sender=None,
            receiver=None,
            subject=None,
            body=None,
            msg_datetime=None
    ):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.datetime = msg_datetime

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "receiver": self.receiver,
            "subject": self.subject,
            "body": self.body,
            "datetime": self.datetime
        }

    def deserialize(self, data):
        try:
            headers = data.get("payload", {}).get("headers", [])
            self.id = data.get("id")
            self.datetime = int(data.get("internalDate", UNINITIALIZED_TIMESTAMP))
            self.body = data.get("payload", {}).get("body", {}).get("data", "")
            self.receiver = self.extract_header(headers, "name", "To")
            self.sender = self.extract_header(headers, "name", "From")
            self.subject = self.extract_header(headers, "name", "Subject")
            return self
        except Exception as e:
            logging.error(f"Error deserializing message: {e}")
            return None

    def satisfies_condition(self, condition):
        field_name = condition.field
        predicate = condition.predicate
        value = condition.value

        message_serialized = self.serialize()
        msg_header = translate_field_to_header(field_name)

        if field_name in CONDITION_FIELDS_STRING:
            s1 = message_serialized[msg_header].casefold().strip()
            s2 = value.casefold().strip()

        elif field_name in CONDITION_FIELDS_DATETIME:
            if self.datetime == UNINITIALIZED_TIMESTAMP:
                return False

            email_date = datetime.fromtimestamp(self.datetime / 1000, tz=timezone.utc)
            cur_date = datetime.now(tz=timezone.utc)
            delta = cur_date - email_date
            days_elapsed = delta.days

            tokens = value.split()
            time_threshold = int(tokens[0])
            if tokens[1] in ["month", "months"]:
                time_threshold = time_threshold * 30

        match predicate:
            case constants.CONTAINS:
                return s2 in s1
            case constants.DOES_NOT_CONTAIN:
                return s2 not in s1
            case constants.EQUALS:
                return s1 == s2
            case constants.DOES_NOT_EQUAL:
                return s1 != s2
            case constants.LESS_THAN:
                return days_elapsed < time_threshold
            case constants.GREATER_THAN:
                return days_elapsed > time_threshold

    @staticmethod
    def extract_header(headers, k, v):
        header = next((h for h in headers if h.get(k) == v), None)
        if header:
            return header.get("value", None)
        return None

    def __repr__(self):
        return f"Message(id='{self.id}', sender='{self.sender}', receiver='{self.receiver}', subject='{self.subject}')"

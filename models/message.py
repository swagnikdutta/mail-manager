import logging

from models import constants
from utils.util import translate_field_to_header


class Message:
    def __init__(
            self,
            id=None,
            sender=None,
            receiver=None,
            subject=None,
            body=None,
            datetime=None
    ):
        self.id = id
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.body = body
        self.datetime = datetime

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
            self.id = data.get("id")
            headers = data.get("payload", {}).get("headers", [])

            self.receiver = self.extract_header(headers, "name", "To")
            self.sender = self.extract_header(headers, "name", "From")
            self.subject = self.extract_header(headers, "name", "Subject")
            self.datetime = self.extract_header(headers, "name", "Date")
            self.body = data.get("payload", {}).get("body", {}).get("data", "")
            return self

        except Exception as e:
            logging.error(f"Error deserializing message: {e}")
            return None

    def satisfies_condition(self, condition):
        field_name = condition.name
        predicate = condition.predicate
        value = condition.value

        message_serialized = self.serialize()
        msg_header = translate_field_to_header(field_name)

        match predicate:
            case constants.CONTAINS:
                s, sub_s = message_serialized[msg_header], value
                return sub_s in s
            case constants.DOES_NOT_CONTAIN:
                s, sub_s = message_serialized[msg_header], value
                return sub_s not in s
            case constants.EQUALS:
                s1, s2 = message_serialized[msg_header], value
                return s1 == s2
            case constants.DOES_NOT_EQUAL:
                s1, s2 = message_serialized[msg_header], value
                return s1 != s2
            case constants.LESS_THAN:
                pass
            case constants.GREATER_THAN:
                pass

    @staticmethod
    def extract_header(headers, k, v):
        header = next((h for h in headers if h.get(k) == v), None)
        if header:
            return header.get("value", "")
        return None

    def __repr__(self):
        return f"Message(id='{self.id}', sender='{self.sender}', receiver='{self.receiver}', subject='{self.subject}')"

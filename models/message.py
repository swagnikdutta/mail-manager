import logging


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

    @staticmethod
    def extract_header(headers, k, v):
        header = next((h for h in headers if h.get(k) == v), None)
        if header:
            return header.get("value", "")
        return None

    def __repr__(self):
        return f"Message(id='{self.id}', sender='{self.sender}', receiver='{self.receiver}', subject='{self.subject}')"

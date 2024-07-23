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
        self.id = data["id"]
        headers = data["payload"]["headers"]

        tmp = next((h for h in headers if h["name"] == "To"), None)
        if tmp:
            self.receiver = tmp["value"]

        tmp = next((h for h in headers if h["name"] == "From"), None)
        if tmp:
            self.sender = tmp["value"]

        tmp = next((h for h in headers if h["name"] == "Subject"), None)
        if tmp:
            self.subject = tmp["value"]

        tmp = next((h for h in headers if h["name"] == "Date"), None)
        if tmp:
            self.datetime = tmp["value"]

        self.body = data["payload"]["body"]["data"]

        return self

    def __repr__(self):
        return f"Email(id='{self.id}', sender='{self.sender}', receiver='{self.receiver}', subject='{self.subject}')"

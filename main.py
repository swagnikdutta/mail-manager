import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth.authenticate import authenticate
from models.message import Message

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def run():
    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    try:
        # results = service.users().messages().list(userId="me").execute()
        # messages = results.get("messages", [])

        results = {}
        messages = results.get("messages", [
            {
                "id": "190dbd799d0fe5d6",
                "threadId": "190dbd799d0fe5d6"
            },
            # {
            #     "id": "190dbb53709bdf66",
            #     "threadId": "190dbb53709bdf66"
            # },
        ])

        if not messages:
            print("No messages found.")
            return

        print(messages)

        for m in messages:
            msg_id = m["id"]
            # msg = svc.users().messages().get(userId="me", id=msg_id).execute()
            msg = {
                "id": "190dbd799d0fe5d6",
                "threadId": "190dbd799d0fe5d6",
                "labelIds": [
                    "IMPORTANT",
                    "CATEGORY_UPDATES",
                    "INBOX"
                ],
                "snippet": "Hello – Within the last 10 months you applied for a role at Mastercard. We value your feedback and would like to know more about your experience. We are working with a third party, non-profit",
                "payload": {
                    "partId": "",
                    "mimeType": "text/plain",
                    "filename": "",
                    "headers": [
                        {
                            "name": "Delivered-To",
                            "value": "swagnikd@gmail.com"
                        },
                        {
                            "name": "Received",
                            "value": "by 2002:a54:2848:0:b0:266:5978:29e2 with SMTP id w8csp2228305ecq;        Mon, 22 Jul 2024 12:07:38 -0700 (PDT)"
                        },
                        {
                            "name": "X-Google-Smtp-Source",
                            "value": "AGHT+IFVDm6t8O2rz+8EG4QWTyJpfZyIP8ui/0274BYnZMV5mXqCzlIJ+yVlsscRND7YWSD7WFYc"
                        },
                        {
                            "name": "X-Received",
                            "value": "by 2002:a05:6808:3008:b0:3da:ac08:cd53 with SMTP id 5614622812f47-3dae60df79emr5045440b6e.7.1721675257962;        Mon, 22 Jul 2024 12:07:37 -0700 (PDT)"
                        },
                        {
                            "name": "ARC-Seal",
                            "value": "i=1; a=rsa-sha256; t=1721675257; cv=none;        d=google.com; s=arc-20160816;        b=X7o6fNS00wv3PEJ98P+F0m+X8yeuB1hZ5R37F6oP/ZaW4kqDZkmfu3vNJCKUaF9FGC         aWhdxCdQZSl0X4XY7KZEofAlZ+cg7rJubKy3lYnKLM1xBWGwOu4rkcRH/2APXAKg2PGE         T0+wJWzVeaiJUa//0wjZH4kZL4Qn4Lpjy9S9rXNy9jTxJqy6qV0aRRJew748mAOyiYWL         Pcn7DuRObMQNIkQ9ja/uib0XX/yLVE+y0mWhxYItaFUSH9qeFCMChEhrQVHAwvkbx7TL         4ikLMQwZut+lzv1E4H8uxcYkev5KzkmW3aI+Tu3kUSLCPsN5namA9cOb+uQR/fv0WCiu         0CXA=="
                        },
                        {
                            "name": "ARC-Message-Signature",
                            "value": "i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;        h=message-id:from:to:subject:dkim-signature:date;        bh=3NqNxyyoG2APeCIyhATsCs1iZO5uAGuHrPK/rX3fiZ0=;        fh=aNZZv6dCGQ2cdv5vNmf/H+r4OvpiKQ3skSGTJF+13+w=;        b=PYy339xGlHty6T6geIwA15fj2iJNzle9Ntfov3lkr5DhamfEyJZTJFoM9Yx6+iHd8r         9ZRUkGM2SFP3jY7ROR+Zkalbk3KRaN5Z1vE5t0R/lINK1H144cfMsQIxE534fN7TP3jZ         /OYbvFjB05qhLvQRycFOHiBOsQXlj3pCVyQ01YG4Vlo0g2aqNgofRLiskkQpDHtC+kUo         0noWgbt4KzXS3VkPQ/2bTA3Yw+FhiYPkIGy8jMk7Ql7RcbKDGu+K+T+EfF+7o+7gmSBv         jOPNIkVkbRwAWxbYZuNMrv3s2ZAMDRkTyfpmREMGZvNH+FH3VmHNLm56w/AbS24qoch6         PeiQ==;        dara=google.com"
                        },
                        {
                            "name": "ARC-Authentication-Results",
                            "value": "i=1; mx.google.com;       dkim=pass header.i=@mastercard.com header.s=mcdk1 header.b=Ph2hvmEJ;       spf=pass (google.com: domain of gtastrategy.operations@mastercard.com designates 216.119.217.33 as permitted sender) smtp.mailfrom=GTAStrategy.Operations@mastercard.com;       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=mastercard.com"
                        },
                        {
                            "name": "Return-Path",
                            "value": "<GTAStrategy.Operations@mastercard.com>"
                        },
                        {
                            "name": "Received",
                            "value": "from bounce0.mastercard.com (bounce0.mastercard.com. [216.119.217.33])        by mx.google.com with ESMTPS id 5614622812f47-3dae09c83a5si3676354b6e.150.2024.07.22.12.07.37        for <swagnikd@gmail.com>        (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);        Mon, 22 Jul 2024 12:07:37 -0700 (PDT)"
                        },
                        {
                            "name": "Received-SPF",
                            "value": "pass (google.com: domain of gtastrategy.operations@mastercard.com designates 216.119.217.33 as permitted sender) client-ip=216.119.217.33;"
                        },
                        {
                            "name": "Authentication-Results",
                            "value": "mx.google.com;       dkim=pass header.i=@mastercard.com header.s=mcdk1 header.b=Ph2hvmEJ;       spf=pass (google.com: domain of gtastrategy.operations@mastercard.com designates 216.119.217.33 as permitted sender) smtp.mailfrom=GTAStrategy.Operations@mastercard.com;       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=mastercard.com"
                        },
                        {
                            "name": "Received",
                            "value": "from pps.filterd (ser2stl21.mastercard.int [127.0.0.1]) by ser2stl21.mastercard.int (8.17.1.19/8.17.1.19) with ESMTP id 46MIJOoP019502 for <swagnikd@gmail.com>; Mon, 22 Jul 2024 14:07:36 -0500"
                        },
                        {
                            "name": "Date",
                            "value": "Mon, 22 Jul 2024 14:07:36 -0500"
                        },
                        {
                            "name": "DKIM-Signature",
                            "value": "v=1; a=rsa-sha256; c=relaxed/relaxed; d=mastercard.com; h=subject : to : from : message-id; s=mcdk1; bh=3NqNxyyoG2APeCIyhATsCs1iZO5uAGuHrPK/rX3fiZ0=; b=Ph2hvmEJy1iPDe/gCZp+U7HQQea/IpsvckslWIqoEUSsIwP/hDa5sfXZDhQVZHgz5OUF yv1FVpoyEHFuQpG4ZOT2zAZC9E9Q5sqbM2d4UbE97j7ZLp80+kR/DHDPfw7OUBDdYfE9 sv4UStSm5tntr8FeMiakSIdQyM1whdZIhFPMxVcP4PggGVdI8Ezpq4iqES8KnPowg58o e7mFneZdbFLMr2z4tls/19+rFARhnDPiznwF+jPnZ6EogQGa692/9FyXGB4RjmKzohAg 7p2A6OKT7i7/3X+tCGQzNNkRHm1zRWYjpc3jdC+BQRf4jcGPNHzb6Wk8Yc7cdjy5wAj2 kg=="
                        },
                        {
                            "name": "Received",
                            "value": "from mailhost.mclocal.int ([10.154.244.24]) by ser2stl21.mastercard.int (PPS) with ESMTP id 40gb3cqscy-1 for <swagnikd@gmail.com>; Mon, 22 Jul 2024 14:07:36 -0500"
                        },
                        {
                            "name": "Subject",
                            "value": "Mastercard Recruiting Survey"
                        },
                        {
                            "name": "To",
                            "value": "swagnikd@gmail.com"
                        },
                        {
                            "name": "From",
                            "value": "Mastercard Talent Acquisition <GTAStrategy.Operations@mastercard.com>"
                        },
                        {
                            "name": "Message-ID",
                            "value": "<40gb3cqscy-1@ser2stl21.mastercard.int>"
                        }
                    ],
                    "body": {
                        "size": 1040,
                        "data": "SGVsbG8g4oCTIA0KDQpXaXRoaW4gdGhlIGxhc3QgMTAgbW9udGhzIHlvdSBhcHBsaWVkIGZvciBhIHJvbGUgYXQgTWFzdGVyY2FyZC4gV2UgdmFsdWUgeW91ciBmZWVkYmFjayBhbmQgd291bGQgbGlrZSB0byBrbm93IG1vcmUgYWJvdXQgeW91ciBleHBlcmllbmNlLg0KDQpXZSBhcmUgd29ya2luZyB3aXRoIGEgdGhpcmQgcGFydHksIG5vbi1wcm9maXQgb3JnYW5pemF0aW9uLCBjYWxsZWQgRVJFIE1lZGlhLCB0byBhbm9ueW1vdXNseSBjb2xsZWN0IGFuZCBhbmFseXplIHlvdXIgZmVlZGJhY2sgdG8gaGVscCB1cyBpbXByb3ZlIHRoZSBleHBlcmllbmNlIHRoYXQgd2UgZGVsaXZlciB0byBvdXIgY2FuZGlkYXRlcy4gWW91IG1heSBoYXZlIHByZXZpb3VzbHkgcmVjZWl2ZWQgYW5kIGNvbXBsZXRlZCBhIE1hc3RlcmNhcmQgc3VydmV5IHJlZ2FyZGluZyB5b3VyIGNhbmRpZGF0ZSBleHBlcmllbmNlLCBwbGVhc2Ugbm90ZSB0aGF0IHRoZSBzdXJ2ZXkgeW91IGFyZSByZWNlaXZpbmcgdG9kYXkgaXMgc2VwYXJhdGUgZnJvbSB0aGUgTWFzdGVyY2FyZCBzdXJ2ZXkgYW5kIGlzIGNvbmR1Y3RlZCBieSBhbiBpbmRlcGVuZGVudCB0aGlyZCBwYXJ0eS4NCg0KTWFzdGVyY2FyZCB3aWxsIGhhdmUgYWNjZXNzIHRvIHJlc3BvbnNlcyBvbiBhbiBhZ2dyZWdhdGVkIGJhc2lzLiBUbyBlbnN1cmUgZnVsbCBhbm9ueW1pdHksIHdlIGFkdmlzZSB0aGF0IHlvdSBhdm9pZCBpbmNsdWRpbmcgYW55IHBlcnNvbmFsIGluZm9ybWF0aW9uIGluIHRoZSBzdXJ2ZXnigJlzIG9wZW4gdGV4dCBib3hlcy4NCg0KWW91ciBwYXJ0aWNpcGF0aW9uIGluIHRoaXMgYnJpZWYgb25saW5lIHN1cnZleSBpcyB2b2x1bnRhcnkgYW5kIHdpbGwgaGVscCB1cyB0byBwcm92aWRlIGEgYmV0dGVyIGNhbmRpZGF0ZSBleHBlcmllbmNlIHRvIGZ1dHVyZSBqb2Igc2Vla2Vycy4gIENsaWNrIGhlcmUgdG8gYWNjZXNzIHRoZSBzdXJ2ZXk6IGh0dHBzOi8vdS5zdXJ2YWxlLmNvbS9lM3cyTg0KDQpUaGFuayB5b3UsDQpNYXN0ZXJjYXJkIFRhbGVudCBBY3F1aXNpdGlvbiBUZWFtDQo="
                    }
                },
                "sizeEstimate": 5126,
                "historyId": "11450876",
                "internalDate": "1721675256000"
            }

            msg_obj = Message().deserialize(msg)
            print(msg_obj)

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    run()

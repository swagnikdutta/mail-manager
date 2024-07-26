import json
import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages, modify_message
from auth.authenticate import authenticate
from database import db
from models.constants import LABEL_UNREAD, LABEL_INBOX
from models.rules import Rule
from models import constants


def run():
    conn = db.setup()
    if not conn:
        return

    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    # Processing rules and putting them into database
    process_rules(conn)

    # Fetching messages
    message_count = 10
    messages = list_messages(svc, message_count)

    # Putting messages into database
    for msg in messages:
        db.insert_message(conn, msg)

    # Applying rules on messages
    apply_rules(conn, svc)

    # teardown
    teardown(conn)


def process_rules(conn):
    with open("rules.json") as rules_file:
        rules = json.load(rules_file)

    for rule in rules:
        rule_obj = Rule().deserialize(rule)
        db.insert_rule(conn, rule_obj)


def apply_rules(conn, svc):
    logger = logging.getLogger(__name__)
    messages = db.get_all_messages(conn)
    rules = db.get_all_rules(conn)

    for m in messages:
        message_id = m.id

        for r in rules:
            rule_applies = False if r.conditions.apply_predicate == constants.ANY else True

            for ci in r.conditions.condition_items:
                match r.conditions.apply_predicate:
                    case constants.ALL:
                        rule_applies = rule_applies and m.satisfies_condition(ci)
                    case constants.ANY:
                        rule_applies = rule_applies or m.satisfies_condition(ci)

            if rule_applies:
                logger.info(f"Rule applicable on message: {message_id}")

                for a in r.actions:
                    payload = {}
                    match a.field:
                        case constants.MARK_AS_READ:
                            payload = {
                                "addLabelIds": [],
                                "removeLabelIds": [LABEL_UNREAD]
                            }
                        case constants.MARK_AS_UNREAD:
                            payload = {
                                "addLabelIds": [LABEL_UNREAD],
                                "removeLabelIds": []
                            }
                            modify_message(svc, message_id, payload)
                        case constants.MOVE_MESSAGE:
                            target = a.predicate
                            payload = {
                                "addLabelIds": [target],
                                "removeLabelIds": [LABEL_INBOX]
                            }
                    modify_message(svc, message_id, payload)
                # end for
            # end if
        # end for
    # end for


def teardown(conn):
    db.clean(conn)
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

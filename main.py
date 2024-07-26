import json
import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages, modify_message
from auth.authenticate import authenticate
from database.db import setup, insert_rule, get_all_messages, get_all_rules, insert_message
from models.rules import Rule
from models import constants


def run():
    conn = setup()
    if not conn:
        return

    creds = authenticate()
    svc = build("gmail", "v1", credentials=creds)

    # Fetching messages
    message_count = 20
    messages = list_messages(svc, message_count)

    # Putting messages into database
    for msg in messages:
        insert_message(conn, msg)

    # Processing rules and putting them into database
    process_rules(conn)

    # Applying rules on messages
    apply_rules(conn, svc)

    # teardown
    teardown(conn)


def process_rules(conn):
    with open("rules.json") as rules_file:
        rules = json.load(rules_file)

    # TODO: add validation on field values
    for rule in rules:
        rule_obj = Rule().deserialize(rule)
        insert_rule(conn, rule_obj)


def apply_rules(conn, svc):
    logger = logging.getLogger(__name__)
    messages = get_all_messages(conn)
    rules = get_all_rules(conn)

    for m in messages:
        message_id = m.id

        for r in rules:
            rule_applies = False if r.apply_predicate == constants.ANY else True

            for c in r.conditions:
                match r.apply_predicate:
                    case constants.ALL:
                        rule_applies = rule_applies and m.satisfies_condition(c)
                    case constants.ANY:
                        rule_applies = rule_applies or m.satisfies_condition(c)

            if rule_applies:
                logger.info(f"Rule applicable on message: {message_id}")

                for a in r.actions:
                    payload = {}
                    match a.name:
                        case constants.MARK_AS_READ:
                            payload = {
                                "addLabelIds": [],
                                "removeLabelIds": ["UNREAD"]
                            }
                        case constants.MARK_AS_UNREAD:
                            payload = {
                                "addLabelIds": ["UNREAD"],
                                "removeLabelIds": []
                            }
                            modify_message(svc, message_id, payload)
                        case constants.MOVE_MESSAGE:
                            payload = {
                                "addLabelIds": [a.predicate],
                                "removeLabelIds": ["INBOX"]
                            }
                    modify_message(svc, message_id, payload)
                # end for
            # end if
        # end for
    # end for


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

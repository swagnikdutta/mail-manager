import json
import logging

from googleapiclient.discovery import build

from api.gmail_api import list_messages, modify_message
from auth import auth
from database import db
from models.constants import LABEL_UNREAD, LABEL_INBOX, DATABASE_PATH, RULES_CONFIG_PATH
from models.rules import Rule
from models import constants


class Runner:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.rules_config_path = RULES_CONFIG_PATH
        self.conn = None
        self.svc = None

    def setup(self):
        self.conn = db.setup(self.db_path)
        if not self.conn:
            raise Exception("Error setting up database connection")

        creds = auth.authenticate()
        self.svc = build("gmail", "v1", credentials=creds)

    def process_rules(self):
        with open(self.rules_config_path) as rules_file:
            rules = json.load(rules_file)

        try:
            logger = logging.getLogger(__name__)

            for rule in rules:
                rule_obj = Rule().deserialize(rule)
                db.insert_rule(self.conn, rule_obj)
        except Exception as e:
            logger.error(f"Error inserting rule into db. Error: {e}")

    def fetch_and_store_messages(self):
        message_count = 10
        messages = list_messages(self.svc, message_count)

        for msg in messages:
            db.insert_message(self.conn, msg)

    def apply_rules(self):
        logger = logging.getLogger(__name__)
        messages = db.get_all_messages(self.conn)
        rules = db.get_all_rules(self.conn)

        for m in messages:
            message_id = m.id
            message_subject = m.subject

            for r in rules:
                rule_applies = False if r.conditions.apply_predicate == constants.ANY else True

                for ci in r.conditions.condition_items:
                    match r.conditions.apply_predicate:
                        case constants.ALL:
                            rule_applies = rule_applies and m.satisfies_condition(ci)
                        case constants.ANY:
                            rule_applies = rule_applies or m.satisfies_condition(ci)

                if rule_applies:
                    logger.info(f"Rule applicable on message: '{message_subject}'")

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
                            case constants.MOVE_MESSAGE:
                                target = a.predicate
                                payload = {
                                    "addLabelIds": [target],
                                    "removeLabelIds": [LABEL_INBOX]
                                }
                        modify_message(self.svc, message_id, payload)
                else:
                    logger.info(f"Rule not applicable on message: '{message_subject}'")

    def teardown(self):
        db.clean(self.conn)
        self.conn.close()

    def run(self):
        self.setup()
        self.process_rules()
        self.fetch_and_store_messages()
        self.apply_rules()
        self.teardown()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    runner = Runner()
    runner.run()

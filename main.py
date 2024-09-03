import json
import logging

import yaml
from googleapiclient.discovery import build

from api.gmail_api import list_messages, modify_message
from auth import auth
from database import db
from models.constants import LABEL_UNREAD, LABEL_INBOX, CONFIG_PATH, DATABASE_PATH_KEY, RULES_CONFIG_PATH_KEY
from models.rules import Rule
from models import constants


class AppInitializer:
    def __init__(self, db_path, rules_config_path):
        self.db_path = db_path
        self.rules_config_path = rules_config_path
        self.conn = None
        self.svc = None

    def setup(self):
        self.conn = db.setup(self.db_path)
        if not self.conn:
            raise Exception("Error setting up database connection")

        creds = auth.authenticate()
        self.svc = build("gmail", "v1", credentials=creds)
        return self.conn, self.svc

    def teardown(self):
        db.clean(self.conn)
        self.conn.close()


class MessageFetcher:
    def __init__(self, svc, conn):
        self.svc = svc
        self.conn = conn
        self.logger = logging.getLogger(__name__)

    def fetch_and_store_messages(self, message_count=10):
        try:
            messages = list_messages(self.svc, message_count)
            for msg in messages:
                db.insert_message(self.conn, msg)
        except Exception as e:
            self.logger.error(f"Error listing messages. Error: {e}")


class RuleProcessor:
    def __init__(self, conn, rules_config_path):
        self.conn = conn
        self.rules_config_path = rules_config_path
        self.logger = logging.getLogger(__name__)

    def process_rules(self):
        try:
            with open(self.rules_config_path) as rules_file:
                rules = json.load(rules_file)

            for rule in rules:
                rule_obj = Rule().deserialize(rule)
                db.insert_rule(self.conn, rule_obj)
        except Exception as e:
            self.logger.error(f"Error processing rules. Error: {e}")


class RuleApplier:
    def __init__(self, conn, svc):
        self.conn = conn
        self.svc = svc
        self.logger = logging.getLogger(__name__)

    def apply_rules(self):
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
                    self.logger.info(f"Rule applicable on message: '{message_subject}'")

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
                    self.logger.info(f"Rule not applicable on message: '{message_subject}'")


class Runner:
    def __init__(self):
        self.config = self.load_config(CONFIG_PATH)
        self.app_initializer = AppInitializer(self.config[DATABASE_PATH_KEY], self.config[RULES_CONFIG_PATH_KEY])

    @staticmethod
    def load_config(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def run(self):
        conn, svc = self.app_initializer.setup()

        message_fetcher = MessageFetcher(svc, conn)
        rule_processor = RuleProcessor(conn, self.config[RULES_CONFIG_PATH_KEY])
        rule_applier = RuleApplier(conn, svc)

        rule_processor.process_rules()
        message_fetcher.fetch_and_store_messages()
        rule_applier.apply_rules()

        self.app_initializer.teardown()


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

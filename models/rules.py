import logging

from models.constants import CONDITION_FIELDS_STRING, CONDITION_FIELDS_DATETIME, CONDITION_PREDICATES_STRING, \
    CONDITION_PREDICATES_DATETIME, CONDITION_APPLY_TYPES, ACTION_TYPES, MOVE_MESSAGE, ACTION_MOVE_DESTINATION, \
    DATE_RECEIVED


class ConditionItem:
    def __init__(self, field=None, predicate=None, value=None):
        self.field = field
        self.predicate = predicate
        self.value = value

    def serialize(self):
        return {
            "field": self.field,
            "predicate": self.predicate,
            "value": self.value
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            self.field = data.get("field", "")
            self.predicate = data.get("predicate", "")
            self.value = data.get("value", "")
            self.validate()
            return self
        except Exception as e:
            logger.error(f"Error deserializing ConditionItem. Error: {e}")
            raise

    def validate(self):
        allowed_fields = CONDITION_FIELDS_STRING + CONDITION_FIELDS_DATETIME
        allowed_predicates = CONDITION_PREDICATES_STRING + CONDITION_PREDICATES_DATETIME

        if self.field not in allowed_fields:
            raise ValueError(f"Field '{self.field}' not among allowed field: {allowed_fields}")

        if self.predicate not in allowed_predicates:
            raise ValueError(f"Predicate '{self.predicate}' not among allowed predicates: {allowed_predicates}")

        if self.field in CONDITION_FIELDS_STRING and self.predicate not in CONDITION_PREDICATES_STRING:
            raise ValueError(f"Predicate '{self.predicate}' is not compatible with field '{self.field}'. "
                             f"Allowed predicates for string fields: {CONDITION_PREDICATES_STRING}")

        if self.field in CONDITION_FIELDS_DATETIME and self.predicate not in CONDITION_PREDICATES_DATETIME:
            raise ValueError(f"Predicate '{self.predicate}' not compatible with field '{self.field}'. "
                             f"Allowed predicates for datetime fields: {CONDITION_PREDICATES_DATETIME}")

        if self.field in CONDITION_FIELDS_DATETIME and self.predicate in CONDITION_PREDICATES_DATETIME:
            tokens = self.value.split()

            length_check = len(tokens) == 2
            if not length_check:
                raise ValueError(f"Invalid condition value: '{self.value}' for '{DATE_RECEIVED}' field. Expected format: '<number> [days|months]'")

            digit_check = tokens[0].isdigit()
            value_check = tokens[1] in ['day', 'days', 'month', 'months']

            if not (digit_check and value_check):
                raise ValueError(f"Invalid condition value: '{self.value}' for '{DATE_RECEIVED}' field. Expected format: '<number> [days|months]'")

class Conditions:
    def __init__(self, apply_predicate=None, condition_items=None):
        self.apply_predicate = apply_predicate
        self.condition_items = condition_items or []

    def serialize(self):
        return {
            "apply_predicate": self.apply_predicate,
            "condition_items": [ci.serialize() for ci in self.condition_items]
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            self.apply_predicate = data.get("apply_predicate", "")
            condition_items = data.get("condition_items", [])
            for ci in condition_items:
                self.condition_items.append(ConditionItem().deserialize(ci))
            self.validate()
            return self
        except Exception as e:
            logger.error(f"Error deserializing Condition. Error: {e}")
            raise

    def validate(self):
        if self.apply_predicate not in CONDITION_APPLY_TYPES:
            raise ValueError(f"Apply predicate '{self.apply_predicate}' not among {CONDITION_APPLY_TYPES}")


class Action:
    def __init__(self, name=None, predicate=None):
        self.field = name
        self.predicate = predicate

    def serialize(self):
        return {
            "field": self.field,
            "predicate": self.predicate,
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            self.field = data.get("field", "")
            self.predicate = data.get("predicate", "")
            self.validate()
            return self
        except Exception as e:
            logger.error(f"Error deserializing Action. Error: {e}")
            raise

    def validate(self):
        if self.field not in ACTION_TYPES:
            raise ValueError(f"Action field '{self.field}' not among allowed fields: {ACTION_TYPES}")
        if self.field == MOVE_MESSAGE and self.predicate not in ACTION_MOVE_DESTINATION:
            raise ValueError(f"Target '{self.predicate}' not among allowed targets: {ACTION_MOVE_DESTINATION}")


class Rule:
    def __init__(self, conditions=None, actions=[]):
        self.conditions = conditions
        self.actions = actions

    def serialize(self):
        return {
            "conditions": self.conditions.serialize(),
            "actions": [a.serialize() for a in self.actions]
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            conditions = data.get("conditions", {})
            self.conditions = Conditions().deserialize(conditions)
            actions = data.get("actions", [])
            for a in actions:
                self.actions.append(Action().deserialize(a))
            return self
        except Exception as e:
            logger.error(f"Error deserializing Rule. Error: {e}")
            raise

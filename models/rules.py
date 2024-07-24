import logging


class Condition:
    def __init__(
            self,
            name=None,
            predicate=None,
            value=None
    ):
        self.name = name
        self.predicate = predicate
        self.value = value

    def serialize(self):
        return {
            "name": self.name,
            "predicate": self.predicate,
            "value": self.value
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            self.name = data.get("name")
            self.predicate = data.get("predicate")
            self.value = data.get("value")
            return self

        except Exception as e:
            logger.error(f"Error deserializing Condition. Error: {e}")
            # TODO: Should I raise here?


class Action:
    def __init__(self, name=None, predicate=None):
        self.name = name
        self.predicate = predicate

    def serialize(self):
        return {
            "name": self.name,
            "predicate": self.predicate,
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            self.name = data.get("name", "")
            self.predicate = data.get("predicate", "")
            return self

        except Exception as e:
            logger.error(f"Error deserializing Action. Error: {e}")
            # TODO: should I raise exception here?


class Rule:
    def __init__(
            self,
            apply_predicate=None,
            conditions=None,
            actions=None
    ):
        self.apply_predicate = apply_predicate
        self.conditions = conditions
        self.actions = actions

    def serialize(self):
        return {
            "apply_predicate": self.apply_predicate,
            "conditions": [c.serialize() for c in self.conditions],
            "actions": [a.serialize() for a in self.actions]
        }

    def deserialize(self, data):
        logger = logging.getLogger(__name__)
        try:
            apply_predicate = data.get("applyPredicate")
            conditions = data.get("conditions")
            actions = data.get("actions")

            self.apply_predicate = apply_predicate
            self.conditions = []
            self.actions = []

            for c in conditions:
                c_obj = Condition().deserialize(c)
                self.conditions.append(c_obj)

            for a in actions:
                a_obj = Action().deserialize(a)
                self.actions.append(a_obj)

            return self

        except Exception as e:
            logger.error(f"Error deserializing Rule. Error: {e}")
            raise

    def apply(self):
        pass



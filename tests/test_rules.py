import unittest

from models.constants import CONDITION_APPLY_TYPES, FROM, \
    CONTAINS, MOVE_MESSAGE, LABEL_TRASH, ALL, LESS_THAN, SUBJECT, DATE_RECEIVED
from models.rules import Rule


class TestRule(unittest.TestCase):

    def test_deserialize_valid(self):
        data = {
            "conditions": {
                "apply_predicate": ALL,
                "condition_items": [
                    {"field": FROM, "predicate": CONTAINS, "value": "test_value"}
                ]
            },
            "actions": [
                {"field": MOVE_MESSAGE, "predicate": LABEL_TRASH}
            ]
        }
        rule = Rule().deserialize(data)
        self.assertEqual(rule.conditions.apply_predicate, CONDITION_APPLY_TYPES[0])
        self.assertEqual(len(rule.conditions.condition_items), 1)
        self.assertEqual(len(rule.actions), 1)

    def test_deserialize_invalid_apply_predicate(self):
        data = {
            "conditions": {
                "apply_predicate": "invalid_apply_predicate",
                "condition_items": []
            },
            "actions": []
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Apply predicate 'invalid_apply_predicate' not among ['all', 'any']"
        self.assertEqual(str(context.exception), expected_message)

    def test_deserialize_invalid_condition_field(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": "invalid_field",
                        "predicate": "contains",
                        "value": "test",
                    }
                ]
            },
            "actions": []
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Field 'invalid_field' not among allowed field: ['from', 'to', 'subject', 'date received']"
        self.assertEqual(str(context.exception), expected_message)

    def test_deserialize_invalid_condition_predicate(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": "subject",
                        "predicate": "invalid_predicate",
                        "value": "test",
                    }
                ]
            },
            "actions": []
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Predicate 'invalid_predicate' not among allowed predicates: ['contains', 'does not contain', 'equals', 'does not equal', 'is lesser than', 'is greater than']"
        self.assertEqual(str(context.exception), expected_message)

    def test_deserialize_field_string_predicate_datetime(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": SUBJECT,
                        "predicate": LESS_THAN,
                        "value": "test",
                    }
                ]
            },
            "actions": []
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Predicate 'is lesser than' is not compatible with field 'subject'. Allowed predicates for string fields: ['contains', 'does not contain', 'equals', 'does not equal']"
        self.assertEqual(str(context.exception), expected_message)

    def test_deserialize_field_datetime_predicate_string(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": DATE_RECEIVED,
                        "predicate": CONTAINS,
                        "value": "test",
                    }
                ]
            },
            "actions": []
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Predicate 'contains' not compatible with field 'date received'. Allowed predicates for datetime fields: ['is lesser than', 'is greater than']"
        self.assertEqual(str(context.exception), expected_message)

    def test_deserialize_invalid_action_field(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": SUBJECT,
                        "predicate": CONTAINS,
                        "value": "test",
                    }
                ]
            },
            "actions": [
                {
                    "field": "invalid_action_field",
                    "predicate": LABEL_TRASH
                }
            ]
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Action field 'invalid_action_field' not among allowed fields: ['mark as read', 'mark as unread', 'move message']"
        self.assertEqual(str(context.exception), expected_message)


    def test_deserialize_invalid_action_predicate(self):
        data = {
            "conditions": {
                "apply_predicate": "all",
                "condition_items": [
                    {
                        "field": SUBJECT,
                        "predicate": CONTAINS,
                        "value": "test",
                    }
                ]
            },
            "actions": [
                {
                    "field": MOVE_MESSAGE,
                    "predicate": "invalid_label"
                }
            ]
        }
        with self.assertRaises(ValueError) as context:
            Rule().deserialize(data)

        expected_message = "Target 'invalid_label' not among allowed targets: ['INBOX', 'SPAM', 'TRASH', 'UNREAD', 'STARRED', 'IMPORTANT', 'CATEGORY_PERSONAL', 'CATEGORY_SOCIAL', 'CATEGORY_PROMOTIONS', 'CATEGORY_UPDATES', 'CATEGORY_FORUMS']"
        self.assertEqual(str(context.exception), expected_message)


if __name__ == '__main__':
    unittest.main()

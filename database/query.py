# messages
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY, 
    sender TEXT, 
    receiver TEXT, 
    subject TEXT,
    body TEXT,
    datetime TEXT
)
"""
INSERT_INTO_MESSAGES = "INSERT INTO messages (id, sender, receiver, subject, body, datetime) VALUES (?, ?, ?, ?, ?, ?)"
GET_ALL_MESSAGES = "SELECT * FROM messages"



# rules
CREATE_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY,
    apply_predicate TEXT,
    conditions TEXT,
    actions TEXT
)
"""
INSERT_INTO_RULES = "INSERT INTO rules (apply_predicate, conditions, actions) VALUES (?, ?, ?)"
GET_ALL_RULES = "SELECT * FROM rules"


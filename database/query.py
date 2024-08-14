# messages
CREATE_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY, 
    sender TEXT, 
    receiver TEXT, 
    subject TEXT,
    body TEXT,
    datetime INTEGER
)
"""
INSERT_INTO_MESSAGES = "INSERT INTO messages (id, sender, receiver, subject, body, datetime) VALUES (?, ?, ?, ?, ?, ?)"
GET_ALL_MESSAGES = "SELECT * FROM messages"
DROP_TABLE_MESSAGES = "DROP TABLE IF EXISTS messages"

# rules
CREATE_RULES_TABLE = """
CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY,
    conditions TEXT,
    actions TEXT
)
"""
INSERT_INTO_RULES = "INSERT INTO rules (conditions, actions) VALUES (?, ?)"
GET_ALL_RULES = "SELECT * FROM rules"
DROP_TABLE_RULES = "DROP TABLE IF EXISTS rules"

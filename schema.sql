DROP TABLE IF EXISTS content;

CREATE TABLE content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    text TEXT NOT NULL,
    numeric INTEGER NOT NULL
);
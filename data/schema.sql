-- events table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    start_datetime DATETIME NOT NULL,
    end_datetime DATETIME,
    max_capacity INTEGER NOT NULL,
    description TEXT
);

-- attendees table with unique constraint on (email, event_id)
CREATE TABLE IF NOT EXISTS attendees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    event_id INTEGER NOT NULL,
    contact_number TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(email, event_id)
);

-- Sample events
INSERT INTO events (name, location, start_datetime, end_datetime, max_capacity, description) VALUES
('Avengers', 'New Delhi', '2025-07-01 10:00:00', '2025-07-01 18:00:00', 2, 'Start of END'),
('End Game', 'Mumbai', '2025-08-15 16:00:00', '2025-08-15 23:00:00', 3, 'A new beginning');

-- Sample attendees (do not exceed max_capacity for each event)
INSERT INTO attendees (name, email, event_id, contact_number) VALUES
('Iron Man', 'ironman@avengers.com', 1, '1234567890'),
('HULK', 'hulk@avengers.com', 1, '2345678901'),
('Thor', 'thor@avengers.com', 2, '3456789012'),
('Captain America', 'capt@avengers.com', 2, '4567890123'),
('Scarlet Witch', 'scarlet@avengers.com', 2, '5678901234');

-- sqlite3 event_management.sqlite < schema.sql
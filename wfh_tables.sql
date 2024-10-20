CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE WFH_Requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    from_datetime DATETIME NOT NULL,
    to_datetime DATETIME NOT NULL,
    approver_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'New',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (approver_id) REFERENCES Users (user_id)
);


-- Insert User (Regular Employee)
INSERT INTO Users (name, email, role) 
VALUES ('Anshul Kashyap', 'anshul.kashyap@wfh.in', 'User');

-- Insert Admin (Approver)
INSERT INTO Users (name, email, role) 
VALUES ('Jane Admin', 'jane.admin@wfh.in', 'Admin');

PRAGMA foreign_keys = ON;

-- 1. Session
CREATE TABLE IF NOT EXISTS Session (
    session_id TEXT PRIMARY KEY,
    title TEXT,
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Message
CREATE TABLE IF NOT EXISTS Message (
    message_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT DEFAULT '{}',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES Session(session_id)
        ON DELETE CASCADE
);

-- 3. Task
CREATE TABLE IF NOT EXISTS Task (
    task_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',

    input_data TEXT DEFAULT '{}',
    result TEXT,
    error TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES Session(session_id)
        ON DELETE CASCADE
);

-- 4. AgentState
CREATE TABLE IF NOT EXISTS AgentState (
    state_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL UNIQUE,

    status TEXT DEFAULT 'idle',

    memory TEXT DEFAULT '{}',
    context TEXT DEFAULT '{}',

    current_task_id TEXT,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id)
        REFERENCES Session(session_id)
        ON DELETE CASCADE,

    FOREIGN KEY (current_task_id)
        REFERENCES Task(task_id)
        ON DELETE SET NULL
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_message_session
ON Message(session_id, created_at);

CREATE INDEX IF NOT EXISTS idx_task_session
ON Task(session_id, status);

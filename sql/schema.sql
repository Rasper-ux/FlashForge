CREATE TABLE IF NOT EXISTS Articles (
    id      SERIAL PRIMARY KEY,
    -- Required fields
    author  TEXT NOT NULL,
    title   TEXT NOT NULL,
    journal TEXT NOT NULL,
    year    INT  NOT NULL,
    -- Optional fields
    volume  INT,
    number  INT,
    pages   TEXT,
    month   TEXT,
    note    TEXT,

    UNIQUE (author, title)
);

CREATE TABLE IF NOT EXISTS Books (
    id        SERIAL PRIMARY KEY,
    -- Required fields
    author    TEXT NOT NULL,
    year      INT  NOT NULL,
    title     TEXT NOT NULL,
    publisher TEXT NOT NULL,
    address   TEXT NOT NULL,

    UNIQUE (author, title)
);

CREATE TABLE IF NOT EXISTS Inproceedings (
    id           SERIAL PRIMARY KEY,
    -- Required fields
    author       TEXT NOT NULL,
    title        TEXT NOT NULL,
    booktitle    TEXT NOT NULL,
    year         INT  NOT NULL,
    -- Optional fields
    editor       TEXT,
    volume       INT,
    number       INT,
    series       TEXT,
    pages        TEXT,
    address      TEXT,
    month        TEXT,
    organization TEXT,
    publisher    TEXT,

    UNIQUE (author, booktitle)
);

CREATE TABLE IF NOT EXISTS Manuals (
    id           SERIAL PRIMARY KEY,
    -- Required fields
    title        TEXT NOT NULL,
    year         INT  NOT NULL,
    -- Optional fields
    author       TEXT,
    organization TEXT,
    address      TEXT,
    edition      TEXT,
    month        TEXT,
    note         TEXT,

    UNIQUE (title)
);

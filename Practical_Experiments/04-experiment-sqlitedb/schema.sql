-- Experiment 04: SQLite Database Schema
-- This file shows the raw SQL commands used to create the tables.

-- Create the User table
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Create the Article table
CREATE TABLE article (
    article_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

-- Create the Junction Table for Many-to-Many relationship
CREATE TABLE article_authors (
    user_id INTEGER NOT NULL,
    article_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, article_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (article_id) REFERENCES article(article_id)
);

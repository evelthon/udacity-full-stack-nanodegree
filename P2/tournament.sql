-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

--Create the database
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

--Connect to tournament database to create tables
\c tournament

--Create table match
DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
    id SERIAL,
    winner INTEGER,
    loser INTEGER
    );

--Create the player table
DROP TABLE IF EXISTS players;
CREATE TABLE players (
    id SERIAL,
    name TEXT
);


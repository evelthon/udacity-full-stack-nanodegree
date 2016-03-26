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


--Create the players table
--This tables must be created before matches table to be able to
--create the REFERENCE
DROP TABLE IF EXISTS players;
CREATE TABLE players (
    id SERIAL UNIQUE,
    name TEXT
);

--Create table matches
DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
    id SERIAL UNIQUE,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id)
    );



--Create standings table
--NOTE: Might not be needed
DROP TABLE IF EXISTS standings;
CREATE TABLE standings (
    id SERIAL,
    player_id INTEGER REFERENCES players(id)
--    wins INTEGER, Get wins from matches
--    Get matches from matches table
);

--CREATE VIEW WINS_LOSS AS
--SELECT COUNT(matches.winner) AS wins, COUNT(matches.loser) AS losses
--FROM matches, players
--WHERE matches.winner = players.id OR matches.loser = players.id;
--
--
--SELECT p.name, wl.wins, wl.loss
--FROM players AS p, matches AS m, WINS_LOSS as wl


SELECT p.id, p.name,
COUNT(m.winner) AS wins,
--COUNT(m.loser) AS losses,
(
(
SELECT COUNT(m.winner)AS wins
FROM matches AS m, players AS p
WHERE m.winner = p.id
)+(
SELECT COUNT(m.loser)AS losses
FROM matches AS m, players AS p
WHERE m.winner = p.id
)
) as SUms

FROM players AS p LEFT JOIN matches AS m
ON (m.winner = p.id OR m.loser = p.id)
GROUP BY p.id, p.name
ORDER BY wins;

SELECT (
(
SELECT COUNT(m.winner)AS wins
FROM matches AS m, players AS p
WHERE m.winner = p.id
)+(
SELECT COUNT(m.loser)AS losses
FROM matches AS m, players AS p
WHERE m.winner = p.id
)
) as SUms;



--=========================================
SELECT p.name, COUNT(m.winner)AS wins
FROM matches AS m, players AS p
WHERE m.winner = p.id
GROUP BY p.name;



SELECT p.name, COUNT(m.winner)AS wins
FROM matches AS m, players AS p
LEFT JOIN players AS p2 ON m.loser = p2.id
;



SELECT p.id, p.name,
    SUM(case when m.winner >0 then 1 else 0 end) as Wins
FROM matches AS m, players AS p
GROUP BY p.id, p.name;


--Count the matches of a player
SELECT p.id, p.name,
    SUM(case when m.winner = p.id then 1 else 0 end) as wins,
    SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end) as matches
FROM players AS p LEFT JOIN matches AS m
ON (m.winner = p.id OR m.loser = p.id)
GROUP BY p.id, p.name
ORDER BY wins DESC;

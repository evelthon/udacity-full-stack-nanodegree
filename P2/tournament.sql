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


--Drop view and tables
DROP VIEW IF EXISTS pairings_view;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;


--Create the players table
--This tables must be created before matches table to be able to
--create the REFERENCE

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT
);

--Create table matches
CREATE TABLE matches (
    id SERIAL UNIQUE,
    winner INTEGER REFERENCES players(id),
    loser INTEGER REFERENCES players(id),
    PRIMARY KEY(winner, loser)
    );


--Create view used by swissPairings()
CREATE OR REPLACE VIEW  pairings_view AS
SELECT * FROM (
    SELECT
        p.id,
        p.name,
        SUM(case when m.winner = p.id then 1 else 0 end) as wins,
        SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end) as total_matches
    FROM players AS p LEFT JOIN matches AS m
    ON (m.winner = p.id OR m.loser = p.id)
    GROUP BY p.id, p.name
    ORDER BY wins DESC
    ) AS equal_matches
    WHERE total_matches = (SELECT MAX(all_matches)
FROM(
SELECT
        SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end)
        AS all_matches
        FROM players AS p LEFT JOIN matches AS m
        ON (m.winner = p.id OR m.loser = p.id)
        GROUP BY p.id, p.name
        ) AS max_matches);
        --No need to reorder since the inner query was already ordered by wins.



--As an alternative to VIEW, one could use the FUNCTION below
CREATE OR REPLACE FUNCTION get_pairings()
RETURNS TABLE (
id INTEGER,
name TEXT,
wins BIGINT,
matches BIGINT
) AS $$
BEGIN
RETURN QUERY
    SELECT * FROM (
    SELECT
        p.id,
        p.name,
        SUM(case when m.winner = p.id then 1 else 0 end) as wins,
        SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end) as total_matches
    FROM players AS p LEFT JOIN matches AS m
    ON (m.winner = p.id OR m.loser = p.id)
    GROUP BY p.id, p.name
    ORDER BY wins DESC
    ) AS equal_matches
    WHERE total_matches = (SELECT MAX(all_matches)
FROM(
SELECT
        SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end)
        AS all_matches
        FROM players AS p LEFT JOIN matches AS m
        ON (m.winner = p.id OR m.loser = p.id)
        GROUP BY p.id, p.name
        ) AS max_matches);

END;
$$
LANGUAGE 'plpgsql';

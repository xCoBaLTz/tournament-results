-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (id serial primary key, name text);

create table matches (id serial primary key, winner_id integer references players(id), loser_id integer references players(id));

CREATE VIEW wincounter
AS SELECT players.id, players.name, COUNT(matches.winner_id) AS wins
FROM players
LEFT JOIN matches ON players.id = matches.winner_id
GROUP  BY players.id;

CREATE VIEW matchcounter
AS SELECT players.id, COUNT(matches) AS matches_played
FROM players
LEFT OUTER JOIN matches ON players.id = matches.winner_id OR players.id = matches.loser_id
GROUP BY players.id
ORDER BY matches_played DESC;

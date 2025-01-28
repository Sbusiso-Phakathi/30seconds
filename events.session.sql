-- CREATE TABLE teams(
--     teamid SERIAL PRIMARY KEY,
--     team VARCHAR
-- )

-- CREATE TABLE players(
--     playerid SERIAL PRIMARY KEY,
--     player VARCHAR,
--     teamid INTEGER,
--     FOREIGN KEY (teamid) REFERENCES teams(teamid)
-- )

-- CREATE TABLE cards(
--     cardid SERIAL PRIMARY KEY,
--     card TEXT[]
-- );


-- CREATE TABLE questions (
--     id SERIAL PRIMARY KEY,
--     question TEXT NOT NULL,
--      answer TEXT NOT NULL
--  );
-- CREATE TABLE scores (
--      id SERIAL PRIMARY KEY,
--      team_name TEXT NOT NULL,
--      score INTEGER NOT NULL,
--     played_at TIMESTAMP NOT NULL
--  );

drop TABLE questions cascade
-- Create the teams table
CREATE TABLE teams (
    team_id INT IDENTITY(1,1) PRIMARY KEY,  -- AUTO_INCREMENT equivalent in MSSQL
    team_name NVARCHAR(100) NOT NULL UNIQUE,  -- Enforcing team name uniqueness
    created_at DATETIME2 DEFAULT GETDATE()  -- Default to current timestamp
);

-- Create the teammates table to store player scores
CREATE TABLE teammates (
    teammate_id INT IDENTITY(1,1) PRIMARY KEY,  -- AUTO_INCREMENT equivalent
    team_id INT,  -- Foreign key to teams table
    member_name NVARCHAR(100) NOT NULL,
    score INT DEFAULT 0,  -- Default score for each teammate
    created_at DATETIME2 DEFAULT GETDATE(),  -- Default to current timestamp
    CONSTRAINT FK_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE,  -- Foreign key constraint
    CONSTRAINT unique_team_member UNIQUE (team_id, member_name)  -- Ensuring unique team-member pairs
);

-- Create the questions table to store trivia questions
CREATE TABLE questions (
    question_id INT IDENTITY(1,1) PRIMARY KEY,  -- AUTO_INCREMENT equivalent
    question_text NVARCHAR(MAX) NOT NULL,
    correct_answer NVARCHAR(MAX) NOT NULL
);

-- Create the game_scores table to store the total score of each team per game
CREATE TABLE game_scores (
    game_id INT IDENTITY(1,1) PRIMARY KEY,  -- AUTO_INCREMENT equivalent
    team_id INT,  -- Foreign key to teams table
    total_team_score INT DEFAULT 0,
    played_at DATETIME2 DEFAULT GETDATE(),  -- Default to current timestamp
    CONSTRAINT FK_game_team FOREIGN KEY (team_id) REFERENCES teams(team_id) ON DELETE CASCADE
);

-- Example Insert for Teams
INSERT INTO teams (team_name) VALUES ('Team A');
INSERT INTO teams (team_name) VALUES ('Team B');

-- Example Insert for Teammates (assuming 'team_id' is 1 for 'Team A' and '2' for 'Team B')
INSERT INTO teammates (team_id, member_name, score) VALUES (1, 'Alice', 0);
INSERT INTO teammates (team_id, member_name, score) VALUES (1, 'Bob', 0);
INSERT INTO teammates (team_id, member_name, score) VALUES (2, 'Charlie', 0);
INSERT INTO teammates (team_id, member_name, score) VALUES (2, 'Dave', 0);

-- Update scores after a round
UPDATE teammates SET score = 3 WHERE team_id = 1 AND member_name = 'Alice';
UPDATE teammates SET score = 5 WHERE team_id = 1 AND member_name = 'Bob';

-- Calculate total team score by summing individual scores of the teammates
WITH team_scores AS (
    SELECT team_id, SUM(score) AS total_team_score
    FROM teammates
    WHERE team_id = 1  -- Replace with appropriate team_id
    GROUP BY team_id
)
-- Insert into game_scores with the total score for the team
INSERT INTO game_scores (team_id, total_team_score) 
SELECT team_id, total_team_score FROM team_scores WHERE team_id = 1;

-- Query to get player scores for a team (e.g., 'Team A')
SELECT m.member_name, m.score
FROM teammates m
JOIN teams t ON m.team_id = t.team_id
WHERE t.team_name = 'Team A'
ORDER BY m.score DESC;

-- Query to get the leaderboard based on total team scores
SELECT t.team_name, gs.total_team_score
FROM game_scores gs
JOIN teams t ON gs.team_id = t.team_id
ORDER BY gs.total_team_score DESC;

-- Alter teammates table to add a unique constraint on team-member pairs (already handled above)
-- ALTER TABLE teammates
-- ADD CONSTRAINT unique_team_member UNIQUE (team_id, member_name);

-- Adding team_score column to teams table
ALTER TABLE teams
ADD team_score INT;

CREATE TABLE IF NOT EXISTS hltv_results(
    href VARCHAR(255) NOT NULL,
    rank_team1 INTEGER NOT NULL,
    rank_team2 INTEGER NOT NULL,
    count_matches1 INTEGER NOT NULL,
    count_matches2 INTEGER NOT NULL,
    wr1 INTEGER NOT NULL,
    wr2 INTEGER NOT NULL,
    streak1 INTEGER NOT NULL,
    streak2 INTEGER NOT NULL,
    won INTEGER NOT NULL,
    UNIQUE (href)
    );
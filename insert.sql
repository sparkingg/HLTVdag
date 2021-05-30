INSERT INTO
    hltv_results
VALUES (
    '{{ params.rank1 }}', 
    '{{ params.rank2 }}', 
    '{{ params.count_matches1 }}', 
    '{{ params.count_matches2 }}', 
    '{{ params.wr1 }}', 
    '{{ params.wr2 }}', 
    '{{ params.streak1 }}', 
    '{{ params.streak2 }}',
    '{{ params.won }}' 
)
ON CONFLICT (hltv) DO
    UPDATE
        SET rate = excluded.rate;
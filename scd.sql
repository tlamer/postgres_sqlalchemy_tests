-- new database entries
INSERT INTO dim_customers
    SELECT s.*,nextval('dim_customers_surrogate_seq'),CURRENT_TIMESTAMP
    FROM (SELECT id FROM src_customers EXCEPT SELECT id FROM dim_customers) n
    JOIN src_customers s ON n.id=s.id;

-- temporary table with changes
DROP TABLE IF EXISTS tmp;
CREATE TABLE tmp AS
    SELECT s.id, s.name, s.address, nextval('dim_customers_surrogate_seq'), CURRENT_TIMESTAMP
    FROM src_customers s
    JOIN dim_customers d ON s.id=d.id
    WHERE d.valid_to IS NULL AND (d.name!=s.name OR d.address!=s.address);

-- update timestamps for old entries
UPDATE dim_customers d 
    SET valid_to=CURRENT_TIMESTAMP 
    FROM tmp t 
    WHERE d.id=t.id And d.valid_to IS NULL;

-- merge tables
INSERT INTO dim_customers SELECT * FROM tmp;


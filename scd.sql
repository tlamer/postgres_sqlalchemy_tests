-- new database entries
INSERT INTO dim_customers
    SELECT s.* FROM (SELECT id FROM src_customers EXCEPT SELECT id FROM dim_customers) n
    JOIN src_customers s ON n.id=s.id;

-- changed entries
INSERT INTO dim_customers
    (SELECT s.* FROM
        (SELECT * FROM dim_customers WHERE surrogate=ANY
            -- check every id with largest surrogate number (against the last change of entry)
            (SELECT max(surrogate) FROM dim_customers GROUP BY id)) d
        JOIN src_customers s ON s.id=d.id
        WHERE (d.name!=s.name OR d.address!=s.address));


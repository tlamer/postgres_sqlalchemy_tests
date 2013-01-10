DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS src_customers;
DROP TABLE IF EXISTS tmp;

CREATE TABLE src_customers (
    id integer PRIMARY KEY,
    name varchar(128),
    address varchar(256)
);

CREATE TABLE dim_customers (
    id integer,
    name varchar(128),
    address varchar(256),
    surrogate SERIAL PRIMARY KEY,
    start_date timestamp,
    valid_to timestamp
);

INSERT INTO src_customers (id, name, address) VALUES (1,'peter','kapicova');
INSERT INTO src_customers (id, name, address) VALUES (2,'danko','romanova');
INSERT INTO src_customers (id, name, address) VALUES (3,'stivi','foobar');


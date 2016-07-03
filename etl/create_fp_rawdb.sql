CREATE SCHEMA raw;

CREATE TABLE raw.frontpage_examples (
    exampleid SERIAL PRIMARY KEY,
    hs_url VARCHAR(40) NOT NULL, 
    is_sd BOOLEAN NOT NULL, 
    sd_version VARCHAR(10) NOT NULL, 
    crawlerid INTEGER NOT NULL, 
    t_scrape TIMESTAMP NOT NULL
);

CREATE TABLE raw.frontpage_traces (
    cellid SERIAL PRIMARY KEY,
    exampleid INTEGER NOT NULL,
    ingoing BOOLEAN NOT NULL,
    circuit BIGINT NOT NULL,
    stream BIGINT NOT NULL,
    command VARCHAR(40) NOT NULL,
    length INTEGER NOT NULL,
    t_trace NUMERIC NOT NULL
);

CREATE TABLE raw.crawlers (
    crawlerid SERIAL PRIMARY KEY,
    country VARCHAR(40),
    asn INTEGER,
    ip INET,
    os VARCHAR(40),
    tor_version VARCHAR(20)
);

# ETL 

## Set up the database

Create the database with the commands in `create_db.sql`

Next, after logging back in as `fp_user`, set up the `raw` schema and table structure with `create_fp_rawdb.sql`.

## Upload data into the database

Everytime you have a directory populated with a bunch of files you'd like to put into the database, use the following utility: 

`./update_db.py -d <dirname> -n <true_for_new_crawler>`

This will show a progress bar of the status adding these new data into the database.

# Commence exciting SQL queries

Example:

```
-- Get all rendezvous cells
SELECT circuit, exampleid, command FROM raw.frontpage_traces
WHERE command LIKE '%RENDEZVOUS%';
```

```
-- check for leakage over all traces
-- i.e. do any circuitids appear in multiple examples?
SELECT * FROM 
    (SELECT circuit, count(distinct exampleid) 
     FROM raw.frontpage_traces
     GROUP BY circuit) leak
WHERE leak.count > 1;
```

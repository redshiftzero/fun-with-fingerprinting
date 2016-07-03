#!/usr/local/bin/python3

from contextlib import contextmanager
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import engine_from_config, MetaData
from tqdm import tqdm
import pandas as pd
import argparse
import glob
import pdb

import dbconfig as db


@contextmanager
def safe_session(engine):
    """Context manager for database session"""
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except:
        # if something goes wrong, do not commit
        session.rollback()
        raise
    finally:
        session.close()


class RawStorage(object):
    """Store raw crawled data in the database"""
    def __init__(self):
        """Read current structure from database"""
        self.engine = engine_from_config(db.config, prefix='db.')

        # Generate mappings from existing tables
        metadata = MetaData(schema='raw')
        metadata.reflect(self.engine)
        Base = automap_base(metadata=metadata)
        Base.prepare()

        # Our fundamental objects are:
        self.Example = Base.classes.frontpage_examples
        self.Cell = Base.classes.frontpage_traces
        self.Crawler = Base.classes.crawlers

    def add_cells(self, foreign_key, df):
        """Add raw trace for a given example"""
        cells = []
        for row in df.itertuples():
            cells.append(self.Cell(
                exampleid = foreign_key,
                ingoing = bool(row.Ingoing),
                circuit = int(row.Circuit),
                stream = int(row.Stream),
                command = row.Command,
                length = int(row.Length),
                t_trace = float(row.Timestamp)))
        with safe_session(self.engine) as session:
            session.add_all(cells)

    def add_crawler(self, **kwargs):
        """Insert row for a new crawler"""
        new_crawler = self.Crawler(**kwargs)
        with safe_session(self.engine) as session:
            session.add(new_crawler)
            session.flush()
            inserted_primary_key = new_crawler.crawlerid
        return inserted_primary_key

    def add_example(self, foreign_key, **kwargs):
        """Insert row for a new training example"""
        new_example = self.Example(**kwargs,
                                   crawlerid=foreign_key)
        with safe_session(self.engine) as session:
            session.add(new_example)
            session.flush()
            inserted_primary_key = new_example.exampleid
        return inserted_primary_key


def clean_trace(trace):
    """Load, clean, and import a trace into a pandas DataFrame"""

    df = pd.read_csv(trace, delimiter=' ', header=None)

    # Meaningful column names
    df.columns = ['Timestamp', 'Direction', 'dummy1', 'Circuit', 
                  'dummy2', 'Stream', 'dummy3', 'Command',
                  'dummy4', 'Length']

    # Drop unnecessary columns
    df.drop(['dummy1', 'dummy2', 'dummy3', 'dummy4'], axis=1, inplace=True)

    # Dump trash commas and fix data types
    df['Circuit'] = df['Circuit'].apply(lambda x: x.rstrip(',')).astype('int')
    df['Stream'] = df['Stream'].apply(lambda x: x.rstrip(',')).astype('int')
    df['Command'] = df['Command'].apply(lambda x: x.rstrip(','))
    df['Ingoing'] = df['Direction'].apply(lambda x: True if x == 'INCOMING' else False)
    df['HumanTime'] = pd.to_datetime(df['Timestamp'], unit='s')
    return df


def upload_data(tracedir, new_crawler):
    """Upload all data into database from a given directory"""
    print('[*] Uploading data from {}'.format(tracedir))
    fpdb = RawStorage()

    if new_crawler:
        # dummy info for now
        crawlerid = fpdb.add_crawler(country = 'USA',
                                     os='Ubuntu')
    else:
        crawlerid = 1

    files = glob.glob('{}/*-raw'.format(tracedir))
    for file in tqdm(files):
        df = clean_trace(file)
        # at the moment we can't correlate the hs_urls
        # in the pickle file and traces so hs_url is a dummy
        file_stem = file.split('/')[-1].rstrip('-raw')
        exampleid = fpdb.add_example(crawlerid,
                         is_sd = True if '-' in file_stem else False,
                         hs_url = 'dummy.onion',
                         sd_version = '0.3.8',
                         t_scrape = df['HumanTime'].iloc[0])
        fpdb.add_cells(exampleid, df)

    print('[*] Successful uploading!')
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data-dir', dest='data_directory',
                        type=str,
                        help='location of trace data to upload to database')
    parser.add_argument('-n', '--new-crawler', dest='new_crawler',
                        type=bool,
                        help='is this a new crawler?')

    args = parser.parse_args()

    upload_data(args.data_directory, args.new_crawler)

"""
init_db.py creates a new SQLite database and populates it with data from
publically available IMDb data files.
"""
import argparse
import csv
import gzip
import sqlite3
import sys
from pathlib import Path
from urllib import request

MOVIES_URL = "https://datasets.imdbws.com/title.basics.tsv.gz"


def main(args):
    conn = sqlite3.connect(args.DB_FILE)
    _create_movies_table(conn)
    _populate_movies_table(conn)
    _create_fulltextsearch(conn)
    _populate_fulltextsearch(conn)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("DB_FILE", type=Path, help="Path to SQLite file")

    return parser.parse_args()


def _create_movies_table(conn):
    with conn:
        query = """CREATE TABLE IF NOT EXISTS Movies(
            id INTEGER PRIMARY KEY,
            tconst TEXT NOT NULL,
            primary_title TEXT NOT NULL,
            original_title TEXT
            );"""
        conn.execute(query)


def _populate_movies_table(conn):
    with request.urlopen(MOVIES_URL) as file:
        with gzip.open(file, "rt", newline="") as tsvfile:
            reader = csv.reader(tsvfile, delimiter="\t")
            next(reader)  # skip header row
            query = """
            INSERT INTO Movies(tconst, primary_title, original_title)
            VALUES(?, ?, ?)"""
            with conn:
                conn.executemany(
                    query,
                    [(row[0], row[2], row[3]) for row in reader],
                )


def _create_fulltextsearch(conn):
    with conn:
        query = """CREATE VIRTUAL TABLE Titles
        USING FTS5(id, primary_title, original_title)"""
        conn.execute(query)


def _populate_fulltextsearch(conn):
    with conn:
        query = """
        INSERT INTO Titles(id, primary_title, original_title)
        SELECT id, primary_title, original_title
        FROM Movies"""
        conn.execute(query)


if __name__ == "__main__":
    args = _parse_args()
    sys.exit(main(args))

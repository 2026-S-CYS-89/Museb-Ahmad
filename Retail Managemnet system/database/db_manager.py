"""
database/db_manager.py
Database connection manager — SQLite single file
"""
import sqlite3
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR   = Path(__file__).resolve().parent.parent
DB_PATH    = BASE_DIR / "retail_store.db"
SCHEMA_SQL = Path(__file__).resolve().parent / "schema.sql"


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conn = None
        return cls._instance

    def connect(self):
        if self._conn is not None:
            return
        self._conn = sqlite3.connect(str(DB_PATH))
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._init_schema()
        logger.info("DB connected: %s", DB_PATH)

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def fetch_one(self, sql, params=()):
        return self._conn.execute(sql, params).fetchone()

    def fetch_all(self, sql, params=()):
        return self._conn.execute(sql, params).fetchall()

    def execute_write(self, sql, params=()):
        try:
            cur = self._conn.execute(sql, params)
            self._conn.commit()
            return cur.lastrowid or cur.rowcount
        except sqlite3.Error as e:
            self._conn.rollback()
            raise e

    def execute_many(self, sql, params_list):
        try:
            cur = self._conn.executemany(sql, params_list)
            self._conn.commit()
            return cur.rowcount
        except sqlite3.Error as e:
            self._conn.rollback()
            raise e

    @property
    def connection(self):
        return self._conn

    def _init_schema(self):
        row = self._conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"
        ).fetchone()
        if row is None:
            script = SCHEMA_SQL.read_text(encoding="utf-8")
            self._conn.executescript(script)
            self._conn.commit()
            logger.info("Schema initialised.")


db = DatabaseManager()

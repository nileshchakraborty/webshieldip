import psycopg
import os

DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(DB_URL)

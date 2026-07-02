import os
import psycopg

# Connects to the database and returns the cursor
def get_connection():
  db_url = os.environ["DB_URL"]
  return psycopg.connect(db_url)

import psycopg

# Connects to the database and returns the cursor
def get_connection(db_uri):
  return psycopg.connect(db_uri)

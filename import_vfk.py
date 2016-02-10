
import sys
import os
import psycopg2
import cuzak_tools
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception, e:
        logging.error("Unable to connect to da database ...")
        raise e

    schema = os.environ.get('DATABASE_SCHEMA', 'public')
    cuzak_tools.createSchema(conn, schema)

    cur = conn.cursor()

    deleteExisting = len(sys.argv) > 2 and sys.argv[2] == '1'

    if deleteExisting:
        cuzak_tools.removeExistingTables(cur, schema)
        conn.commit()

    cuzak_tools.parse(sys.argv[1], cur, schema)

    logging.error("done ...")
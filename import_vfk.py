
import sys
import os
import psycopg2
import cuzak_tools


if __name__ == "__main__":

    schema = os.environ.get('DATABASE_SCHEMA', 'public')
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception, e:
        print "Unable to connect to da database ..."
        raise e

    cur = conn.cursor()

    deleteExisting = len(sys.argv) > 2 and sys.argv[2] == '1'

    if deleteExisting:
        cuzak_tools.removeExistingTables(cur, schema)
        conn.commit()

    cuzak_tools.parse(sys.argv[1], cur)
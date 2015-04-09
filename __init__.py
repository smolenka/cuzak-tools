
from nvf2sql import ChangesSolvingImportVFKParser

def removeExistingTables(cursor, schema):
    print "Deleting tables..."

    q = "select tablename from pg_tables where schemaname=%s"
    cursor.execute(q, (schema, ))
    tables=cursor.fetchall()

    for table in tables:
        if not table[0] in ('spatial_ref_sys', 'geometry_columns'):
            cursor.execute("DROP TABLE %s cascade;" % table[0])

def parse(file_name, cur):
    # parse input file and fill the DB
    with codecs.open(file_name, encoding='iso-8859-2') as f:
        ChangesSolvingImportVFKParser(f, cur)


if __name__ == "__main__":
    # tohle je tu proto, aby se to dalo spustit (ne v ramci jineho projektu)
    import sys
    import os
    import codecs
    import psycopg2

    schema = os.environ.get('DATABASE_SCHEMA', 'public')
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception, e:
        print "Unable to connect to da database ..."
        raise e

    cur = conn.cursor()

    deleteExisting = len(sys.argv) > 2 and sys.argv[2] == '1'

    if deleteExisting:
        removeExistingTables(cur, schema)
        conn.commit()

    parse(sys.argv[1], cur)

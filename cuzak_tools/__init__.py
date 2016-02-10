
import logging
import codecs
import psycopg2
from importer import ChangesSolvingImportVFKParser


def createSchema(conn, schema):
    cursor = conn.cursor()
    try:
        logging.info("ensuring existence schema %s..." % schema)
        cursor.execute("CREATE SCHEMA IF NOT EXISTS %s" % schema)
        conn.commit()
    except psycopg2.Error, e:
        logging.exception(e)
        conn.rollback()
    finally:
        cursor.close()
    

def removeExistingTables(conn, schema):
    logging.info("Deleting tables...")
    cursor = conn.cursor()
    try:
        q = "select tablename from pg_tables where schemaname=%s"
        cursor.execute(q, (schema, ))
        tables=cursor.fetchall()

        for table in tables:
            if not table[0] in ('spatial_ref_sys', 'geometry_columns'):
                cursor.execute("DROP TABLE %s cascade;" % table[0])
        conn.commit()
    except psycopg2.Error, e:
        logging.exception(e)
        conn.rollback()
    finally:
        cursor.close()

def parse(file_name, cur, schema='public'):
    # parse input file and fill the DB
    with codecs.open(file_name, encoding='iso-8859-2') as f:
        ChangesSolvingImportVFKParser(f, cur, schema)


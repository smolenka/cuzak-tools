
import codecs
from importer import ChangesSolvingImportVFKParser


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


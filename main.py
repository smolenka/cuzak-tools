
import nvf2sql
import psycopg2
import geom
import codecs
import sys
import os


def main(file_name, deleteExisting=False):
    schema = 'public'
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception, e:
        print "I am unable to connect to the database ..."
        raise e

    cur = conn.cursor()

    if deleteExisting:
        _removeExistingTables(cur)

    # parse input file and fill the DB
    with codecs.open(file_name, encoding='iso-8859-2') as f:
        nvf2sql.ImportVFKParser(f, cur)

    conn.commit()

    print "Geometry HP..."
    geom.AddGeometryL('public', 'hp', cur)
    conn.commit()

    print "Geometry OB..."
    geom.AddGeometryL('public','ob',cur)
    conn.commit()

    print "Geometry DPM..."
    geom.AddGeometryL('public','dpm',cur)
    conn.commit()

    print "Geometry PAR..."
    cur.execute('CREATE TABLE IF NOT EXISTS par (id serial);')
    geom.AddGeometryP(schema,'par','hp', cur)
    conn.commit()

    print "Geometry BUD..."
    cur.execute('CREATE TABLE IF NOT EXISTS bud (id numeric(30));')
    geom.AddGeometryP('public', 'bud', 'ob', cur)
    conn.commit()

#     funkce.AddColumn(cur,'par','drupoz_nazev','varchar(60)','drupoz','nazev','kod','drupoz_kod')
#     funkce.AddColumn(cur,'par','zpvypo_nazev','varchar(60)','zpvypo','nazev','kod','zpvypa_kod')
#     funkce.SetUpParcelNumber(cur)
#     funkce.SetUpBuildingNumber(cur)
    print "Complete."


def _removeExistingTables(cursor):
    print "Deleting tables..."

    cursor.execute("select tablename from pg_tables where schemaname='public'")
    tables=cursor.fetchall()

    for table in tables:
        if not table[0] in ('spatial_ref_sys', 'geometry_columns'):
            cursor.execute("DROP TABLE %s cascade;" % table[0])


if __name__ == "__main__":
    main(sys.argv[1])

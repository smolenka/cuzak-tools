
import psycopg2

def addGeometryColumn(geomtype, schema, tab, col, cur):
    q = "select AddGeometryColumn('%s','%s','%s',2065,'%s',2);"
    try:
        cur.execute(q % (schema, tab, col, geomtype))  # zkusime pridat
        cur.connection.commit()
    except psycopg2.ProgrammingError:   # kdy chyba, uz tam je
        cur.connection.rollback()   # tak vratime zmeny - rollback
        

def pointListString(points):
    strs = []
    for p in points:
        # minusy protoze zaporny krovak
        strs.append('-%s -%s' % (p[0], p[1]))
    return ','.join(strs)
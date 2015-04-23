
import psycopg2

def addGeometryColumn(geomtype, schema, tab, col, cur):
    q = "select AddGeometryColumn('%s','%s','%s',2065,'%s',2);"
    try:
        cur.execute(q % (schema, tab, col, geomtype))  # zkusime pridat
        cur.connection.commit()
    except psycopg2.ProgrammingError:   # kdy chyba, uz tam je
        cur.connection.rollback()   # tak vratime zmeny - rollback

def point2GeoJSON(p):
    return '{"type":"Point","coordinates":[-%s,-%s]}' % p

def lineSet2MultiLineStringGeoJSON(lineset):
    s = []
    for l in lineset:
        l = '[[-%s,-%s],[-%s,-%s]]' % (l[0][0], l[0][1], l[1][0], l[1][1])
        s.append(l)
    return '{"type":"MultiLineString","coordinates": [%s]}' % ',\n'.join(s)

def pointListString(points):
    strs = []
    for p in points:
        # minusy protoze zaporny krovak
        strs.append('-%s -%s' % (p[0], p[1]))
    return ','.join(strs)

def lines2LineString(points):
    """
    Z paru bodu v tuples udela Linestring
    """
    return 'LINESTRING(%s)' % pointListString(points)

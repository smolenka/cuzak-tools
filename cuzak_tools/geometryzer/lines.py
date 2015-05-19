
import logging
import utils

def addLinesGeometry(schema, tab, cur):
    utils.addGeometryColumn('LINESTRING', schema, 'lines', 'geom', cur)

    cur.execute('select id from %s' % tab)
    for i in cur.fetchall():
        lines = _getLine(i[0], tab, cur)
        for l in lines:
            addLine(l, {'zdroj': 0, 'zdrojid': i[0] }, cur)

def addLine(points, attrs, cur):
    q = """INSERT INTO lines (geom, %s) VALUES (
        ST_GeomFromText('LINESTRING(%s)',2065), %s
    ) RETURNING id
    """
    attsconcat = ','.join([a for a in attrs.keys()])
    substitutes = ','.join(['%s' for _ in range(len(attrs))])
    query = q % (attsconcat, utils.pointListString(points), substitutes)
    try:
        cur.execute(query, attrs.values())
        return cur.fetchone()[0]
    except Exception, e:
        logging.exception(e)

def linieParcely(pid, cur):
    lines = []
    # vyberu vsechny hrany, ktere maji par_id_1 nebo par_id_2 rovno parId
    cur.execute("""
    select id as idckalinii from hp where par_id_1 = %s OR par_id_2 = %s
    """, (pid, pid))
    for lineId in cur.fetchall():
        lines.extend(_getLine(lineId[0], 'hp', cur))
    # a udelam z nich GeoJSON multilinii
    return utils.lineSet2MultiLineStringGeoJSON(lines)

def _lineAlreadyExists(itemid, zdrojid, zdroj, cur):
    q = "SELECT COUNT(*) FROM lines WHERE zdrojid=%s AND zdroj=%s"
    cur.execute(q, (str(itemid), zdroj))
    contains = cur.fetchone()
    return contains[0] > 0

def _getLine(itemid, tab, cur):
    sql="""select souradnice_y,souradnice_x from sobr where id in
    (select bp_id from sbp where %s_id=%s)""" % (tab, itemid)
    cur.execute(sql)
    rows=cur.fetchall()
    if len(rows) == 0:
        return ()
    if len(rows) > 2:
        return _getMultiline(itemid, cur)
    else:
        return [(rows[0], rows[1])]

def _getMultiline(itemid, cur):
    logging.warn('WARN: multiline: %s' % itemid)
    lines = []
    q = '''SELECT souradnice_y, souradnice_x
    FROM sobr o INNER JOIN sbp s ON o.id=s.bp_id
    WHERE s.hp_id=%s ORDER BY poradove_cislo_bodu ASC
    '''
    cur.execute(q, (itemid, ))
    points = cur.fetchall()
    for idx in range(len(points)-1):
        lines.append((points[idx], points[idx+1]))


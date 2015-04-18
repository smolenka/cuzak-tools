
import utils

def addLinesGeometry(schema, tab, cur):
    utils.addGeometryColumn('LINESTRING', schema, 'lines', 'geom', cur)

    cur.execute('select id from %s' % tab)

    for i in cur.fetchall():
        _solveLine(i[0], tab, cur)
        
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
        print str(e)
        
def _lineAlreadyExists(itemid, zdrojid, zdroj, cur):
    q = "SELECT COUNT(*) FROM lines WHERE zdrojid=%s AND zdroj=%s"
    cur.execute(q, (str(itemid), zdroj))
    contains = cur.fetchone()
    return contains[0] > 0
        
def _solveLine(itemid, tab, cur):
    if _lineAlreadyExists(itemid, itemid, 0, cur):
        return
    sql="""select souradnice_y,souradnice_x from sobr where id in
    (select bp_id from sbp where %s_id=%s)""" % (tab, itemid)
    cur.execute(sql)
    rows=cur.fetchall()
    if len(rows) == 0:
        return
    if len(rows) > 2:
        _solveMultiline(itemid, cur)
    else:
        addLine(rows, {'zdroj': 0, 'zdrojid': itemid }, cur)
    
def _solveMultiline(itemid, cur):
    print 'WARN: multiline: %s' % itemid
    
    q = '''SELECT souradnice_y, souradnice_x 
    FROM sobr o INNER JOIN sbp s ON o.id=s.bp_id 
    WHERE s.hp_id=%s ORDER BY poradove_cislo_bodu ASC
    '''
    cur.execute(q, (itemid, ))
    points = cur.fetchall()
    for idx in range(len(points)-1):
        addLine([points[idx], points[idx+1]], {
            'zdroj': 0, 'zdrojid': itemid
        }, cur)
        


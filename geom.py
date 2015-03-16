
def Update_geom(points):
    strs = []
    for p in points:
        # minusy protoze zaporny krovak
        strs.append('-%s -%s' % (p[0], p[1]))
    return ','.join(strs)

def AddGeometryL(schema, tab, cur):
    q = "select AddGeometryColumn('%s','%s','geom%s',2065,'LINESTRING',2);" % (schema, tab, tab)
    cur.execute(q)

    cur.execute('select id from %s' % tab)
    tab_ids=cur.fetchall()

    for i in tab_ids:
        sql="""select souradnice_y,souradnice_x from sobr where id in
        (select bp_id from sbp where %s_id=%s)""" % (tab, i[0])
        cur.execute(sql)
        rows=cur.fetchall()
        if len(rows) == 0:
            continue
        sqlt="""UPDATE %s SET geom%s=ST_GeomFromText(
            'LINESTRING(%s)'
        ,2065) WHERE id=%s""" % (tab, tab, Update_geom(rows), i[0])

        try:
            cur.execute(sqlt)
        except Exception, e:
            print str(e)

def AddGeometryP(schema,tab,tab_L,cur):
    q = "select AddGeometryColumn('%s','%s','geom%s',2065,'POLYGON',2);" % (schema, tab, tab)
    cur.execute(q)

    cur.execute('select id from %s' % tab)
    tab_ids=cur.fetchall()
    for p in tab_ids:
        createGeometry(tab, tab_L, p[0], cur)

    # get par_ids in tab_L
    if tab=='par':
        cur.execute('select DISTINCT par_id_1 from %s' % tab_L)
        for p in cur.fetchall():
            createGeometry(tab, tab_L, p[0], cur)
        cur.execute('select DISTINCT par_id_2 from %s' % tab_L)
        for p in cur.fetchall():
            createGeometry(tab, tab_L, p[0], cur)
    elif tab=='bud':
        cur.execute('select DISTINCT bud_id from %s' % tab_L)
        for p in cur.fetchall():
            createGeometry(tab, tab_L, p[0], cur)

def _hranaObsahujiciBod(idHran, bod, tabulkaHran, cur):
    for idx, h in enumerate(idHran): # najde tu, obsahujici currpoint
        sql="select ST_Distance((select geom%s from %s where id=%s),'%s')" % (tabulkaHran, tabulkaHran, h[0], bod)
        cur.execute(sql)
        vzdalenost = cur.fetchone()[0]
        if vzdalenost == 0:
            return idx
    return None

def _PGPoint2Floats(point, cur):
    cur.execute("select ST_X('%s')" % point)
    x = cur.fetchone()[0]
    cur.execute("select ST_Y('%s')" % point)
    y = cur.fetchone()[0]
    return (x, y)

def _hranyParcely(hp_ids, tab, tab_L, cur):
    hp_points = []
    for idHr in hp_ids: # naplni hp_points body
        cur.execute("select ST_PointN(geom%s,1) from %s where id=%s" % (tab_L, tab_L, idHr[0]))
        p1=cur.fetchone()[0]
        cur.execute("select ST_PointN(geom%s,2) from %s where id=%s" % (tab_L, tab_L, idHr[0]))
        p2=cur.fetchone()[0]
        hp_points.append([p1,p2])

    return hp_points

def _2PolygonQuery(polydata):
    return "ST_GeomFromText('POLYGON((%s))',2065)" % Update_geom(polydata)

def _odNejvnejsnejsihoPoNejvnitrnejsi(PolyCoords, cur):
    first=0
    for ii in range(len(PolyCoords)):
        for jj in range(ii+1,len(PolyCoords)):
            cur.execute("select ST_Contains(%s,%s)" % \
                (_2PolygonQuery(PolyCoords[ii]), _2PolygonQuery(PolyCoords[jj])))
            if cur.fetchone()[0]==1:
                first=1
                pom=PolyCoords[0]
                PolyCoords[0]=PolyCoords[ii]
                PolyCoords[ii]=pom
                break
        if first==1:
            break

def createGeometry(tab, tab_L, par_id, cur):
    if par_id == None: return

    cur.execute("SELECT id, geom%s FROM %s WHERE id='%s'" % (tab, tab, par_id))
    existing = cur.fetchone()
    if not existing:
        cur.execute("INSERT INTO %s VALUES('%s');" % (tab, par_id))
    elif existing[1]:
        # uz mame geometrii vyplnenou ...
        return

    if tab=='par':
        sql="select id from %s where (par_id_1=%s) or (par_id_2=%s);" % (tab_L, par_id, par_id)
    elif tab=='bud':
        sql="select id from %s where (bud_id=%s) and (obrbud_type='OB');" % (tab_L, par_id)
    cur.execute(sql)
    hp_ids = cur.fetchall()  #seznam id hran k dane parcele

    hp_points = _hranyParcely(hp_ids, tab, tab_L, cur)  # nacte hranice parcely

    PolyCoords=[]

    sp=-1
    while 1:
        if len(hp_ids)==0:
            break
        sp=sp+1
        PolyCoords.append([])
        x, y = _PGPoint2Floats(hp_points[0][0], cur)
        PolyCoords[sp].append([-x,-y])
        currpoint = hp_points[0][0]
        hp_ids.pop(0)       # popne hranu
        hp_points.pop(0)    # vezme 1. bod a popne ho ze seznamu

        for _ in range(len(hp_ids)):    # pro vsechny hrany
            ind = _hranaObsahujiciBod(hp_ids, currpoint, tab_L, cur)
            if ind == None: break

            for foo in range(2): # pro oba body nalezene hrany
                x, y = _PGPoint2Floats(hp_points[ind][foo], cur)
                try:
                    PolyCoords[sp].index([-x,-y])   # zkus jestli tam uz je
                except ValueError:                  # kdyz ne
                    PolyCoords[sp].append([-x,-y])  # prida ho do polygonu
                    currpoint=hp_points[ind][foo]   # posune currpoint
                    hp_ids.pop(ind)
                    hp_points.pop(ind)
                    break
        PolyCoords[sp].append(PolyCoords[sp][0])    # uzavre polygon (1.bod)

    # odstranime neuzavrene polygony (jak muzou vzniknout? Chyba v datech?
    checked = []
    for p in PolyCoords:
        if(len(p)) > 3:
            checked.append(p)
    if len(checked) == 0:
        return
    PolyCoords = checked

    # Prehazuje poradi od nejvnejsnejsiho po nejvnitrnejsi
    if len(PolyCoords)>1:
        _odNejvnejsnejsihoPoNejvnitrnejsi(PolyCoords, cur)

    # udela polygon
    parts = []
    for pc in PolyCoords:
        parts.append('(%s)' % Update_geom(pc))

    # a ulozi ho
    sqlt="UPDATE %s SET geom%s=ST_GeomFromText('POLYGON(%s)',2065) WHERE id='%s'" % \
        (tab, tab, ','.join(parts), par_id)
    try:
        cur.execute(sqlt)
    except Exception, e:
        print str(e)

    cur.connection.commit()





    
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
    cur.execute('CREATE TABLE IF NOT EXISTS %s (id VARCHAR(30));' % tab)
    q = "select AddGeometryColumn('%s','%s','geom%s',2065,'POLYGON',2);" % (schema, tab, tab)
    cur.execute(q)

    cur.execute('select id from %s' % tab)
    tab_ids=cur.fetchall()
    for i in tab_ids:
        createGeometry(tab, tab_L, i, cur)
        
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
        
def createGeometry(tab, tab_L, par_id, cur):
    cur.execute("SELECT id, geom%s FROM %s WHERE id='%s'" % (tab, tab, par_id))
    existing = cur.fetchone()
    if not existing:
        cur.execute("INSERT INTO %s VALUES('%s');" % (tab, par_id))
    elif existing[1]:
        # uz mame geometrii vyplnenou ...
        return
            
    hp_points=[]
    if tab=='par':
        sql="select id from %s where (par_id_1=%s) or (par_id_2=%s);" % (tab_L, par_id, par_id)
    elif tab=='bud':
        sql="select id from %s where (bud_id=%s) and (obrbud_type='ob');" % (tab_L, par_id)
        
    cur.execute(sql)
    hp_ids=cur.fetchall() #seznam hp k dane parcele
    for j in hp_ids: #naplni hp_points body
        cur.execute("select ST_PointN(geom%s,1) from %s where id=%s" % (tab_L, tab_L, j[0]))
        p1=cur.fetchone()[0]
        cur.execute("select ST_PointN(geom%s,2) from %s where id=%s" % (tab_L, tab_L, j[0]))
        p2=cur.fetchone()[0]
        hp_points.append([p1,p2])

    PolyCoords=[]

    sp=-1
    while 1:
        if len(hp_ids)==0:
            break
        sp=sp+1
        PolyCoords.append([])
        # print hp_points[0][0]
        cur.execute("select ST_X('"+hp_points[0][0]+"')")
        x=cur.fetchone()[0]
        cur.execute("select ST_Y('"+hp_points[0][0]+"')")
        y=cur.fetchone()[0]
        PolyCoords[sp].append([-x,-y])
        point=hp_points[0][0]
        hp_ids.pop(0)
        hp_points.pop(0)

        dalsi = 0
        for k in range(len(hp_ids)):
            for ind,h in enumerate(hp_ids): #najde hp, obsahujici bod point
                sql="select ST_Distance((select geom%s from %s where id=%s),'%s')" % (tab_L, tab_L, h[0], point)
                cur.execute(sql)
                if cur.fetchone()[0]==0:
                    dalsi=1
                    break
            if dalsi==0:
                break
            dalsi=0
            for foo in range(2):
                cur.execute("select ST_X('"+hp_points[ind][foo]+"')")
                x=cur.fetchone()[0]
                cur.execute("select ST_Y('"+hp_points[ind][foo]+"')")
                y=cur.fetchone()[0]
                try:
                    PolyCoords[sp].index([-x,-y])
                except:
                    PolyCoords[sp].append([-x,-y])
                    point=hp_points[ind][foo]
                    hp_ids.pop(ind)
                    hp_points.pop(ind)
                    break
        PolyCoords[sp].append(PolyCoords[sp][0])

    poly=[]
    for p in PolyCoords:
        if(len(p)) < 4:
            continue    # neuzavrena cara
        sqlt="select ST_GeomFromText('POLYGON((%s))',2065)" % Update_geom(p)
        try:
            cur.execute(sqlt)
            poly.append(cur.fetchone()[0])
        except Exception, e:
            print str(e)
#     if len(poly)>1:
#         first=0
#         for ii in range(len(poly)):
#             for jj in range(ii+1,len(poly)):
#                 cur.execute("select ST_Contains('"+poly[ii]+"','"+poly[jj]+"')")
#                 if cur.fetchone()[0]==1:
#                     first=1
#                     pom=PolyCoords[0]
#                     PolyCoords[0]=PolyCoords[ii]
#                     PolyCoords[ii]=pom
#                     break
#             if first==1:
#                 break
    
    parts = []
    for pc in PolyCoords:
        if(len(p)) < 4:
            continue    # neuzavrena cara
        parts.append('(%s)' % Update_geom(pc))
    if len(parts) == 0:
        return
    sqlt="UPDATE %s SET geom%s=ST_GeomFromText('POLYGON(%s)',2065) WHERE id='%s'" % (tab, tab, ','.join(parts), par_id)
    
    try:
        cur.execute(sqlt)
    except Exception, e:
        print str(e)
        
    cur.connection.commit()





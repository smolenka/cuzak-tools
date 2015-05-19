
def createPolygonGeometry(multilinie, cur):
    """
    """
    cur.execute("""
    SELECT ST_AsGeoJson(ST_Polygonize(ST_GeomFromGeoJSON(%s)))
    """, (multilinie, ))
    moznePolygony = cur.fetchone()[0]

    cur.execute("""
    SELECT ST_NumGeometries(ST_GeomFromGeoJSON(%s))
    """, (moznePolygony, ))
    pocet = cur.fetchone()[0]

    if pocet > 1:
        idx = _najdiTenSpravnyNeDiru(moznePolygony, pocet, cur)
    else:
        idx = 1

    cur.execute("""
    SELECT ST_AsGeoJson(ST_GeometryN(ST_GeomFromGeoJSON(%s), %s))
    """, (moznePolygony, idx))

    return cur.fetchone()[0]

# -------------------------- private funcs ------------------------------

def _najdiTenSpravnyNeDiru(moznePolygony, jejichPocet, cur):
    moznosti = range(jejichPocet)
    while len(moznosti) > 1:
        testovany = moznosti.pop()
        obsahujeOstatni = True
        for i in moznosti:
            q = """
SELECT ST_Within(
  ST_GeometryN(ST_GeomFromGeoJSON(%s), %s),
  ST_MakePolygon(ST_ExteriorRing(ST_GeometryN(ST_GeomFromGeoJSON(%s), %s)))
)
            """
            pars = (moznePolygony, i+1, moznePolygony, testovany+1)
            cur.execute(q, pars)
#           print cur.mogrify(q, pars)
            jeUvnitr = cur.fetchone()[0]
            if not jeUvnitr:
                obsahujeOstatni = False
        if obsahujeOstatni:
            return testovany + 1
    return moznosti.pop() + 1



def createPolygonGeometry(parcelID, tab, tab_L, cur):
    cur.execute(_polygonizeQ, (parcelID, parcelID))
    moznePolygony = cur.fetchone()[0]
    cur.execute(_pocetQ, (moznePolygony, ))
    pocet = cur.fetchone()[0]
    if pocet > 1:
        idx = _najdiTenSpravnyNeDiru(moznePolygony, pocet, cur)
        cur.execute(_updateQ, (moznePolygony, idx, str(parcelID)))
    else:
        cur.execute(_updateQ, (moznePolygony, 1, str(parcelID)))
            
# -------------------------- private funcs ------------------------------
_updateQ = """
UPDATE parcely
SET geom = ST_SetSRID(ST_GeometryN(ST_GeomFromGeoJSON(%s), %s), 2065)
WHERE zdrojid = %s
"""

_polygonizeQ = """
SELECT ST_AsGeoJson(ST_Polygonize(seznamlinii.multip)) as pol FROM (
    SELECT ST_Multi(ST_Collect(linie.jakotext)) as multip FROM (
        SELECT ST_AsText(geom) as jakotext FROM lines as l WHERE zdroj = 0 AND zdrojid IN (
            select text(id) as idckalinii from hp where par_id_1 = %s OR par_id_2 = %s
        )
    ) AS linie
) AS seznamlinii
"""

_pocetQ = """
SELECT ST_NumGeometries(ST_GeomFromGeoJSON(%s))
"""

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
            cur.execute(q, (moznePolygony, i+1, moznePolygony, testovany+1))
#             print cur.mogrify(q, (moznePolygony, i+1, moznePolygony, testovany+1))
            jeUvnitr = cur.fetchone()[0]
            if not jeUvnitr:
                obsahujeOstatni = False
        if obsahujeOstatni:
            return testovany + 1
    return moznosti.pop() + 1
        

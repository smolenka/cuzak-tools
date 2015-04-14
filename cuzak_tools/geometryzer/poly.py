
def createPolygonGeometry(parcelID, tab, tab_L, cur):
    cur.execute(_q, (parcelID, parcelID, str(parcelID)))
            
# -------------------------- private funcs ------------------------------
_q = """
UPDATE parcely SET geom = ST_SetSRID(p.pol, 2065) FROM (
    SELECT ST_GeometryN(ST_Polygonize(seznamlinii.multip), 1) as pol FROM (
        SELECT ST_Multi(ST_Collect(linie.jakotext)) as multip FROM (
            SELECT ST_AsText(geom) as jakotext FROM lines as l WHERE zdroj = 0 AND zdrojid IN (
                select text(id) as idckalinii from hp where par_id_1 = %s OR par_id_2 = %s
            )
        ) AS linie
    ) AS seznamlinii
) p
WHERE zdrojid = %s
"""

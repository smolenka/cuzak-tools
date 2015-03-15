import dbconstraints

def removeExistingTables(cursor):
    print "Deleting tables..."
    
    cursor.execute("select tablename from pg_tables where schemaname='public'")
    tables=cursor.fetchall()
    
    for table in tables:
        if not table[0] in ('spatial_ref_sys', 'geometry_columns'):
            cursor.execute("DROP TABLE %s cascade;" % table[0])
         
   
def createPK(table, cursor):
    """ Udela primarni klic na dane tabulce podle info v dbconstraints.py """
    try:
        s = 'ALTER TABLE %s ADD CONSTRAINT %s_pk PRIMARY KEY(%s);'
        tname = table.lower()
        pks = dbconstraints.PrimKeys[table]
        cursor.execute(s % (tname, tname, ','.join(pks)))
    except (IndexError, KeyError):
        print 'table %s nema PK? Divne ...' % table


def createFKs(table, cursor):
    qtmp = 'ALTER TABLE %s ADD CONSTRAINT %s FOREIGN KEY(%s) REFERENCES %s(%s)'
    try:
        keys = dbconstraints.ForKeys[table]
        for idx, k in enumerate(keys):
            refTable, col, refCol = k
            q = qtmp % (table.lower(), 'FK_%i' % idx, col, refTable, refCol)
            cursor.execute(q)
    except (IndexError, KeyError):
        pass
      

######    ADD COLUMN
def AddColumn(cur,tab,col,typ,tab2,col2,id2,id1):
    cur.execute("ALTER TABLE "+tab+" ADD COLUMN "+col+" "+typ)
    cur.execute(" UPDATE "+tab+" "+""" 
                    SET """+col+" = ( SELECT "+col2+" "+"""
                    FROM """+tab2+" "+"""
                    WHERE """+tab2+"."+id2+" = "+tab+"."+id1+""") 
                    WHERE EXISTS
                    ( SELECT """+col2+" "+"""
                    FROM """+tab2+" "+"""
                    WHERE """+tab2+"."+id2+" = "+tab+"."+id1+")")

## *********** doplnil Jiri Petrak dne 11.05.2007 ******************* 

###     SLOZENI PARCELNIHO CISLA A PRIDANI DO TABULKY PAR
def SetUpParcelNumber(cursor):
    print 'Skladani parcelnich cisel... '
##    cursor.execute("ALTER TABLE par DROP COLUMN par_cislo_komplet")
    cursor.execute("ALTER TABLE par ADD COLUMN par_cislo_komplet varchar(15)")
    cursor.execute("""SELECT druh_cislovani_par, kmenove_cislo_par, poddeleni_cisla_par
                    FROM par
                    ORDER BY kmenove_cislo_par""")
    result=cursor.fetchall()
    for row in result:                  # skladani parcelniho cisla:
        druh_cis_par = '%s' % (row[0])  # preformatovani na retezec
        kmen_cis_par = '%s' % (row[1])  # - kvuli skladani do query
        podd_cis_par = '%s' % (row[2])
        if row[2]==None:                # neexistuje poddeleni par. cisla
            par_c = kmen_cis_par
            podd_cis_par='IS NULL'
        else:                           # existuje poddeleni par. cisla
            par_c = kmen_cis_par+'/'+podd_cis_par
            podd_cis_par = '= '+podd_cis_par
        if row[0]==1:                   # jedna se o stavebni parcelu
            par_c='St. '+par_c
        
        query=""" UPDATE par  
                    SET par_cislo_komplet = '"""+par_c+"' "+"""
                    WHERE druh_cislovani_par = """+druh_cis_par+" "+""" AND
                        kmenove_cislo_par = """+kmen_cis_par+" "+""" AND
                        poddeleni_cisla_par """+podd_cis_par+" "
##        print query
        cursor.execute(query)

##      SLOZENI CISLA BUDOVY
def SetUpBuildingNumber(cursor):
    print 'Skladani cisel budov... '
##    cursor.execute("ALTER TABLE bud DROP COLUMN cislo_bud_komplet")
    cursor.execute("ALTER TABLE bud ADD COLUMN cislo_bud_komplet varchar(15)")
    cursor.execute("""SELECT tb.zkratka, bud.cislo_domovni, bud.id
                    FROM bud, typbud tb
                    WHERE tb.kod=bud.typbud_kod
                    ORDER BY bud.cislo_domovni""")
    result=cursor.fetchall()
    for row in result:
        typbud = '%s' % (row[0])
        cislo = '%s' % (row[1])
        bud_id = '%s' % (row[2])
        if cislo != 'None':
            cis_bud = typbud+' '+cislo
        else:
            cis_bud = typbud

        query = """UPDATE bud
                SET cislo_bud_komplet = '"""+cis_bud+"""'
                WHERE id = """+bud_id

        cursor.execute(query)

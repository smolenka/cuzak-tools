from init import *

def removeExistingTables(cursor):
    print "Deleting tables..."
    
    cursor.execute("select tablename from pg_tables where schemaname='public'")
    tables=cursor.fetchall()
    
    for table in tables:
        if not table[0] in ('spatial_ref_sys', 'geometry_columns'):
            cursor.execute("DROP TABLE %s cascade;" % table[0])
            
def createPK(table, cursor):
    try:
        s = 'ALTER TABLE %s ADD CONSTRAINT %s_pk PRIMARY KEY(%s);'
        tname = table.lower()
        keys = get_keys('p', table)[0][1]
        cursor.execute(s % (tname, tname, ','.join(keys)))
    except (IndexError, KeyError):
        print 'table %s nema PK? Divne ...' % table

def createFKs(table, cursor):
#     try:
#         ff.write(set_Fkeys(i))
#     except:
#         print "chyba Foreign " + i, sys.exc_type, sys.exc_value
    pass

######    KEY FUNCTIONS
def get_keys(typ_key,tab):
    return_key=[]
    if typ_key=='p':
        keys=PrimKeys[tab]
    elif typ_key=='f':
        keys=ForKeys[tab]
    i=0
    for k in keys:
        return_key.append([])
        return_key[i].append(k[0])
        return_key[i].append(k[1:])
        i=i+1
    return return_key

def drop_keys(tab):
    keys=get_keys(tab)
    sqlt='ALTER TABLE '+tab.lower()+' DROP CONSTRAINT '+keys[0]+';'
    return sqlt
    
######      SET PRIMARY KEYS
def set_Pkeys(tab):
    keys=get_keys('p',tab)
    col=''
    for i in keys[0][1]:
        col=col+i+','
    col=col[:-1]
    sqlt='ALTER TABLE '+tab.lower()+' ADD CONSTRAINT '+keys[0][0]+' PRIMARY KEY('+col+');\n'
    return sqlt

######      SET FOREIGN KEYS
def set_Fkeys(tab):
    sqlt=''
    keys=get_keys('f',tab)
    for k in keys:
        col=['','']
        foo=1
        for i in k[1][1:]:
            foo=foo+1
            if foo%2==0:
                col[0]=col[0]+i+','
            else:
                col[1]=col[1]+i+','
        col[0]=col[0][:-1]
        col[1]=col[1][:-1]
        sqlt=sqlt+'ALTER TABLE '+tab.lower()+' ADD CONSTRAINT '+k[0]+' FOREIGN KEY('+col[0]+')\n'
        sqlt=sqlt+'REFERENCES '+k[1][0]+'('+col[1]+');\n'
    return sqlt
        
    

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

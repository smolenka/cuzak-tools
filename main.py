
import nvf2sql
import psycopg2
import funkce
import geom
import codecs
import sys
import os


def main(file_name, deleteExisting=False):
    try:
        conn = psycopg2.connect(os.environ['DATABASE_URL'])
    except Exception, e:
        print "I am unable to connect to the database ..."
        raise e
    
    cur = conn.cursor()
    
    if deleteExisting:
        funkce.removeExistingTables(cur)
            
    # parse input file and fill the DB
#     with codecs.open(file_name, encoding='iso-8859-2') as f:
#         nvf2sql.ImportVFKParser(f, cur)
#         
#     conn.commit()
#
#     print "Geometry HP..."
#     geom.AddGeometryL('public', 'hp', cur)
#     conn.commit()
#     
#     print "Geometry OB..."
#     geom.AddGeometryL('public','ob',cur)
#     conn.commit()
#     
#     print "Geometry DPM..."
#     geom.AddGeometryL('public','dpm',cur)
#     conn.commit()
    
    print "Geometry PAR..."
    geom.AddGeometryP('public','par','hp', cur)
    conn.commit()
    
    print "Geometry BUD..."
    geom.AddGeometryP('public','bud','ob',cur)
    conn.commit()
    
    funkce.AddColumn(cur,'par','drupoz_nazev','varchar(60)','drupoz','nazev','kod','drupoz_kod')
    funkce.AddColumn(cur,'par','zpvypo_nazev','varchar(60)','zpvypo','nazev','kod','zpvypa_kod')
    funkce.SetUpParcelNumber(cur)
    funkce.SetUpBuildingNumber(cur)
    print "Complete."    


if __name__ == "__main__":
    file_name="/home/vencax/prg/vojta/OPENGIS/data/balkovka-3-2015/737925.vfk"
    os.environ['DATABASE_URL'] = 'postgresql://vojta:hoVNO1234@localhost/vojtadb3'
    main(file_name)

import funkce

from vfkparser import BaseVFKParser


class ImportVFKParser(BaseVFKParser):
    
    def onHead(self, head):
        pass
    
    def onBlock(self, table, colsInfo):
        self.currColinfo = colsInfo
        cols = []
        for c in colsInfo:
            cols.append('%s %s' % (c[0].lower(), self._colType(c)))
        sql='CREATE TABLE %s (%s);' % (table.lower(), ','.join(cols))

        try:
            self._cursor.execute(sql)   # SQL dotaz vytvori prazdnou tabulku
            funkce.createPK(table, self._cursor)
            funkce.createFKs(table, self._cursor)
        except Exception, e:
            print str(e)
    
    def onData(self, table, data):            
        val_strings = []
        for idx, val in enumerate(data):
            val_strings.append(self._sqlVal(val, self.currColinfo[idx]))
        sqlt='INSERT INTO %s VALUES(%s);' % (table.lower(), ','.join(val_strings))

        try:
            self._cursor.execute(sqlt)     #SQL dotaz naplni tabulku
        except Exception, e:
            print str(e)
        
    def _sqlVal(self, val, colinfo):
        val = val.replace('\'', '')
        if len(val) == 0:
            return 'null'
        
        typ = colinfo[1]
        if typ[0]=='N':
            return val
        elif typ[0]=='T':
            return '\'%s\'' % val
        elif typ[0]=='D':
            p = val.split(' ')
            datepts = p[0].split('.')
            return 'TIMESTAMP \'%s-%s-%s %s\'' % (datepts[2], datepts[1], datepts[0], p[1])
    
    def _colType(self, colinfo):
        typ = colinfo[1]
        if typ[0]=='N':
            return 'NUMERIC(%s)' % typ[1:].replace('.',',')
        elif typ[0]=='T':
            return 'VARCHAR(%s)' % typ[1:]
        elif typ[0]=='D':
            return 'TIMESTAMP'


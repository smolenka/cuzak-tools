import dbconstraints
from vfkparser import BaseVFKParser


class ImportVFKParser(BaseVFKParser):
    schema = 'public'

    def onHead(self, head):
        pass

    def onBlock(self, table, colsInfo):
        self.currColinfo = colsInfo
        q = """
        SELECT column_name, data_type FROM information_schema.columns
        WHERE table_schema = '%s' AND table_name = '%s'
        """ % (self.schema, table.lower())
        self._cursor.execute(q)
        existingCols = self._cursor.fetchall()

        if len(existingCols) > 0:
            self._updateTable(table, existingCols, colsInfo)
        else:
            self._createTable(table, colsInfo)
        self._cursor.connection.commit()

    def onData(self, table, data):
        val_strings = []
        for idx, val in enumerate(data):
            val_strings.append(self._sqlVal(val, self.currColinfo[idx]))
        sqlt='INSERT INTO %s VALUES(%s);' % (table.lower(), ','.join(val_strings))

        try:
            self._cursor.execute(sqlt)     #SQL dotaz naplni tabulku
            self._cursor.connection.commit()
        except Exception, e:
            print str(e)
            self._cursor.connection.rollback()

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

    def _createTable(self, table, colsInfo):
        cols = []
        for c in colsInfo:
            cols.append('%s %s' % (c[0].lower(), self._colType(c)))
        sql='CREATE TABLE %s (%s);' % (table.lower(), ','.join(cols))

        try:
            self._cursor.execute(sql)   # SQL dotaz vytvori prazdnou tabulku
            dbconstraints.createPK(table, self._cursor)
#             dbconstraints.createFKs(table, self._cursor)
        except Exception, e:
            print str(e)

    def _updateTable(self, table, existingCols, colsInfo):
        aq = "ALTER TABLE %s ADD COLUMN %s %s;"
        def _contains(col):
            for c in existingCols:
                if c[0] == col: return True
            return False
        for c in colsInfo:
            if not _contains(c[0].lower()):
                self._cursor.execute(aq % (table.lower(), c[0].lower(), self._colType(c)))

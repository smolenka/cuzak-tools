import dbconstraints
from vfkparser import BaseVFKParser
from datetime import datetime
from decimal import Decimal


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
        try:
            self._insertNew(table, data)
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
                
    def _insertNew(self, table, data):
        val_strings = []
        for idx, val in enumerate(data):
            val_strings.append(self._sqlVal(val, self.currColinfo[idx]))
        q = 'INSERT INTO %s VALUES(%s);' % (table.lower(), ','.join(val_strings))
        self._cursor.execute(q)
        
    
class ChangesSolvingImportVFKParser(ImportVFKParser):
    
    def onData(self, table, data):
        existing = self._getExisting(table, data)
        try:
            if existing == None:
                self._insertNew(table, data)
            else:
                self._solveDifferences(table, data, existing)
            self._cursor.connection.commit()
        except Exception, e:
            print str(e)
            self._cursor.connection.rollback()

    def _getExisting(self, table, data):
        """
        Zkonstruuje dotaz podle primarnich klicu,
        a vybere existujici zaznam podle 'data' nebo None kdyz neexistuje.
        """
        try:
            pks = dbconstraints.PrimKeys[table]
            constrs = []
            for pk in pks:
                colInfoIdx = self._columnOrd(pk) # poradi sloupecku
                val = self._sqlVal(data[colInfoIdx], self.currColinfo[colInfoIdx])
                constrs.append("%s=%s" % (pk, val))
            q = "SELECT * FROM %s WHERE %s" % (table, ' AND '.join(constrs))
            self._cursor.execute(q)
            return self._cursor.fetchone()
        except (KeyError):
            return None # nezmame primarni klic table, zaznam jakoby nebyl

    def _columnOrd(self, col):
        for idx, c in enumerate(self.currColinfo):
            if c[0].lower() == col:
                return idx    

    def _solveDifferences(self, table, data, existing):
        changes = {}
        for idx, ci in enumerate(self.currColinfo):
            if data[idx].replace('\'', '') != str(existing[idx]):
                changes[ci[0]] = (data[idx], existing[idx])

        self._odstranBlbosti(changes)
        if len(changes) > 0 and hasattr(self, 'onChanges'):
            self.onChanges(table, changes)
            
    def _odstranBlbosti(self, changes):
        """ odstran blbost, ktere se tvari jako zmeny, ale nejsou """
        for col, diff in changes.items():
            if len(diff[0].replace('\'', '')) == 0 and diff[1] == None:
                del changes[col]
            if isinstance(diff[1], datetime):   # odstran defacto stejne datumy
                if diff[1].strftime('%d.%m.%Y %H:%M:%S') == diff[0].replace('\'', ''):
                    del changes[col]
            if isinstance(diff[1], Decimal):
                if float(diff[1]) == float(diff[0].replace('\'', '')):
                    del changes[col]

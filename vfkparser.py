
class BaseVFKParser(object):
    """
    Iteruje radky v souboru (streamin) a podle jejich typu
    vyvola patricnou metodu implementovanou v potomeku teto tridy.
    """
    
    def __init__(self, streamin, cursor):
        self._sin = streamin
        self._cursor = cursor
        self._linenum = 0
        self._parse()
    
    def _parse(self):
        head = []
        inBody = False
        
        for line in self._sin:    # prochazime vstupni soubor po radcich
            self._linenum += 1
            if self._linenum % 50 == 0:
                print 'processing line %i' % self._linenum
                
            linetype = line[1]
            line=line.replace('"','\'')         #nahradi " -> '
            line=line.replace('\r\n', '')[2:]
            
            if linetype=='H':                    #if radek je HLAVICKA
                head.append(line)
                
            elif linetype=='B':  # if uvozujici radek BLOKU (table info)
                self.onBlock(*self._make_blockinfo(line))
                
            elif linetype=='D':  # if radka obsahuje DATA
                if not inBody:
                    # nevim proc radka pred touto Datovou neni uvozena jako B
                    # taze ji budu brat jako blockinfo
                    lastLine = head.pop()
                    table, binfo = self._make_blockinfo(lastLine)
                    # jeste predtin ale flushnu hlavicku
                    self.onHead(head)
                    # pouziju binfo
                    self.onBlock(table, binfo)
                    inBody = True
                parts = line.split(';')
                self.onData(parts[0], parts[1:])
                
    def _make_blockinfo(self, line):
        parts = line.split(';')
        return (parts[0], [p.split(' ') for p in parts[1:]])
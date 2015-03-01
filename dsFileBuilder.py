import os
from pprint import pprint
from utilityFunc import splitNameToWords, getStructFileName

class DSFileBuilder:
    def __init__(self, strName, lstTypes):
        self.strFileName = getStructFileName(strName)
        self.lstTypes = lstTypes

    def __getDefineString(self, strName):
        lstSplitWords = splitNameToWords(strName)
        ret = '__'
        for w in lstSplitWords:
            ret += w.upper()
            ret += '_'
        ret += '_'
        return ret

    def buildDS(self):
        pprint(self.lstTypes)
        sep = os.linesep
        tabSpace = '  '
        strTypeDefHead = "typedef struct {" + sep

        with open(self.strFileName, 'w') as fDS:
            for ds in self.lstTypes:
                dsName = ds.get('name', 'UnknownStruct')
                lstBody = ds.get('fields', [])
                if len(lstBody) == 0: continue

                fDS.write("#ifndef %s"%(self.__getDefineString(dsName)) + sep)
                fDS.write("#define %s"%(self.__getDefineString(dsName)) + sep)
                fDS.write(sep)
                fDS.write(strTypeDefHead)
                for dicVar in lstBody:
                    varName = dicVar.get('name', 'UnknownVar')
                    varType = dicVar.get('type', 'int')
                    strLineInput = tabSpace + "%s"%(varType) + ' ' + \
                                   "%s"%(varName) + ';' + sep
                    fDS.write(strLineInput)
                strTypeDefTail = "} %s;"%(dsName) + sep
                fDS.write(strTypeDefTail)
                fDS.write(sep)

            fDS.write("#endif" + sep)
        pass
import os
import numpy
from pprint import pprint
from utilityFunc import splitNameToWords, getStructFileName

dicCType2NumpyDS = {
    'byte'      : numpy.int8,
    'ubyte'     : numpy.uint8,
    'short'     : numpy.int16,
    'ushort'    : numpy.uint16,
    'int'       : numpy.int32,
    'uint'      : numpy.uint32,
    'float'     : numpy.float32,
    'long'      : numpy.int64,
    'string'    : numpy.object
}

class DSFileBuilder:
    def __init__(self, strName, lstTypes, strFolder = 'out'):
        self.strFileName = getStructFileName(strName, strFolder)
        self.lstTypes = lstTypes

        self.dicNumpyDS = {} # {'DS':numpyDType}

    def getGeneratedNumpyDS(self):
        return self.dicNumpyDS

    def __generateNumpyDS(self, dsName, lstData):
        lstNumpyData = []
        for dicVar in lstData:
            varName = dicVar.get('name', 'UnknownVar')
            varType = dicVar.get('type', 'int')
            # unicode string is not acceptable in dtype
            tupData = (str(varName), dicCType2NumpyDS[varType])
            lstNumpyData.append(tupData)

        self.dicNumpyDS[str(dsName)] = numpy.dtype(lstNumpyData)

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
        strTypeDefHead = 'typedef struct {' + sep

        with open(self.strFileName, 'w') as fDS:
            for ds in self.lstTypes:
                dsName = ds.get('name', 'UnknownStruct')
                lstBody = ds.get('fields', [])
                if len(lstBody) == 0: continue

                fDS.write('#ifndef %s'%(self.__getDefineString(dsName)) + sep)
                fDS.write('#define %s'%(self.__getDefineString(dsName)) + sep)
                fDS.write(sep)
                fDS.write(strTypeDefHead)
                for dicVar in lstBody:
                    varName = dicVar.get('name', 'UnknownVar')
                    varType = dicVar.get('type', 'int')
                    strLineInput = tabSpace + '%s'%(varType) + ' ' + \
                                   '%s'%(varName) + ';' + sep
                    fDS.write(strLineInput)
                strTypeDefTail = '} %s;'%(dsName) + sep
                fDS.write(strTypeDefTail)
                fDS.write(sep)

                self.__generateNumpyDS(dsName, lstBody)

            fDS.write("#endif" + sep)
        pass
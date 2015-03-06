import os
import numpy
from pprint import pprint
from utilityFunc import splitNameToWords, \
                        getStructFileName, \
                        DS_TYPE_TO_NUMPY_TYPE

class DSFileBuilder:
    def __init__(self, strName, lstTypes, strFolder='out'):
        assert (not os.path.isabs(strFolder)), "strFolder should be a relatvie path"
        self.strFileName = getStructFileName(strName)
        self.strOutputFolder = os.path.join(os.path.dirname(__file__), strFolder)
        if not os.path.exists(self.strOutputFolder):
            os.makedirs(self.strOutputFolder)

        self.strFilePath = os.path.join(self.strOutputFolder, self.strFileName)
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
            tupData = (str(varName), DS_TYPE_TO_NUMPY_TYPE[varType])
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

        with open(self.strFilePath, 'w') as fDS:
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
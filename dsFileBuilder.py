import os
import numpy
from pprint import pprint
from utilityFunc import splitNameToWords, \
                        getStructFileName, \
                        DS_TYPE_TO_NUMPY_TYPE, \
                        KERNEL_TYPE_MAP

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

                lstNumpyData = []
                fDS.write('#ifndef %s'%(self.__getDefineString(dsName)) + sep)
                fDS.write('#define %s'%(self.__getDefineString(dsName)) + sep)
                fDS.write(sep)
                fDS.write(strTypeDefHead)
                for dicVar in lstBody:
                    varName = dicVar.get('name', 'UnknownVar')
                    varKernelType = KERNEL_TYPE_MAP[dicVar.get('type', 'int')]
                    strLineInput = tabSpace + '%s'%(varKernelType) + ' ' + \
                                   '%s'%(varName) + ';' + sep
                    fDS.write(strLineInput)
                    # unicode string is not acceptable in dtype
                    tupData = (str(varName), DS_TYPE_TO_NUMPY_TYPE[dicVar.get('type', 'int')])
                    lstNumpyData.append(tupData)

                strTypeDefTail = '} %s;'%(dsName) + sep
                fDS.write(strTypeDefTail)
                fDS.write(sep)

                self.dicNumpyDS[str(dsName)] = numpy.dtype(lstNumpyData)
                fDS.write("#endif" + sep)
        pass

import os
from pprint import pprint
from utilityFunc import splitNameToWords, getKernelFileName, \
                        getStructFileName, getKernelType

class KernelFuncBuilder:
    def __init__(self, strName, lstFuncs, strFolder='out'):
        assert (not os.path.isabs(strFolder)), "strFolder should be a relatvie path"
        # the strFileName is for output
        self.strFileName = getKernelFileName(strName)
        self.strOutputFolder = os.path.join(os.path.dirname(__file__), strFolder)
        if not os.path.exists(self.strOutputFolder):
            os.makedirs(self.strOutputFolder)
        self.strFilePath = os.path.join(self.strOutputFolder, self.strFileName)

        # the strDSFileName is for inclusion and they should be at the same
        # folder.
        self.strDSFileName = getStructFileName(strName)
        self.lstFuncs = lstFuncs
        self.dicKFuncDS = {}

    def getGeneratedKFuncDS(self):
        return self.dicKFuncDS

    def __generateKFuncDS(self, funcName, lstArgs):
        dicArgs = {}
        dicArgs['var'] = ['gWorkSize', 'lWorkSize']
        dicArgs['types'] = {}
        for item in lstArgs:
            varName = item['name']
            dicArgs['var'].append(varName)
            dicArgs['types'][varName] = {'argType' : item['argType'], 'type' : item['type']}
        self.dicKFuncDS[funcName] = dicArgs
        pass

    def buildKF(self):
        pprint(self.lstFuncs)
        sep = os.linesep
        tabSpace = '  '

        strDSInclude = '#include "%s"'%(os.path.join(self.strOutputFolder, self.strDSFileName)) + sep
        with open(self.strFilePath, 'w') as fKF:
            fKF.write(strDSInclude)
            fKF.write(sep)
            for dicFunc in self.lstFuncs:
                funcName = dicFunc.get('name', 'unknownFunc')
                lstArgs = dicFunc.get('arguments', [])

                strFuncHead = '__kernel void %s('%(funcName)
                strFuncTail = '}'+sep
                strFuncBody = tabSpace + '// Please implement your kernel code here.' + sep
                strParametersSpace = ' ' * len(strFuncHead)

                for idx, dicPara in enumerate(lstArgs):
                    varName = dicPara.get('name', 'unknow')
                    memoryType = dicPara.get('memoryType', None)
                    memoryType = '__' + memoryType + ' ' if memoryType is not None else ''
                    varType = dicPara.get('type', 'int')
                    if type(varType) == dict:
                        varType = varType['arrayType'] + '*'
                    else:
                        varType = getKernelType(varType)

                    argLine = memoryType + varType + ' ' + varName
                    argLine += ') {' if idx == (len(lstArgs) - 1) else ','
                    argLine += sep

                    if idx == 0:
                        fKF.write(strFuncHead + argLine)
                    else:
                        fKF.write(strParametersSpace + argLine)

                fKF.write(strFuncBody)
                fKF.write(strFuncTail)
                fKF.write(sep)

                self.__generateKFuncDS(funcName, lstArgs)
            pass
        pass
import os
from pprint import pprint
from utilityFunc import splitNameToWords, getKernelFileName, \
                        getStructFileName

class KernelFuncBuilder:
    def __init__(self, strName, lstFuncs):
        self.strFileName = getKernelFileName(strName)
        self.strDSFileName = getStructFileName(strName)
        self.lstFuncs = lstFuncs    

    def buildKF(self):
        pprint(self.lstFuncs)
        sep = os.linesep
        tabSpace = '  '

        strDSInclude = '#include "%s"'%(self.strDSFileName) + sep
        with open(self.strFileName, 'w') as fKF:
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
                    memoryType = '__' + dicPara.get('memoryType', 'global')
                    varType = dicPara.get('type', 'int')
                    if type(varType) == dict:
                        varType = varType['arrayType'] + '*'
                    
                    argLine = memoryType + ' ' + varType + ' ' + varName
                    argLine += ')' if idx == (len(lstArgs)-1) else ','
                    argLine += sep

                    if idx == 0:
                        fKF.write(strFuncHead + argLine)
                    else:
                        fKF.write(strParametersSpace + argLine)

                fKF.write(strFuncBody)
                fKF.write(strFuncTail)
                fKF.write(sep)
            pass
        pass
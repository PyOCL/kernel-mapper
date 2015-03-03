import os
from pprint import pprint
from utilityFunc import splitNameToWords, getStructFileName

def getClassDef(strName, inheritCls=[]):
    strCls = 'class %s'%(strName)
    for idx, cls in enumerate(inheritCls):
        if idx == 0:
            strCls += '('
        strCls += cls
        strCls += ')' if idx == (len(inheritCls)-1) else ', '
    strCls += ':' + os.linesep
    return strCls

def getMethodDef(strMethodName, dicArgd={}):
    strREt = 'def %s(self, '%(strMethodName)

def getFileName(strName):
    return strName+'.py'

class oclPyObjGenerator:
    def __init__(self, strName):
        self.className = strName
        pass

    def generateOCLPyObj(self):
        sep = os.linesep
        tabSpace = '    '
        with open(getFileName(self.className), 'w') as fPyObj:
            fPyObj.write(getClassDef(self.className))
        pass

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
    strRetHead = 'def %s'%(strMethodName)
    strParams = '(self, '
    lstVars = dicArgd.get('var', [])
    lstVars_Default = dicArgd.get('var_default', [])
    args = dicArgd.get('args', None)
    argd = dicArgd.get('argd', None)

    for var in lstVars:
        strParams += var + ', '
    for dicVar in lstVars_Default:
        for var, default in dicVar.iteritems():
            strTemp = var + '=' + str(default) + ', '
            strParams += strTemp
    if args:
        strParams += '*args, '
    if argd:
        strParams += '**argd, '
    strParams = strParams[:-2]

    strRetTail = '):' + os.linesep
    return strRetHead + strParams + strRetTail

def getFileName(strName):
    return strName+'.py'

class OCLPyObjGenerator:
    def __init__(self, strName, lstTypes, lstFuncs):
        self.className = strName
        self.lstTypes = lstTypes
        self.lstFuncs = lstFuncs
        pass

    def generateOCLPyObj(self):
        sep = os.linesep
        tabSpace = '    '
        with open(getFileName(self.className), 'w') as fPyObj:
            fPyObj.write(getClassDef(self.className))
        pass

# dicArgd = {'var' : ['a', 'b', ...],
#            'var_default' : [{'c':pyobj}],
#            'args' : False/True,
#            'argd' : False/True}

lstTestMethodData = [
dicTest0 = {'var' : [],
            'var_default' : [],
            'args' : False,
            'argd' : False}
dicTest1 = {'var' : ['a', 'b'],
            'var_default' : [],
            'args' : False,
            'argd' : False}
dicTest2 = {'var' : [],
            'var_default' :[{'a':1, 'b':[2,3], 'c':{'d':6}, 'd':None}],
            'args' : False,
            'argd' : False}
dicTest3 = {'var' : [],
            'var_default' :[],
            'args' : True,
            'argd' : False}
dicTest4 = {'var' : [],
            'var_default' : [],
            'args' : False,
            'argd' : True}
dicTest5 = {'var' : dicTest1['var'],
            'var_default' : dicTest2['var_default'],
            'args' : dicTest3['args'],
            'argd' : dicTest4['argd']}]
def testMethodDef():
    for idx in xrange(len(lstTestMethodData)):
        dicData = eval('dicTest'+str(idx))
        print getMethodDef(str(idx), dicData)

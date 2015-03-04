import os
from pprint import pprint
from utilityFunc import splitNameToWords, \
                        getStructFileName, \
                        getPyFileName

tabSpace = '    '

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
    return tabSpace + strRetHead + strParams + strRetTail

def prepareImport():
    strOS = 'import os' + os.linesep
    strNumpy = 'import numpy' + os.linesep
    return strOS + strNumpy + os.linesep

def prepareNumpyDS(dicDS={}):
    # Should be inside __init__()
    strTemp = ''
    for k in dicDS.iterkeys():
        strTemp = tabSpace * 2
        strTemp += 'self.%s = %s'%(str(k), str(dicDS[k]))
        strTemp += os.linesep
    return strTemp

class OCLPyObjGenerator:
    def __init__(self, strName, dicNumpyDS, dicKFuncDS, strFolder = 'out'):
        self.strFileName = getPyFileName(strName, strFolder)
        self.className = strName
        self.dicNumpyDS = dicNumpyDS
        self.dicKFuncDS = dicKFuncDS
        pass

    def generateOCLPyObj(self):
        sep = os.linesep
        with open(self.strFileName, 'w') as fPyObj:
            fPyObj.write(prepareImport())
            fPyObj.write(getClassDef(self.className))

            fPyObj.write(getMethodDef('__init__'))
            fPyObj.write(prepareNumpyDS(self.dicNumpyDS))
        pass

# dicArgd = {'var' : ['a', 'b', ...],
#            'var_default' : [{'c':pyobj}],
#            'args' : False/True,
#            'argd' : False/True}

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
            'argd' : dicTest4['argd']}

def testMethodDef():
    for idx in xrange(6):
        dicData = eval('dicTest'+str(idx))
        print getMethodDef(str(idx), dicData)

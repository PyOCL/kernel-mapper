import os
from pprint import pprint
from utilityFunc import splitNameToWords, \
                        getStructFileName, \
                        getPyFileName, \
                        getKernelFileName, \
                        DS_TYPE_TO_NUMPY_STRING_TYPE

tabSpace = '    '
opj = os.path.join

def getClassDef(strName, inheritCls=[], nIndent=0):
    strCls = 'class %s'%(strName)
    for idx, cls in enumerate(inheritCls):
        if idx == 0:
            strCls += '('
        strCls += cls
        strCls += ')' if idx == (len(inheritCls)-1) else ', '
    strCls += ':' + os.linesep
    return tabSpace*nIndent + strCls

def getMethodDef(strMethodName, dicArgd={}, nIndent=0):
    # Head
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
    head = tabSpace*nIndent + strRetHead + strParams + strRetTail
    return head

def prepareImport(nIndent=0):
    lstImport = ['import os', 'import numpy', 'from oclConfigurar import OCLConfigurar, PREFERRED_GPU']
    strResult = ''
    for item in lstImport:
        strResult += item + os.linesep
    return tabSpace*nIndent + strResult + os.linesep

def prepareNumpyDS(dicDS={}, nIndent=0):
    # Should be inside __init__()
    strTemp = ''
    for k in dicDS.iterkeys():
        strTemp = tabSpace * nIndent
        strTemp += '%s = numpy.dtype(%s)'%(str(k), str(dicDS[k]))
        strTemp += os.linesep
    return strTemp

def prepareOCLConfigurar(nIndent=0):
    return tabSpace*nIndent + "self.oclConfigurar = OCLConfigurar()" + os.linesep

def prepareOCLSetup(clsName, dicNumpyDS={}, nIndent=0):
    strDS = ''
    for k in dicNumpyDS.iterkeys():
        strDS += ' \'' + k + '\'' + ' : ' + '%s.%s,'%(clsName, k)
    space = tabSpace*nIndent
    test = space + 'self.oclConfigurar.setupContextAndQueue(PREFERRED_GPU)' + os.linesep
    test += space + 'dirPath = os.path.dirname(__file__)' + os.linesep
    test += space + 'path = os.path.join(dirPath, %s)'%('\''+str(getKernelFileName(clsName))+'\'') + os.linesep
    test += space + 'dicRetDS = self.oclConfigurar.setupProgramAndDataStructure(path, [dirPath], {%s})'%(strDS) + os.linesep
    for k in dicNumpyDS.iterkeys():
        test += space + 'self.%s = dicRetDS.get(%s, None)'%(k, '\''+k+'\'') + os.linesep
    return test + os.linesep

def prepareOCLFuncImpl(strMethodName, dicArgd={}, nIndent=0):
    lstVars = dicArgd.get('var', [])
    types = dicArgd.get('types', {})
    strRepresArgs = ''
    for var in lstVars:
        if var in ['gWorkSize', 'lWorkSize']:
            strRepresArgs += var + ', '
        else:
            varTypeInfo = types[var]
            if type(varTypeInfo['type']) == dict:
                strRepresArgs += '%s.data, '%(var)
            else:
                strRepresArgs += '%s(%s), '%(DS_TYPE_TO_NUMPY_STRING_TYPE[str(varTypeInfo['type'])], var)
    if strRepresArgs == '':
        return '' + os.linesep
    strRepresArgs = strRepresArgs[:-2]
    body = tabSpace*nIndent + 'self.oclConfigurar.callFuncFromProgram(%s, %s)'%('\''+strMethodName+'\'', strRepresArgs) + os.linesep
    return body

def prepareOCLBufferByDS(nIndent=0):
    dicArgs = {'var' : ['dataStructure'],
               'var_default' : [{'nSize':0}, {'lstData':[]}]}
    strFuncDef = getMethodDef('createBufferData', dicArgs, nIndent)
    strFuncDef += tabSpace*(nIndent+1) + 'OCLFunc = self.oclConfigurar.createOCLArrayForInput if nSize == 0 else self.oclConfigurar.createOCLArrayEmpty' + os.linesep
    strFuncDef += tabSpace*(nIndent+1) + 'input = lstData if nSize == 0 else nSize' + os.linesep
    strFuncDef += tabSpace*(nIndent+1) + 'dataBuffer = OCLFunc(dataStructure, input)' + os.linesep
    strFuncDef += tabSpace*(nIndent+1) + 'return dataBuffer' + os.linesep
    return strFuncDef + os.linesep

def prepareFuncTail(nIndent=0):
    return tabSpace*nIndent + 'pass' + os.linesep + os.linesep

class OCLPyObjGenerator:
    def __init__(self, strName, dicNumpyDS, dicKFuncDS, strFolder='out'):
        assert (not os.path.isabs(strFolder)), "strFolder should be a relatvie path"
        self.strFileName = getPyFileName(strName)
        self.strOutputFolder = opj(os.path.dirname(__file__), strFolder)
        if not os.path.exists(self.strOutputFolder):
            os.makedirs(self.strOutputFolder)
        self.strFilePath = opj(self.strOutputFolder, self.strFileName)

        self.strRelFolder = strFolder
        self.className = strName
        self.dicNumpyDS = dicNumpyDS
        self.dicKFuncDS = dicKFuncDS
        pass

    def getObj(self):
        import pkgutil
        modules = pkgutil.iter_modules(path=[self.strOutputFolder])
        instance = None
        for loader, mod_name, ispkg in modules:
            if mod_name == self.className:
                loaded_mod = __import__(self.strRelFolder+'.'+mod_name, fromlist=[mod_name])
                loaded_class = getattr(loaded_mod, self.className)
                instance = loaded_class()
                break
        return instance

    def __copyOCLConfigurarToOutput(self):
        from shutil import copyfile
        outputFilePath = opj(self.strOutputFolder, 'oclConfigurar.py')
        copyfile(opj(os.path.dirname(__file__), 'oclConfigurar.py'), outputFilePath)

    def generateOCLPyObj(self):
        # __init__ file for module loader in folder
        with open(opj(self.strOutputFolder, getPyFileName('__init__')), 'w'):
            pass
        # Copy OCLConfigurar into output folder
        self.__copyOCLConfigurarToOutput()

        # Generating target file
        with open(self.strFilePath, 'w') as fPyObj:
            # import
            fPyObj.write(prepareImport())

            # class
            fPyObj.write(getClassDef(self.className))
            fPyObj.write(prepareNumpyDS(self.dicNumpyDS, 1))

            # __init__
            fPyObj.write(getMethodDef('__init__', nIndent=1))
            fPyObj.write(prepareOCLConfigurar(2))
            fPyObj.write(prepareOCLSetup(self.className, self.dicNumpyDS, 2))
            fPyObj.write(prepareFuncTail(2))

            fPyObj.write(prepareOCLBufferByDS(1))

            # methods
            for funcName, dicArgs in self.dicKFuncDS.iteritems():
                fPyObj.write(getMethodDef(funcName, dicArgs, nIndent=1))
                fPyObj.write(prepareOCLFuncImpl(funcName, dicArgs, nIndent=2))
                fPyObj.write(prepareFuncTail(2))
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

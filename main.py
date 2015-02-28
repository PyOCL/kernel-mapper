import os
import json
from pprint import pprint

def loadJSON(fInput):
    with open(fInput) as f:
        return json.load(f)

def splitNameToWords(strName):
    lstSplitWords = []
    idxBegin = -1
    for idx, c in enumerate(strName):
        if c.isupper():
            if idxBegin >= 0:
                w = strName[idxBegin:idx]
                lstSplitWords.append(w)
            idxBegin = idx
        if idx == (len(strName)-1):
            w = strName[idxBegin:]
            lstSplitWords.append(w)
    return lstSplitWords

def getDefineString(strName):
    lstSplitWords = splitNameToWords(strName)
    ret = '__'
    for w in lstSplitWords:
        ret += w.upper()
        ret += '_'
    ret += '_'
    return ret

def getStructFileName(strName):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        ret += '_'
    ret += 'structs.h'
    return ret

def buildDS(strFileName, lstInput):
    pprint(lstInput)
    sep = os.linesep
    tabSpace = '  '
    strTypeDefHead = "typedef struct {" + sep

    with open(strFileName, 'w') as fDS:
        for ds in lstInput:
            dsName = ds.get('name', 'UnknownStruct')
            lstBody = ds.get('fields', [])
            if len(lstBody) == 0: continue

            fDS.write("#ifndef %s"%(getDefineString(dsName)) + sep)
            fDS.write("#define %s"%(getDefineString(dsName)) + sep)
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

filePath = "data/example.json"
data = loadJSON(filePath)

name = data.get('name')
lstTypes = data.get('types')
lstFuncs = data.get('functions')

buildDS(getStructFileName(name), lstTypes)

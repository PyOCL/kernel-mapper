import os

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

def getStructFileName(strName, strFolder = 'out'):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        ret += '_'
    ret += 'structs.h'

    if not os.path.exists(strFolder):
        os.makedirs(strFolder)
    return os.path.join(strFolder, ret)

def getKernelFileName(strName, strFolder = 'out'):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        if w != lstSplitWords[-1]:
            ret += '_'
    ret += '.c'

    if not os.path.exists(strFolder):
        os.makedirs(strFolder)    
    return os.path.join(strFolder, ret)

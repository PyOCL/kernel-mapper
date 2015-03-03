
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

def getStructFileName(strName):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        ret += '_'
    ret += 'structs.h'
    return ret

def getKernelFileName(strName):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        if w != lstSplitWords[-1]:
            ret += '_'
    ret += '.c'
    return ret
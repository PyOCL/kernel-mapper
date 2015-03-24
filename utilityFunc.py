import os
import numpy

KERNEL_TYPE_MAP = {\
    'byte': 'char',\
    'ubyte': 'unsigned char',\
    'short': 'short',\
    'ushort': 'unsigned short',\
    'int': 'int',\
    'uint': 'unsigned int',\
    'float': 'float',\
    'long': 'long',\
    'string': 'char*'\
}

DS_TYPE_TO_NUMPY_TYPE = {
    'byte'      : numpy.int8,
    'ubyte'     : numpy.uint8,
    'short'     : numpy.int16,
    'ushort'    : numpy.uint16,
    'int'       : numpy.int32,
    'uint'      : numpy.uint32,
    'float'     : numpy.float32,
    'long'      : numpy.int64,
    'string'    : numpy.object
}

DS_TYPE_TO_NUMPY_STRING_TYPE = {
    'byte'      : 'numpy.int8',
    'ubyte'     : 'numpy.uint8',
    'short'     : 'numpy.int16',
    'ushort'    : 'numpy.uint16',
    'int'       : 'numpy.int32',
    'uint'      : 'numpy.uint32',
    'float'     : 'numpy.float32',
    'long'      : 'numpy.int64',
    'string'    : 'numpy.object'
}

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

def getStructFileName(strName, strFolder=None):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        ret += '_'
    ret += 'structs.h'

    if strFolder is not None:
        if not os.path.exists(strFolder):
            os.makedirs(strFolder)
        return os.path.join(strFolder, ret)
    else:
        return ret

def getKernelFileName(strName, strFolder=None):
    lstSplitWords = splitNameToWords(strName)
    ret = ''
    for w in lstSplitWords:
        ret += w.lower()
        if w != lstSplitWords[-1]:
            ret += '_'
    ret += '.c'

    if strFolder is not None:
        if not os.path.exists(strFolder):
            os.makedirs(strFolder)
        return os.path.join(strFolder, ret)
    else:
        return ret

def getKernelType(dataType):
    return KERNEL_TYPE_MAP[dataType] if dataType in KERNEL_TYPE_MAP else None

def getPyFileName(strName, strFolder=None):
    ret = strName + '.py'
    if strFolder is not None:
        if not os.path.exists(strFolder):
            os.makedirs(strFolder)
        return os.path.join(strFolder, ret)
    return ret

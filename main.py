import os
import json
import sys
from pprint import pprint

def loadJSON(fInput):
    with open(fInput) as f:
        return json.load(f)
    return None

if __name__ == '__main__':
    filePath = os.path.join(os.path.dirname(__file__), 'data/example.json')
    data = loadJSON(filePath)
    # check if the data is loaded correctly
    if data is None:
        sys.exit('wrong json file');

    name = data.get('name')
    lstTypes = data.get('types')
    lstFuncs = data.get('functions')
    strOutFolder = os.path.join(os.path.dirname(__file__), 'out')
    print "Output files to : %s"%(os.path.abspath(strOutFolder))

    from dsFileBuilder import DSFileBuilder
    dsb = DSFileBuilder(name, lstTypes, strOutFolder)
    dsb.buildDS()
    dicNumpyDS = dsb.getGeneratedNumpyDS()

    from kernelFuncBuilder import KernelFuncBuilder
    kfb = KernelFuncBuilder(name, lstFuncs, strOutFolder)
    kfb.buildKF()
    dicKFuncDS = kfb.getGeneratedKFuncDS()

    from oclPyObjGenerator import OCLPyObjGenerator
    opg = OCLPyObjGenerator(name, dicNumpyDS, dicKFuncDS, strOutFolder)
    opg.generateOCLPyObj()
    a = opg.getObj()
    print a
    pass

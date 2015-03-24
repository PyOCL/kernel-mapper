import os
import json
import sys
import argparse

def loadJSON(fInput):
    with open(fInput) as f:
        return json.load(f)
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enter your .json definition file & output folder path,\
        default data/example.json will be executed either input or output is not set")
    parser.add_argument('-i', help="Relative path to your definition .json file")
    parser.add_argument('-o', help="Relative path to your output folder")
    args = parser.parse_args()

    filePath = None
    strOutFolder = None
    if args.i == None or args.o == None:
        filePath = os.path.join(os.path.dirname(__file__), 'data/example.json')
        strOutFolder = os.path.join(os.path.dirname(__file__), 'out')
    else:
        filePath = os.path.join(os.path.dirname(__file__), args.i)
        strOutFolder = os.path.join(os.path.dirname(__file__), args.o)

    print "Input file here : %s"%(os.path.abspath(filePath))
    print "Output files to : %s"%(os.path.abspath(strOutFolder))

    data = loadJSON(filePath)

    # check if the data is loaded correctly
    if data is None:
        sys.exit('wrong json file');
    name = data.get('name')
    lstTypes = data.get('types')
    lstFuncs = data.get('functions')

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

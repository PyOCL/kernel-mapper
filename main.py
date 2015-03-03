import os
import json
from pprint import pprint

def loadJSON(fInput):
    with open(fInput) as f:
        return json.load(f)
    return None

if __name__ == '__main__':
    filePath = "data/example.json"
    data = loadJSON(filePath)

    name = data.get('name')
    lstTypes = data.get('types')
    lstFuncs = data.get('functions')

    from dsFileBuilder import DSFileBuilder
    dsb = DSFileBuilder(name, lstTypes)
    dsb.buildDS()

    from kernelFuncBuilder import KernelFuncBuilder
    kfb = KernelFuncBuilder(name, lstFuncs)
    kfb.buildKF()

import pyopencl as cl
import pyopencl.tools
import pyopencl.array
import numpy as np
import sys
PREFERRED_GPU = 0
PREFERRED_CPU = 1
PREFERRED_MCU = 2

class OCLConfigurar:

    def __init__(self):
        self.dicIdx2Platform = {}
        self.dicPlatform2Devices = {}

        self.context = None
        self.curDevice = None
        self.queue = None
        self.program = None
        self.mem_pool = None
        self.__parseInfo()

    def __parseInfo(self):
        for idx, platform in enumerate(cl.get_platforms()):
            self.dicIdx2Platform[idx] = platform
            print "===================================="
            print "Platform : %s"%(platform.name)
            print "Profile  : %s"%(platform.profile)
            print "Vendor   : %s"%(platform.vendor)
            print "Version  : %s"%(platform.version)
            lstDevices = platform.get_devices()
            self.dicPlatform2Devices[platform] = lstDevices
            for device in lstDevices:
                print "  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print "  Device         : %s"%(device.name)
                print "  Type           : %s"%(cl.device_type.to_string(device.type))
                print "  Memory         : %s"%(str(device.global_mem_size/1024/1024) + 'MB')
                print "  Compute Unit   : %s"%(device.max_compute_units)
                print "  Max Work Group Size        : %s"%(device.max_work_group_size)
                print "  Max Work Item  Dimensions  : %s"%(device.max_work_item_dimensions)
                print "  Max Work Item Size         : %s"%(device.max_work_item_sizes)
                print "  Extensions     : %s"%(device.extensions.split(' '))
            print "===================================="


    def __getDefaultDevice(self):
        platform = self.dicIdx2Platform[0]
        default_dev = platform.get_devices(device_type=cl.device_type.DEFAULT)
        return cl.Context(devices=default_dev)

    def setupContextAndQueue(self, device=PREFERRED_GPU):
        self.context = self.getContext(device)
        self.queue = cl.CommandQueue(self.context)
        self.mem_pool =cl.tools.MemoryPool(cl.tools.ImmediateAllocator(self.queue))
        #print "self.queue", self.queue

    def setupProgramAndDataStructure(self, program, lstIPath=[], dicName2DS={}):
        # program : Path to the kernel file
        # lstIPath : Path to be included while building program, e.g. ['testA/', '../testB/']
        # dicName2DS : name to data structure wrapped by numpy,
        #              e.g. {'SampleStruct' : numpy.dtype([('dataIndex', numpy.int),
        #                                                  ('open', numpy.float32)]}
        assert (self.context != None), "Setup context seems incorrectly !!"
        assert (len(self.context.devices) > 0), "Error, No device for context !!"
        self.curDevice = self.context.devices[0]
        dicReturnStruct = {}
        for k, v in dicName2DS.iteritems():
            kObj, k_c_decl = cl.tools.match_dtype_to_c_struct(self.curDevice, k, v)
            retV = cl.tools.get_or_register_dtype(k, kObj)

            dicReturnStruct[k] = retV

        f = open(program, 'r')
        fstr = ''.join(f.readlines())
        f.close()

        strInc = '-I '
        modifiedlstPath = []
        for path in lstIPath:
            escapedPath = path.replace(' ', '^ ') if sys.platform.startswith('win') else path.replace(' ', '\\ ')
            modifiedlstPath.append(strInc + escapedPath)
        self.program = cl.Program(self.context, fstr).build(modifiedlstPath)
        return dicReturnStruct

    def callFuncFromProgram(self, strMethodName, *args, **argd):
        methodCall = getattr(self.program, strMethodName)
        if methodCall:
            if len(args) >= 2 and type(args[1])==tuple and (not args[1]) != True:
                wgs = cl.Kernel(self.program, strMethodName).get_work_group_info(
                    cl.kernel_work_group_info.WORK_GROUP_SIZE, self.curDevice)
                local_worksize = reduce(lambda x,y: x*y, args[1])
                print 'local size : ', local_worksize
                assert wgs >= local_worksize, 'Out of capability, please reduce the local work size for %s()'%(strMethodName)
            evt = methodCall(self.queue, *args)
            return evt
        return None

    def getContext(self, device=PREFERRED_GPU):
        assert len(self.dicIdx2Platform) > 0, 'No platform for OCL operation'
        context = None
        if device == PREFERRED_CPU:
            for lstDev in self.dicPlatform2Devices.itervalues():
                for dev in lstDev:
                    if 'CPU' in cl.device_type.to_string(dev.type):
                        context = cl.Context(devices=[dev])
                        break

        elif device == PREFERRED_MCU:
            mcu_dev = None
            mcu = 0
            for lstDev in self.dicPlatform2Devices.itervalues():
                for dev in lstDev:
                    if dev.max_compute_units > mcu:
                        mcu = dev.max_compute_units
                        mcu_dev = dev

            context = cl.Context(devices=[mcu_dev])
        else:
            for lstDev in self.dicPlatform2Devices.itervalues():
                for dev in lstDev:
                    if 'GPU' in cl.device_type.to_string(dev.type):
                        context = cl.Context(devices=[dev])
                        break

        if not context:
            context = self.__getDefaultDevice()
        return context

    def createOCLArrayEmpty(self, stDType, size):
        # stDType : c style structure
        # size : the size of the array
        assert size > 0, "Can NOT create array size <= 0"
        assert (self.queue != None), " Make sure setup correctly"
        # Creat a list which contains element initialized with structure stDType
        npArrData = np.zeros(size, dtype=stDType)
        clArrData = cl.array.to_device(self.queue, npArrData, allocator=self.mem_pool)
        return clArrData

    def createOCLArrayForInput(self, stDType, lstData):
        # stDType : c style structure
        # lstData : [(a,b,),] ... (a,b,) should maps to stDtype
        assert len(lstData) > 0, "Size of input data list = 0"
        assert (self.queue != None), " Make sure setup correctly"

        arrayData = np.array(lstData, dtype=stDType)
        clArrayData = cl.array.to_device(self.queue, arrayData, allocator=self.mem_pool)
        return clArrayData

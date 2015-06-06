import os
import argparse
import sys
from datetime import datetime
from pprint import pprint
from PIL import Image

def msg(aMsg, c='green'):
    if c == 'blue':
        print "\033[1;34m%s\033[m"%(aMsg)
    elif c == 'green':
        print "\033[1;32m%s\033[m"%(aMsg)
    else:
        print "%s"%(aMsg)

def toBlurCPU(img, filename, maskSize=5):
    imgSize = img.size[0] * img.size[1]
    seqImg = img.getdata()
    AA = seqImg[0]
    newImg = Image.new('RGB', img.size)
    lstNewData = []
    lstAppend = lstNewData.append
    maskIter = xrange(-int(maskSize/2), int(maskSize/2)+1)
    for y in xrange(img.size[1]):
        for x in xrange(img.size[0]):
            count = r = g = b = 0
            for i in maskIter:
                for j in maskIter:
                    if x+i < 0 or x+i >= img.size[0] or \
                        y+j < 0 or y+j >= img.size[1]:
                        continue
                    count += 1
                    tmp_gid = x+i + (y+j) * img.size[0]
                    r += seqImg[tmp_gid][0]
                    g += seqImg[tmp_gid][1]
                    b += seqImg[tmp_gid][2]
            lstAppend((r/count, g/count, b/count))
    newImg.putdata(lstNewData)
    lstFileName = os.path.splitext(filename)
    fname = lstFileName[0] + '_cpu_blur' + lstFileName[1]
    newImg.save(fname)
    pass

def toGrayCPU(img, filename):
    imgSize = img.size[0] * img.size[1]
    seqImg = img.getdata()
    newImg = Image.new('RGB', img.size)
    lstNewData = []
    lstAppend = lstNewData.append
    for p in seqImg:
        temp = (p[0] + p[1] + p[2]) / 3
        lstAppend((temp,temp, temp))
    newImg.putdata(lstNewData)
    lstFileName = os.path.splitext(filename)
    fname = lstFileName[0] + '_cpu_gray' + lstFileName[1]
    newImg.save(fname)
    pass

def toSomethingGPU(img, filename, method=0, maskSize=5):
    from DoMeABlurGray import DoMeABlurGray
    dmabg = DoMeABlurGray()

    imgSize = img.size[0] * img.size[1]

    t1 = datetime.now()
    buffIn = dmabg.createBufferData(DoMeABlurGray.Pixel, lstData=img.getdata())
    buffOut = dmabg.createBufferData(DoMeABlurGray.Pixel, imgSize)
    t2 = datetime.now()
    msg(" Prepare buffer for GPU takes %s (sec.)"%(str(t2-t1)), c='blue')

    if method == 0:
        dmabg.to_gray((img.size[0],img.size[1],), None, img.size[0], img.size[1], buffIn, buffOut)
    else:
        dmabg.to_blur((img.size[0],img.size[1],), None, maskSize, img.size[0], img.size[1], buffIn, buffOut)

    lstFileName = os.path.splitext(filename)
    fname = lstFileName[0] + '_gpu_%s'%('gray' if method == 0 else 'blur') + lstFileName[1]
    outRS = buffOut.reshape(img.size[1], img.size[0]).get()
    im= Image.fromarray(outRS, 'RGB')
    im.save(fname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process input image to a grayed one")
    parser.add_argument('-i', help="Relatvie path to image")
    parser.add_argument('-g', action='store_true', help="Gray the image")
    parser.add_argument('-b', action='store_true', help="Blur the image")
    args = parser.parse_args()
    if args.i == None:
        print "Hey ~ Let me do you a gray !"
        sys.exit(0)

    img = Image.open(os.path.join(os.path.dirname(__file__), args.i))
    if not img:
        print " Image could not be loaded !! "
        sys.exit(0)
    print "ImageSize : ",img.size

    if args.g:
        t1 = datetime.now()
        toGrayCPU(img, args.i)
        t2 = datetime.now()
        msg(" ToGrayCPU takes %s (sec.)"%(str(t2-t1)))
        toSomethingGPU(img, args.i, 0)
        t3 = datetime.now()
        msg(" ToGrayGPU takes %s (sec.)"%(str(t3-t2)))
    if args.b:
        maskSize = 7
        assert (maskSize % 2 != 0), "Please make the size of mask odd"

        t1 = datetime.now()
        toBlurCPU(img, args.i, maskSize=maskSize)
        t2 = datetime.now()
        msg(" ToBlurCPU takes %s (sec.)"%(str(t2-t1)))
        toSomethingGPU(img, args.i, 1, maskSize=maskSize)
        t3 = datetime.now()
        msg(" ToBlurGPU takes %s (sec.)"%(str(t3-t2)))
#include "/home/kilikkuo/Projects/PyOCL/kernel-mapper/samples/img2BlurGray/do_me_a_blur_gray_structs.h"

__kernel void to_gray(int aWidth,
                      int aHeight,
                      __global Pixel* aBufferIn,
                      __global Pixel* aBufferOut) {
  // Please implement your kernel code here.
  unsigned int gid_x = get_global_id(0);
  unsigned int gid_y = get_global_id(1);
  unsigned int gid = gid_x + gid_y * aWidth;
  int gray = (aBufferIn[gid].red + aBufferIn[gid].blue + aBufferIn[gid].green) / 3;
  aBufferOut[gid].red = gray;
  aBufferOut[gid].blue = gray;
  aBufferOut[gid].green = gray;  
}

__kernel void to_blur(int aWidth,
                      int aHeight,
                      __global Pixel* aBufferIn,
                      __global Pixel* aBufferOut) {
  // Please implement your kernel code here.
  unsigned int gid_x = get_global_id(0);
  unsigned int gid_y = get_global_id(1);
  unsigned int gid = gid_x + gid_y * aWidth;
  
  int count = 0;
  int r = 0;
  int g = 0;
  int b = 0;
  int tmp_gid = 0;
  for (int i=-1; i<2; i++) {
    for (int j=-1; j<2; j++) {
      if ((int)(gid_x)+i < 0 || (int)(gid_x)+i > (aWidth-1) ||
        (int)(gid_y)+j < 0 || (int)(gid_y)+j > (aHeight-1)) {
        continue;
      }
      count++;
      tmp_gid = ((int)(gid_x)+i) + ((int)(gid_y)+j)*aWidth;
      r += aBufferIn[tmp_gid].red;
      g += aBufferIn[tmp_gid].green;
      b += aBufferIn[tmp_gid].blue;
    }
  }
  
  aBufferOut[gid].red = r / count;
  aBufferOut[gid].blue = b / count;
  aBufferOut[gid].green = g / count;  
}


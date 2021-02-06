import os

import numpy
import sys
sys.path.append("/home/wly/anaconda3/lib/python3.7/site-packages")
import dicom
# SRC_ROOT='dicoms'
# dicoms_list=os.listdir(SRC_ROOT)
# print(dicoms_list)
# for dicomi in dicoms_list:
#     dicomi=os.path.join(SRC_ROOT,dicomi)
#     frames_list=os.listdir(dicomi)
#     for src_path in frames_list:
#         if not src_path.endswith('.jpg') and not src_path.endswith('.dcm'):
#             src_path=os.path.join(dicomi,src_path)
#             print(src_path)

# a = [1, 2, 3]
# print(max(a))


# li = [1, 2]
# lia = numpy.array(li)
# print(lia)

def get_angel(filepath):
    ds = dicom.read_file(filepath)
    if ds is None:
        return None, None
    else:
        try:
            print(ds.PositionerSecondaryAngle)
            primary=int(ds.PositionerSecondaryAngle)
            secondary=int(ds.PositionerSecondaryAngle)
            return  primary,secondary
        except Exception as e:
            print(e)
            return None, None
def get_FileSize(filePath):
    # filePath = unicode(filePath, 'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)

def get_frames_num(file_path):
    ds = dicom.read_file(file_path)
    num_of_frames=ds.NumberOfFrames
    return num_of_frames

if __name__=='__main__':
    file='/home/DataBase3/segmentation/20190517/lx_20190107_5/HU_YI_ZHEN/2019_1_7_9_41_57/IMG-0001-00001.dcm'
    # p,s=get_angel(file)
    # print(p,s)

    num_of_frames=get_frames_num(file)
    print(num_of_frames)

    # size=get_FileSize(file)
    # print(size)

    

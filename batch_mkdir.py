import os

path='C:/Users/wangl/Desktop/test_cto_frames/dicoms_1217/tmp_res'
for i in range(51,100):

    name='dicom%d'%i
    new_path=os.path.join(path,name)
    if not os.path.exists(new_path):
        os.mkdir(new_path)
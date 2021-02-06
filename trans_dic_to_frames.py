import numpy 
import shutil
from tqdm import tqdm
# import SimpleITK as sitk
import sys
sys.path.append("/home/wly/anaconda3/lib/python3.7/site-packages")
import dicom
import os
import imageio
def split_to_frames(path):

    # pydicom.encaps.generate_pixel_data_frame()
    base_name=os.path.basename(path)
    dir_name=os.path.dirname(path)
    # print(base_name,dir_name)#IMG-0007-00008.dcm dicoms/dicoms1
    try:
        ds = dicom.read_file(path)
        # print(ds.pixel_array.shape)#(115, 512, 512)
        img=ds.pixel_array
        num_of_frames=ds.NumberOfFrames
        for i in range(int(num_of_frames*0.4),num_of_frames-3):
            img1=img[i]
            frames_file=os.path.join(dir_name,'frames{}'.format(i))
            os.mkdir(frames_file)
            imageio.imwrite("{}/{}_{}.jpg".format(dir_name,base_name,i), img1)
            imageio.imwrite("{}/{}_{}.jpg".format(frames_file,base_name,i), img1)
    except:
        print('dicom:{} too short'.format(path))




    # reader = sitk.ImageSeriesReader()
    # img_names = reader.GetGDCMSeriesFileNames('dicoms')
    # reader.SetFileNames(img_names)
    # image = reader.Execute()
    # image_array = sitk.GetArrayFromImage(image)  # z, y, x
    # print(image_array.shape)


def list_all_files(rootdir):
    import os
    _files = []

    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)

    for i in range(0, len(list_file)):
        # 构造路径
        path = os.path.join(rootdir, list_file[i])

        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归

        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files
def make_each_dic_into_a_path(path):
    files=list_all_files(path)
    i=0
    for file in files:
        i+=1
        ####
        # dir_name = os.path.dirname(file)
        dir_name = os.path.join(os.path.dirname(file),'merged')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        base_name = os.path.basename(file)
        new_dicom_i_path=os.path.join(dir_name,'dicom'+str(i))
        os.mkdir(new_dicom_i_path)
        shutil.move(file, new_dicom_i_path)



def rename_same_dicom(path):
    files=os.listdir(path)
    i=0
    for file in files:
        # print(file) #1 2 3
        file_name=os.path.basename(file)
        print(file_name)
        child_path=os.path.join(path,file)
        for c_file in os.listdir(child_path):
            # print(c_file)

            new=str(file_name)+str(c_file.split('-')[1])
            new_file=c_file.split('-')[0]+'-'+str(new)+'-'+str(c_file.split('-')[2])
            print(new_file)
            os.rename(os.path.join(child_path,c_file),os.path.join(child_path,new_file))


def merge(path,new_merged_path):
    # 原文件夹
    old_path =path
    # 查看原文件夹下所有的子文件夹
    filenames = os.listdir(old_path)
    # 新文件夹
    target_path = new_merged_path
    if not os.path.exists(target_path):
        os.mkdir(target_path)

    for file in filenames:
        # 所有的子文件夹
        sonDir = os.path.join(path,file)
        # 遍历子文件夹中所有的文件
        for root, dirs, files in os.walk(sonDir):
            # 如果文件夹中有文件
            if len(files) > 0:
                for f in files:
                    newDir = sonDir + '/' + f
                    # 将文件移动到新文件夹中
                    shutil.move(newDir, target_path)
            else:
                print(sonDir + "文件夹是空的")

if __name__=='__main__':
    #
    # path='dicoms/dicoms2/IMG-0007-00008.dcm'
    # read(path)



    path='/home/DataBase4/cto_gan_data/RAO_CAU'
    '''1'''
    # rename_same_dicom(path)
    new_merged_path='/home/DataBase4/cto_gan_data/RAO_CAU'#LAO_CRA RAO_CAU
    '''2'''
    # merge(path,new_merged_path)
    '''3''' 
    make_each_dic_into_a_path(new_merged_path)

    '''4'''
    files=list_all_files(new_merged_path)
    pbar=tqdm(files)
    for  file in pbar:
        pbar.set_description("Processing %s" % file)
        split_to_frames(file)

    '''5'''
    ### run add_format_frame.py

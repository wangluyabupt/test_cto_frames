import os
import re
import shutil
import sys
# sys.path.append("/home/wly/anaconda3/lib/python3.7/site-packages")
import cv2

def find_each_child_files(rootdir):
    _files = []

    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)

    for i in range(0, len(list_file)):
        # 构造路径
        dicomi = os.path.join(rootdir, list_file[i])
        framesj = os.listdir(dicomi)
        format_file = ''
        for j in range(0, len(framesj)):
            # if os.path.isfile(framesj[j]):
            #     format_file=framesj[j]
            if framesj[j].endswith('.jpg'):
                format_file = framesj[j]
        for j2 in range(0, len(framesj)):
            # if os.path.isdir(framesj[j2]):
            #     with open(os.path.join(framesj[j2],os.path.basename(format_file)),'w') as fw:
            #         fw.write(format_file)
            if not framesj[j2].endswith('.jpg') and not framesj[j2].endswith('.dcm'):
                origin_dir = os.path.join(dicomi, framesj[j2])
                # with open(os.path.join(origin_dir,os.path.basename(format_file)),'w') as fw:
                #     fw.write(format_file)
                img = cv2.imread(os.path.join(dicomi, format_file))
                nn = os.path.join(origin_dir, os.path.basename(format_file))
                cv2.imwrite(nn, img)

        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归

    #     if os.path.isdir(path):
    #         _files.extend(find_each_child_files(path))
    #     if os.path.isfile(path):
    #
    #         dir_path = os.path.dirname(path)
    #         l=os.listdir(dir_path)
    #         add_format_frames(path,l)
    #         _files.append(dir_path)
    # return _files


def add_format_frames(format_file, dir_path_list):
    base_name = os.path.basename(format_file)
    for dir in dir_path_list:
        file = os.path.join(dir, base_name)
        # with open(file,'wb') as fw:
        #     fw.write(format_file)
        img = cv2.imread(format_file)
        cv2.imwrite(file, img)


def delete_format_frames(new_merged_path):
    _files = []
    rootdir = new_merged_path

    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)

    for i in range(0, len(list_file)):
        # 构造路径
        dicomi = os.path.join(rootdir, list_file[i])
        framesj = os.listdir(dicomi)
        format_file = ''
        for j in range(0, len(framesj)):
            # if os.path.isfile(framesj[j]):
            #     format_file=framesj[j]
            if framesj[j].endswith('.jpg'):
                format_file = framesj[j]
        if format_file == '':
            print('dicom can not be used :', list_file[i])
            continue
        for j2 in range(0, len(framesj)):
            # if os.path.isdir(framesj[j2]):
            #     with open(os.path.join(framesj[j2],os.path.basename(format_file)),'w') as fw:
            #         fw.write(format_file)
            if not framesj[j2].endswith('.jpg') and not framesj[j2].endswith('.dcm'):
                origin_dir = os.path.join(dicomi, framesj[j2])
                format_last_num = format_file.split('.')[-2].split('_')[-1]
                frames_name = os.path.basename(framesj[j2])
                j2_last_num = frames_name.split('es')[1]

                if str(j2_last_num) == str(format_last_num):
                    shutil.rmtree(origin_dir)


def add_last_frames(new_merged_path):
    _files = []
    rootdir = new_merged_path
    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)
    print(list_file)


    for i in range(0, len(list_file)):
        # 构造路径
        err=list_file[i]
        print('dicomi:',err)
        dicomi = os.path.join(rootdir,err )
        framesj = os.listdir(dicomi)
        format_file = ''
        num_dict={}
        for j2 in range(0, len(framesj)):
            if framesj[j2].endswith('.dcm') or framesj[j2].endswith('.jpg'):
                continue
            else:

                num_dict[framesj[j2]]=int(framesj[j2].split('es')[1])



        s_dict=sorted(num_dict.items(), key=lambda e:e[1], reverse=True)
        max_k,max_v=s_dict[0]
        format_frames_path=os.path.join(dicomi,max_k)
        format_frames_file=os.listdir(format_frames_path)[0]
        img = cv2.imread(os.path.join(format_frames_path,format_frames_file))
        cv2.imwrite(os.path.join(dicomi,format_frames_file), img)
        continue




def delete_other_frames(dicoms_li,frames_li):
    dicoms=os.listdir(new_merged_path)
    for  dicom in dicoms:
        dicom_num=int(dicom.split('dicom')[-1])
        if dicom_num<=30:
            continue
        file_need_to_save_num=frames_li[dicoms_li.index(dicom_num)]
        dicom_path=os.path.join(new_merged_path,dicom)
        file_may_jpg=os.listdir(dicom_path)
        for file in file_may_jpg:
            if not '.jpg' in file:
                continue
            file_num=int(file.split('_')[-1].split('.')[0])
            file_path=os.path.join(dicom_path,file)
            if file_num!=file_need_to_save_num:
                os.remove(file_path)
                


            





if __name__ == '__main__':
    # path = 'dicoms'
    # find_each_child_files(path)
    '''trick add last frames as format frames'''
    # new_merged_path = 'dicom_113/merged'
    # add_last_frames(new_merged_path)

    '''delete other frames according to index from multi_plot rst ；save format frame.jpg'''
    new_merged_path='/home/DataBase4/cto_gan_data/RAO_CAU/merged'
    # dicoms_li=[31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180]
    # frames_li=[41, 33, 55, 48, 50, 29, 32, 39, 35, 36, 34, 59, 38, 58, 49, 41, 26, 51, 34, 32, 25, 27, 37, 18, 21, 21, 0 , 39, 22, 26, 43,  0, 32, 33, 49, 49, 52, 40, 44, 28, 47, 36, 29, 0,  22, 50, 44, 22, 31, 33, 29, 44, 40, 35, 40, 32, 24,  0, 25, 29, 31, 27, 29, 32, 25, 22, 35, 34, 22,  28,  34,  34,  37,  37,  49,  28,  46,  42,  26, 46,  32,  25, 29 ,   20, 34,  37,   26,  37,  49,  37,  43,  47,  41,  33,   36,  38,  26,  37,  49, 29,  41,  54,  23,  21,  22,  33,  32,  49,   34,  44,  43,  49, 43,  33,  36,  59,  33,  35,  36,  44, 44,  46,   0,    0,  0,    30, 25,  25,  0,    33, 0,   0,  0,     37, 0,   24,  43,  39,   21,  43, 79,  31,  37,  35,  27,  40,  40,  36, 52,  32]
    # if len(dicoms_li)!=len(frames_li):
    #     print('ERROR!!!')
    # delete_other_frames(dicoms_li,frames_li)



    '''add_format_frames'''
    find_each_child_files(new_merged_path)

    '''delete_format_frames'''

    # delete_format_frames(new_merged_path)

    # format_file = 'IMG-0006-000000.jpg'
    # add_format_frames(format_file, files)

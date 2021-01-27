import os
import re
import shutil

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









if __name__ == '__main__':
    # path = 'dicoms'
    # find_each_child_files(path)
    '''trick add last frames as format frames'''
    new_merged_path = 'dicom_113/merged'
    add_last_frames(new_merged_path)

    '''add_format_frames'''
    # new_merged_path = 'dicoms_1217/merged'
    find_each_child_files(new_merged_path)

    '''delete_format_frames'''

    delete_format_frames(new_merged_path)

    # format_file = 'IMG-0006-000000.jpg'
    # add_format_frames(format_file, files)

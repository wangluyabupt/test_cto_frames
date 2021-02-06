import numpy as np
import os 
import shutil
import sys
# import SimpleITK as sitk
sys.path.append("/home/wly/anaconda3/lib/python3.7/site-packages")
import dicom
from tqdm import tqdm
def get_FileSize(filePath):
    # filePath = unicode(filePath, 'utf8')
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024*1024)
    return round(fsize, 2)

def check_position(root):
    dcm_list=os.listdir(root)
    position_dic={}
    for i in dcm_list:
        dcm = dicom.read_file(os.path.join(root,i))
        info = {}
        info["PatientID"] = dcm.PatientID
        f=dcm.PositionerPrimaryAngle
        s=dcm.PositionerSecondaryAngle
        info['PositionerPrimaryAngle']=f
        info['PositionerSecondaryAngle']=s
        position=str(f)+'_'+str(s)
        position_dic[position] = position_dic.get(position, 0) + 1
        # print(i,info)
    print(position_dic)

def get_position(dcm_path):
    dcm = dicom.read_file(dcm_path)
    info = {}
    f=dcm.PositionerPrimaryAngle
    s=dcm.PositionerSecondaryAngle
    info['PositionerPrimaryAngle']=f
    info['PositionerSecondaryAngle']=s
    # classifier position 

    position_type=str(f)+'_'+str(s)
    return position_type

def get_angel(filepath):
    ds = dicom.read_file(filepath)
    if ds is None:
        return None, None
    else:
        try:
            primary=int(ds.PositionerSecondaryAngle)
            secondary=int(ds.PositionerSecondaryAngle)
            return  primary,secondary
        except Exception as e:
            print(e)
            return None, None



# 根据传入的两个dicom角度信息，判断其体位；

def pos_classification(primary, secondary):
    # 像限确定；
    # 足位，secondary < 0
    if np.abs(primary) <= 15 and np.abs(secondary) <= 15:
        return 'AP'

    if primary == 0:
        if secondary < 0:
            return 'CAU'
        else:
            return 'CRA'
    elif secondary == 0:
        if primary < 0:
            return 'RAO'
        else:
            return 'LAO'

    y = np.abs(primary)
    x = np.abs(secondary)
    ## 处理成弧度；
    y = np.pi * float(y) / 180.0
    x = np.pi * float(x) / 180.0
    border = np.pi * float(11.25) / 180
    # border = np.pi * float(22.5) / 180

    if np.tan(y) / np.tan(x) < np.tan(border):
        if secondary < 0:
            return 'CAU'
        else:
            return 'CRA'
    if np.tan(x) / np.tan(y) < np.tan(border):
        if primary < 0:
            return 'RAO'
        else:
            return 'LAO'

    if primary > 0 and secondary > 0:
        return 'LAO_CRA'
    elif primary > 0 and secondary < 0:
        return 'LAO_CAU'
    elif primary < 0 and secondary > 0:
        return 'RAO_CRA'
    elif primary < 0 and secondary < 0:
        return 'RAO_CAU'

def process():
    patient_index=0
    all_dcm_num=0
    position_dic={}
    ####
    pbar=tqdm(patient_paths_list)
    for patient_path in pbar:
        pbar.set_description("Processing %s" % patient_path)
        patient_file=patient_path.split('/')[-1]
    # pbar=tqdm(patient_files_list)
    # for patient_file in pbar:
    #     pbar.set_description("Processing %s" % patient_file)
        # patient_path=os.path.join(origin_disk_path,patient_file)
        patient_date_file_list=os.listdir(patient_path)
        for patient_date_file in patient_date_file_list:

            patient_date_file_path=os.path.join(patient_path,patient_date_file)
            if os.path.isfile(patient_date_file_path):
                continue
            patient_date_dcms=os.listdir(patient_date_file_path)
            
            dcm_index=0
            for dcm in patient_date_dcms:
                if os.path.splitext(dcm)[-1] !='.dcm':
                    continue
                dcm_path=os.path.join(patient_date_file_path,dcm)
                #判断文件大小，小于5M的pass
                dcm_size=get_FileSize(dcm_path)
                if dcm_size < 5:
                    continue
                primary,secondary=get_angel(dcm_path)
                if primary==None:
                    continue
                position_type=pos_classification(primary, secondary)

                position_dic[position_type] = position_dic.get(position_type, 0) + 1
                new_dcm=os.path.splitext(patient_file)[0]+str(all_dcm_num)+dcm
                target_dick_pos_path=os.path.join(target_dick_path,position_type)

                if not os.path.exists(target_dick_pos_path):
                    os.mkdir(target_dick_pos_path)
                
                need_to_save_path=os.path.join(target_dick_pos_path,new_dcm)
                shutil.copy(dcm_path, need_to_save_path)
                dcm_index+=1
                all_dcm_num+=1

                # print('{} moved!'.format(new_dcm))
    print(position_dic)
    print('all_dcm_num:',all_dcm_num)



if __name__=='__main__':

    '''
    export PYTHONPATH=$PYTHONPATH:/home/wly/anaconda3/lib/python3.7/site-packages
    '''
    
    os.chdir('/home')
    origin_disk_path='DataBase3/segmentation'
    target_dick_path='DataBase4/cto_gan_data/'
    day_list=os.listdir(origin_disk_path)
    ###
    patient_files_list=[]
    patient_paths_list=[]
    for day in day_list:
        day_path=os.path.join(origin_disk_path,day)
        for xl in os.listdir(day_path):
            xl_path=os.path.join(day_path,xl)
            for patien in os.listdir(xl_path):
                if 'ALL'in patien or os.path.isfile(os.path.join(xl_path,patien)):
                    continue
                patient_files_list.append(patien)
                patient_paths_list.append(os.path.join(xl_path,patien))
    ###



    # patient_files_list=os.listdir(origin_disk_path)

    patient_num=len(patient_files_list)
    print('原始人数：',patient_num)

    process()
    '''
    {'LAO_CRA': 708, 'RAO': 122, 'CRA': 306, 'LAO_CAU': 310, 'CAU': 306, 'AP': 50, 
    'LAO': 943, 'RAO_CRA': 448, 'RAO_CAU': 366}
    all_dcm_num: 3559   
    CRA、CAU、LAO_CAU、RIGHT四类吗？
    对  按照分割的经验来说分这四种就够了 你可以这样分试试，后面有问题再调整

    去除小dcm文件后：

    现在换成了其他3个路径：
    {'LAO_CRA': 372, 'AP': 303, 'RAO_CAU': 180}
    all_dcm_num: 855

    '''




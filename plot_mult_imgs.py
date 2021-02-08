import os
from PIL import Image, ImageDraw
from PIL import ImageFont
import math
from tqdm import tqdm
root='/home/DataBase4/cto_gan_data/RAO_CAU/find_merged_result'
os.chdir(root)





# 定义图像拼接函数
def image_compose(is_res):
    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]

    # 简单的对于参数的设定和实际图片集的大小进行数量判断
    if len(image_names) > IMAGE_ROW * IMAGE_COLUMN:
        raise ValueError("合成图片的参数和要求的数量不能匹配！")

    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            i=IMAGE_COLUMN * (y - 1) + x - 1
            if i >= len(image_names):
                break

            try:
                from_image = Image.open(IMAGES_PATH + '/'+image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                    (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
                draw = ImageDraw.Draw(from_image)
                fnt = ImageFont.truetype('/home/wly/FZLTHPro_GB18030_Zhun.otf',size=40)
                if not is_res:
                    '''选标准帧的时候的命名'''
                    text_content=image_names[IMAGE_COLUMN * (y - 1) + x - 1].split('_')[-1].split('.')[0]
                else:
                    '''反选res的时候的命名'''
                    two_img=image_names[IMAGE_COLUMN * (y - 1) + x - 1].split('-')
                    text_content=two_img[2].split('_')[-1].split('.')[0]+'_'+two_img[5].split('_')[-1].split('.')[0]
                draw.text(xy=(0,0),text= text_content,fill=255, font=fnt)
    
                del draw

                to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
            except:
                print('err!!!:',image_names[IMAGE_COLUMN * (y - 1) + x - 1])
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图

if __name__=='__main__':
    new_dicom_path='/home/DataBase4/cto_gan_data/RAO_CAU/find_merged_result/merge_rst'
    if not os.path.exists(new_dicom_path):
        os.mkdir(new_dicom_path)

    dicoms_list=os.listdir(root)
    pbar=tqdm(dicoms_list)
    is_res=True
    for path in pbar:
        i=path.split('dicom')[-1]
        pbar.set_description("Processing %s" % path)
        IMAGES_FORMAT = ['.jpg','.JPG','.png','.PNG']  # 图片格式
        IMAGE_SIZE = 255  # 每张小图片的大小
        dicom_path=os.path.join(root,path)
        IMAGES_PATH = dicom_path
        img_num=len(os.listdir(dicom_path))

        # IMAGE_ROW = int(math.sqrt(img_num) ) # 图片间隔，也就是合并成一张图后，一共有几行
        # IMAGE_COLUMN = IMAGE_ROW+1  # 
        IMAGE_COLUMN=4
        IMAGE_ROW = int(img_num/IMAGE_COLUMN)+1

        ####
        # IMAGE_SAVE_PATH = dicom_path + '/merge_{}.jpg'.format(str(i)) # 图片转换后的地址

        IMAGE_SAVE_PATH = new_dicom_path + '/merge_{}.jpg'.format(str(i)) # 图片转换后的地址

        image_compose(is_res)  # 调用函数


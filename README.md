# test_cto_frames
main first
1、操作choose_dcm.py
    首先在database3的segmentation的20190221_2(90+病人，290+日期,5000+张dcm)
    中每个病人的每个日期中选取5个dicom，重命名文件,至新的文件夹cto_gan_data
        1. 放路径的时候记得按名字_次数(日期）/ dcm原始名字 例如： xaioming_1/ xiaoming_2/ lili_3/ songming_4/ songming_5/ ...
        2. 体位信息：
            1. 左冠中：CRA是前降支【左主干横行输出】很清楚，CAU则是用来观测回旋支【左主干偏下方输出，有分支】的（LAO_CAU特殊）
            2. 右冠：左侧下来往右的钩子
            3. 有分类规则：
                1. 分割：LAO/RAO + CRA/CAU 以及Right 一共 5类
                2. primary angle：对应LAO(+)或RAO(-)
                    second angle：对应CRA(+)或CAU(-)

2、目前仅针对LAO pass 
3、数据集20190221_2误删，现在对segmentation中仅剩的3个日期文件夹72例病患进行统计

2、操作trans_dic_to_frames.py
   dicom变帧（frames），每帧进入所在dicom_i的frame_i文件夹，同时复制一份到dicom_i

操作plot_mult_imgs.py
2、对DataBase4/cto_gan_data的LAO_CRA 中dicom frames 数据进行观察+手动筛选
    1、利用复制到dicom_i中的jpg合并成merge_i.jpg（4列比较合适）
    1、除去导丝（这三个数据集不怎么有导丝）
    2、人工选出标准帧（充盈的，尤其是支端）

4、操作add_format_frames.py
    1、把上一步选出的标准帧jpg留在dicom_i中
    3、把标准帧加入每一个frame_i(执行py中的find_each_child_files()函数时，引入cv2，注意用python3.7.3-bit('bse':conda)编译器)
    2、同时删除标准帧i对应的dicom_i的frame_i文件夹


5、分割 操作cto_frames工程

6、训练 操作pix2pix
        
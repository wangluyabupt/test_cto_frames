# test_cto_frames
origin
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
   1、dicom变帧（frames），每帧进入所在dicom_i的frame_i文件夹，同时复制一份到dicom_i
   2、这里忽略了前面的一些帧（百分之X0），为了更方便的选取到标准帧（充盈）

操作plot_mult_imgs.py
2、对DataBase4/cto_gan_data的LAO_CRA 中dicom frames 数据进行观察+手动筛选
    1、利用复制到dicom_i中的jpg合并成merge_i.jpg（4列比较合适）
    1、除去导丝（这三个数据集不怎么有导丝）
    2、人工选出标准帧（充盈的，尤其是支端）

4、操作add_format_frames.py
    1、把上一步选出的标准帧jpg留在dicom_i中
    3、把标准帧加入每一个frame_i(执行py中的find_each_child_files()函数时，引入cv2，注意用python3.7.3-bit('base':conda)编译器)
    2、同时删除标准帧i对应的dicom_i的frame_i文件夹


5、分割 操作cto_frames工程
    1、这一部分要考虑一下怎么融合进大网络
    2、
6、操作find_mer_rst.py  
    1、将合并结果res放入示例'/home/DataBase4/cto_gan_data/RAO_CAU/find_merged_result'路径
    2、合并的时候有个问题，就是两张图的序号可能会被随机选择为第一、第二张图片，所以要重新整合一下合并图上每一个小图片左上角的命名
7、再次操作plot_mul_imgs.py将反选出的res结果合并成一整幅图片来实现人工选择合适的数据对
    1、选择的时候最好不要选择距离标准帧很近的帧
    2、这一步其实可以考虑重新生成一下钱面几帧
    1、选出的数据对直接去/home/DataBase4/cto_gan_data/RAO_CAU/merged下面每个dicom的frame的moved去选择已经实现了位移弥补的数据帧对即可
8、操作find_mer_rst.py 将选出的数据放入AB路径来操作pix2pix
    1、 A是long分支，是标签
    2、 B是要被预测的

6、训练 操作pix2pix
    1、result中的html文件中图片链接是依赖于工程的，所以使用插件live server打开该html才可以显示（右击：open in live server）
    2、

流程更新记录：
1、DataBase3/segmentation/目前2017年的数据

2、操作choose_dcm.py，每个病人的每个日期中选取前7 dicom，trick：开头几个通常是没有导丝的
    原始人数702，用非conda环境的python3（其实终端显示的是base）,选取前7个
    {'RAO_CRA': 76, 'AP': 2, 'LAO': 73, 'RAO_CAU': 48, 'LAO_CAU': 53, 'CRA': 66, 'CAU': 38, 'LAO_CRA': 63, 'RAO': 4}
    all_dcm_num: 423
2、操作trans_dic_to_frames.py 时，留下帧的全部信息
    本次仅针对LAO,用非conda环境的python3（其实终端显示的是base）
3、操作plot_mult_imgs.py
    修改#1路径，合成原始帧
    人工选出标准帧（充盈的，尤其是支端）【每个dicom选一张】
4、操作add_format_frames.py
    ???用'base':conda环境的python3

5、分割 操作cto_frames工程
    用'base':conda环境的python3


6、操作find_mer_rst.py (不切换上一步的环境)
    按提示去plot_mult_imgs.py中 #1 merged_multi_imgs切换为 #2 find_merged_result
7、返回find_mer_rst.py 
    组合AB




反思：
1、代码可以不优美但是注意结果的保存于整合用在论文中做结果展示
2、
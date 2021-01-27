import os


def show_mer_rst(new_merged_path):
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
            # if os.path.isdir(framesj[j2]):
            #     with open(os.path.join(framesj[j2],os.path.basename(format_file)),'w') as fw:
            #         fw.write(format_file)
            if framesj[j2].endswith('.dcm') or framesj[j2].endswith('.jpg'):
                continue
            else:

                num_dict[framesj[j2]]=int(framesj[j2].split('es')[1])

if __name__=='__main__':
    mer_rst_path=''
    show_mer_rst(mer_rst_path)
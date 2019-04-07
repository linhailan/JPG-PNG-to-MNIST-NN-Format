import os
from PIL import Image
from array import *
from random import shuffle
import shutil



def move_file(src_path, dst_path, file):
    print("from : ",src_path)
    print("to   : ",dst_path)
    try:
        # cmd = 'chmod -R +x ' + src_path
        # os.popen(cmd)
        f_src = os.path.join(src_path, file)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        f_dst = os.path.join(dst_path, file)
        shutil.move(f_src, f_dst)
    except Exception as e:
        print("move file ERROR: ",e)


# Load from and save to
def loadfile(Names):
    FileList = []
    for dirname in os.listdir(Names[0][0]):
        path = os.path.join(Names[0][0], dirname)
        print(path)
        i = 0
        for filename in os.listdir(path):
            if i >= 50:
                break
            if filename.endswith(".jpg"):
                print(i,":",filename)
                src_path = os.path.join(Names[0][0],dirname)
                dst_path = os.path.join(Names[1][0],dirname)
                move_file(src_path,dst_path,filename)
                i += 1


Names = [['./training-images','train'], ['./test-images','test']]
for name in Names:
    FileList = []
    for dirname in os.listdir(name[0]):
        path = os.path.join(name[0],dirname)
        print(path,":",len(os.listdir(path)))





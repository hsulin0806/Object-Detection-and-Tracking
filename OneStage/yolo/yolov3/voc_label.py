import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#我的项目中有6个类别，类别名称在这里修改
classes = ["people","fire_extinguisher","fireplug","car","bicycle","motorcycle"]
def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    #这里改为.xml文件夹的路径
    in_file = open('/home/cai/Desktop/dataset/data/Annotations/%s.xml'%(image_id))
    #这里是生成每张图片对应的.txt文件的路径
    out_file = open('/home/cai/Desktop/yolo_dataset/objectdetection/labels/%s.txt'%(image_id),'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)#

    for obj in root.iter('object'):
        cls = obj.find('name').text
        if cls not in classes :
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
#这里是train.txt文件的路径
image_ids_train = open('/home/cai/Desktop/yolo_dataset/objectdetection/train.txt').read().strip().split()
#这里是val.txt文件的路径
image_ids_val = open('/home/cai/Desktop/yolo_dataset/objectdetection/val.txt').read().strip().split()

list_file_train = open('object_train.txt', 'w')
list_file_val = open('object_val.txt', 'w')
for image_id in image_ids_train:
    #这里改为样本图片所在文件夹的路径
    list_file_train.write('/home/cai/Desktop/yolo_dataset/objectdetection/JPEGImages/%s.jpg\n'%(image_id))
    #convert_annotation(image_id)
list_file_train.close()
for image_id in image_ids_val:
    #这里改为样本图片所在文件夹的路径
    list_file_val.write('/home/cai/Desktop/yolo_dataset/objectdetection/JPEGImages/%s.jpg\n'%(image_id))
    #convert_annotation(image_id)
list_file_val.close()

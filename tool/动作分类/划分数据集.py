import os
import shutil
import random

# 路径配置
pic_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic_all'
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt_all'
train_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/train'
val_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/val'

# 确保输出文件夹结构存在
os.makedirs(os.path.join(train_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(train_folder, 'labels'), exist_ok=True)
os.makedirs(os.path.join(val_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(val_folder, 'labels'), exist_ok=True)

# 获取所有图片文件
images = [f for f in os.listdir(pic_folder) if f.endswith('.png')]
total_images = len(images)

# 打乱顺序
random.shuffle(images)

# 计算训练集和验证集的数量
train_size = int(total_images * 0.95)
val_size = total_images - train_size

# 划分训练集和验证集
train_images = images[:train_size]
val_images = images[train_size:]

# 复制文件到训练集文件夹
for img_file in train_images:
    txt_file = img_file.replace('.png', '.txt')
    shutil.copy(os.path.join(pic_folder, img_file), os.path.join(train_folder, 'images', img_file))
    shutil.copy(os.path.join(txt_folder, txt_file), os.path.join(train_folder, 'labels', txt_file))

# 复制文件到验证集文件夹
for img_file in val_images:
    txt_file = img_file.replace('.png', '.txt')
    shutil.copy(os.path.join(pic_folder, img_file), os.path.join(val_folder, 'images', img_file))
    shutil.copy(os.path.join(txt_folder, txt_file), os.path.join(val_folder, 'labels', txt_file))

print("数据集划分完成")

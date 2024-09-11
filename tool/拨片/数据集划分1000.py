import os
import shutil

# 路径配置
pic_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic'
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/txt'
train_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/train_2000'
val_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/val_1000'

# 确保输出文件夹结构存在
os.makedirs(os.path.join(train_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(train_folder, 'labels'), exist_ok=True)
os.makedirs(os.path.join(val_folder, 'images'), exist_ok=True)
os.makedirs(os.path.join(val_folder, 'labels'), exist_ok=True)

# 获取所有图片文件
images = [f for f in os.listdir(pic_folder) if f.endswith('.png')]
total_images = len(images)

# 排序图片文件
images.sort()

# 设置测试集的数量
test_size = 1000

# 划分测试集和训练集
test_images = images[:test_size]
train_images = images[test_size:]

# 复制文件到验证集文件夹
for img_file in test_images:
    txt_file = img_file.replace('.png', '.txt')
    shutil.copy(os.path.join(pic_folder, img_file), os.path.join(val_folder, 'images', img_file))
    shutil.copy(os.path.join(txt_folder, txt_file), os.path.join(val_folder, 'labels', txt_file))

# 复制文件到训练集文件夹
for img_file in train_images:
    txt_file = img_file.replace('.png', '.txt')
    shutil.copy(os.path.join(pic_folder, img_file), os.path.join(train_folder, 'images', img_file))
    shutil.copy(os.path.join(txt_folder, txt_file), os.path.join(train_folder, 'labels', txt_file))

print("数据集划分完成")

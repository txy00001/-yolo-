import os
import shutil
import random
from collections import defaultdict

# 原始图片和标注文件路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic_all'
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt_all'

# 训练集和验证集路径
train_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/cls_train'
val_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/cls_val'

# 类别映射
label_map = {
    0: "未开始",
    1: "放置底板",
    2: "放PCB板1",
    3: "放泡棉",
    4: "放PCB板2",
    5: "完整产品"
}

# 确保训练集和验证集文件夹存在
for folder in [train_folder, val_folder]:
    os.makedirs(folder, exist_ok=True)
    for label in label_map.values():
        os.makedirs(os.path.join(folder, label), exist_ok=True)

# 分类图片
images_by_class = defaultdict(list)

for filename in os.listdir(image_folder):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        txt_path = os.path.join(txt_folder, os.path.splitext(filename)[0] + '.txt')
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    label_id, _, _, _, _ = map(float, line.strip().split())
                    label_id = int(label_id)
                    if label_id in label_map:
                        images_by_class[label_id].append(filename)
                        break  # 假设每张图片只有一个主要类别

# 按照9:1的比例划分训练集和验证集，并移动文件
for label_id, images in images_by_class.items():
    random.shuffle(images)
    split_idx = int(len(images) * 0.9)
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    for image in train_images:
        src_image_path = os.path.join(image_folder, image)
        dest_image_path = os.path.join(train_folder, label_map[label_id], image)
        shutil.copy(src_image_path, dest_image_path)

    for image in val_images:
        src_image_path = os.path.join(image_folder, image)
        dest_image_path = os.path.join(val_folder, label_map[label_id], image)
        shutil.copy(src_image_path, dest_image_path)

print("图片分类和数据集划分完成。")

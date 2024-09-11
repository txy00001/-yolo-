import os
import shutil

# 定义数据集文件夹路径
images_dir_1 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_1 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_2 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_2 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_3 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_3 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_4 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_4 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_5 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_5 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_6 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_6 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_7 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_7 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_8 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_8 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_9 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_9 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_10 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_10 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_11 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_11 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

images_dir_12 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
labels_dir_12 = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'


# 定义新文件夹路径
merged_images_dir = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic_all'
merged_labels_dir = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt_all'

# 创建新文件夹
os.makedirs(merged_images_dir, exist_ok=True)
os.makedirs(merged_labels_dir, exist_ok=True)

# 函数用于复制文件并重命名
def copy_and_rename_files(src_images_dir, src_labels_dir, start_index):
    image_files = sorted([f for f in os.listdir(src_images_dir) if f.endswith(('.jpg', '.png'))])
    label_files = sorted([f for f in os.listdir(src_labels_dir) if f.endswith('.txt')])

    if len(image_files) != len(label_files):
        raise ValueError(f"The number of images and labels in {src_images_dir} and {src_labels_dir} do not match.")

    for i, (image_file, label_file) in enumerate(zip(image_files, label_files)):
        new_index = start_index + i + 1
        new_image_name = f"{new_index:06d}.png"
        new_label_name = f"{new_index:06d}.txt"

        # 复制并重命名文件
        shutil.copy(os.path.join(src_images_dir, image_file), os.path.join(merged_images_dir, new_image_name))
        shutil.copy(os.path.join(src_labels_dir, label_file), os.path.join(merged_labels_dir, new_label_name))

    return len(image_files)

# 从第一个数据集开始复制和重命名
current_index = 0
current_index += copy_and_rename_files(images_dir_1, labels_dir_1, current_index)

# 接着复制和重命名第二个数据集
current_index += copy_and_rename_files(images_dir_2, labels_dir_2, current_index)

current_index += copy_and_rename_files(images_dir_3, labels_dir_3, current_index)
current_index += copy_and_rename_files(images_dir_4, labels_dir_4, current_index)

current_index += copy_and_rename_files(images_dir_5, labels_dir_5, current_index)
current_index += copy_and_rename_files(images_dir_6, labels_dir_6, current_index)
current_index += copy_and_rename_files(images_dir_7, labels_dir_7, current_index)
current_index += copy_and_rename_files(images_dir_8, labels_dir_8, current_index)
current_index += copy_and_rename_files(images_dir_9, labels_dir_9, current_index)
current_index += copy_and_rename_files(images_dir_10, labels_dir_10, current_index)
current_index += copy_and_rename_files(images_dir_11, labels_dir_11, current_index)
current_index += copy_and_rename_files(images_dir_12, labels_dir_12, current_index)

print("数据集合并完成")

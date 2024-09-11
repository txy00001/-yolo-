import os
import shutil

# 源图片文件夹路径
source_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic'
# 目标图片文件夹路径
destination_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic_2'

# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, filename)
    
    # 复制文件
    shutil.copy2(source_path, destination_path)
    print(f'文件 {filename} 已复制到 {destination_folder}')

print("文件复制完成。")

import os
from PIL import Image

# 原始文件夹路径
source_dir = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/螺丝锁付分类'
# 新的文件夹路径
target_dir = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/640'

# 截取参数
crop_x_start = 780  # 截取开始的 x 坐标
crop_width = 1280    # 截取的宽度
crop_x_end = crop_x_start + crop_width  # 计算结束的 x 坐标

# 遍历原始文件夹
for root, dirs, files in os.walk(source_dir):
    for file in files:
        # 检查文件扩展名，确保是图片文件
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # 构建原始文件的完整路径
            source_file_path = os.path.join(root, file)
            
            # 打开图片并进行截取
            with Image.open(source_file_path) as img:
                # 截取区域 (crop_x_start, 0, crop_x_end, img.height)
                cropped_img = img.crop((crop_x_start, 0, crop_x_end, img.height))
                
                # 构建新的文件夹路径
                relative_path = os.path.relpath(root, source_dir)
                new_folder_path = os.path.join(target_dir, relative_path)
                
                # 创建新的文件夹（如果不存在）
                os.makedirs(new_folder_path, exist_ok=True)
                
                # 修改新文件的保存路径，并统一保存为jpg格式
                new_file_name = os.path.splitext(file)[0] + '.jpg'
                new_file_path = os.path.join(new_folder_path, new_file_name)
                
                # 保存截取后的图片为JPEG格式
                cropped_img.save(new_file_path, format='JPEG')

print("图片截取并保存完成！")

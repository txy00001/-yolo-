import os
import shutil

# 设置目标路径
base_path = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/螺丝锁付分类/val'

# 遍历每个子文件夹
for folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, folder)
    
    # 确保是文件夹
    if os.path.isdir(folder_path):
        # 获取文件夹中的所有图片文件
        images = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        # 如果图片数量超过 30，则删除多余的图片
        if len(images) > 30:
            # 保留前 30 张图片
            images_to_keep = images[:30]
            
            # 删除多余的图片
            for image in images:
                if image not in images_to_keep:
                    image_path = os.path.join(folder_path, image)
                    os.remove(image_path)  # 删除文件
                    print(f"Deleted: {image_path}")

print("处理完成！")

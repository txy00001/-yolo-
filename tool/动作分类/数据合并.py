import os
import json
import shutil

# 源文件夹列表
source_folders = [
    '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/动作分类',
    
]
# 新的目标文件夹
target_pic_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
target_json_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/json'

# 创建目标文件夹
os.makedirs(target_pic_folder, exist_ok=True)
os.makedirs(target_json_folder, exist_ok=True)

image_id = 0

# 处理每个源文件夹
for folder in source_folders:
    image_folder = os.path.join(folder, 'images', 'default')
    annotation_file = os.path.join(folder, 'annotations', 'default.json')

    # 读取JSON文件
    with open(annotation_file, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    # 处理每个图片和其标注
    for item in annotations["items"]:
        # 获取旧的图片路径
        old_image_path = os.path.join(image_folder, item["image"]["path"])

        # 创建新的图片名称
        new_image_name = f'frame_{image_id:06d}.png'
        new_image_path = os.path.join(target_pic_folder, new_image_name)

        # 复制图片到新的文件夹
        shutil.copy2(old_image_path, new_image_path)

        # 更新标注信息
        item["id"] = f'frame_{image_id:06d}'
        item["image"]["path"] = new_image_name
        if "media" in item:
            item["media"]["path"] = new_image_name

        # 保留原来的图像大小
        item["image"]["size"] = [1080, 1920]  # 假设所有图片尺寸相同，如果不同，需要从原数据中获取

        # 创建单独的JSON结构
        new_annotations = {
            "info": annotations.get("info", {}),
            "categories": {
                "label": annotations["categories"]["label"],
                "points": annotations["categories"]["points"]
            },
            "items": [item]
        }

        # 单独JSON文件路径
        target_json_file = os.path.join(target_json_folder, f'frame_{image_id:06d}.json')

        # 将新的JSON结构写入文件
        with open(target_json_file, 'w', encoding='utf-8') as f:
            json.dump(new_annotations, f, ensure_ascii=False, indent=4)

        # 更新图片ID
        image_id += 1

print(f'整合完成：图片保存到 {target_pic_folder}，标注文件保存到 {target_json_folder}')

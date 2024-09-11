import os
import json
import shutil

# 源文件夹列表
source_folders = ['/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/task_拨片测试1-2024_07_15_10_00_41-datumaro 1.0', 
                  '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/task_拨片测试2-2024_07_15_10_33_24-datumaro 1.0', 
                  '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/task_拨片测试3-2024_07_15_10_56_51-datumaro 1.0', 
                  '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/task_拨片测试4-2024_07_15_11_16_45-datumaro 1.0']
# 新的目标文件夹
target_pic_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic'
target_json_file = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/json/annotations.json'

# 创建目标图片文件夹
os.makedirs(target_pic_folder, exist_ok=True)

# 初始化新的JSON结构
new_annotations = {
    "info": {},
    "categories": {
        "label": {
            "labels": [],
            "attributes": []
        },
        "points": {
            "items": []
        }
    },
    "items": []
}

image_id = 0

# 处理每个源文件夹
for folder in source_folders:
    image_folder = os.path.join(folder, 'images', 'default')
    annotation_file = os.path.join(folder, 'annotations', 'default.json')
    
    # 读取JSON文件
    with open(annotation_file, 'r', encoding='utf-8') as f:
        annotations = json.load(f)
    
    # 更新类别和属性信息（假设这些信息在所有文件夹中相同）
    if not new_annotations["categories"]["label"]["labels"]:
        new_annotations["categories"]["label"]["labels"] = annotations["categories"]["label"]["labels"]
    if not new_annotations["categories"]["label"]["attributes"]:
        new_annotations["categories"]["label"]["attributes"] = annotations["categories"]["label"]["attributes"]
    
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
        item["media"]["path"] = new_image_name
        
        # 保留原来的图像大小
        item["image"]["size"] = [1080, 1920]  # 假设所有图片尺寸相同，如果不同，需要从原数据中获取
        
        # 添加更新后的标注信息到新的JSON结构
        new_annotations["items"].append(item)
        
        # 更新图片ID
        image_id += 1

# 将新的JSON结构写入文件
with open(target_json_file, 'w', encoding='utf-8') as f:
    json.dump(new_annotations, f, ensure_ascii=False, indent=4)

print(f'整合完成：图片保存到 {target_pic_folder}，标注文件保存为 {target_json_file}')
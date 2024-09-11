import os
import json

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic'
# 原始JSON文件路径
original_json_path = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/json/annotations.json'
# 新的JSON文件路径
new_json_path = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/json/annotations_new.json'

# 获取图片文件列表
image_files = set(os.listdir(image_folder))

# 读取原始JSON文件
with open(original_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化新的items列表
new_items = []

# 遍历JSON中的items
for item in data['items']:
    image_path = item['image']['path']
    if image_path in image_files:
        new_items.append(item)

# 更新JSON数据
data['items'] = new_items

# 保存新的JSON文件
with open(new_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f'新JSON文件已保存到 {new_json_path}')

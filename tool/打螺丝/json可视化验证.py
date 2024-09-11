import os
import json
import cv2
import matplotlib.pyplot as plt

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/pic'
# JSON文件夹路径
json_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/json'
# 可视化输出文件夹路径
visualization_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/json可视化验证'

# 确保可视化输出文件夹存在
os.makedirs(visualization_folder, exist_ok=True)

# 遍历JSON文件夹中的所有JSON文件
for json_file in os.listdir(json_folder):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_folder, json_file)
        
        # 读取JSON文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 获取图片路径
        item = data['items'][0]  # 每个JSON文件只有一个item
        image_path = os.path.join(image_folder, item['image']['path'])
        
        if os.path.exists(image_path):
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                print(f"无法读取图片：{image_path}")
                continue

            # 遍历该图片的标注
            for annotation in item['annotations']:
                if annotation['type'] == 'bbox':
                    x, y, w, h = annotation['bbox']
                    x2, y2 = x + w, y + h

                    # 绘制边框
                    cv2.rectangle(image, (int(x), int(y)), (int(x2), int(y2)), (0, 255, 0), 2)

                elif annotation['type'] == 'points':
                    points = annotation['points']
                    # 假设关键点是成对出现的
                    for i in range(0, len(points), 2):
                        x, y = points[i], points[i+1]
                        cv2.circle(image, (int(x), int(y)), 5, (0, 0, 255), -1)

            # 保存可视化图片
            vis_image_path = os.path.join(visualization_folder, os.path.basename(image_path))
            cv2.imwrite(vis_image_path, image)
            print(f"可视化图片已保存到：{vis_image_path}")
        else:
            print(f"图片文件不存在：{image_path}")

print("验证和可视化过程完成。")

import os
import json

# 路径配置
json_path = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/json/annotations_new.json'
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pic'
output_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/txt'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 读取JSON文件
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 处理每个item
for item in data['items']:
    image_path = item['image']['path']
    annotations = item['annotations']
    
    # 生成对应的txt文件路径
    txt_filename = os.path.splitext(os.path.basename(image_path))[0] + '.txt'
    txt_path = os.path.join(output_folder, txt_filename)
    
    with open(txt_path, 'w') as txt_file:
        for annotation in annotations:
            if not annotation['attributes']['occluded']:
                label_id = annotation['label_id']
                bbox = annotation['bbox']
                
                # 将bbox转为YOLO格式
                x_center = (bbox[0] + bbox[2] / 2) / item['image']['size'][1]
                y_center = (bbox[1] + bbox[3] / 2) / item['image']['size'][0]
                width = bbox[2] / item['image']['size'][1]
                height = bbox[3] / item['image']['size'][0]
                
                # 写入txt文件
                txt_file.write(f"{label_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

print("转换完成")

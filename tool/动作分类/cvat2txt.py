import os
import json

# 路径配置
json_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/json'
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
output_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 类别映射
label_map = {
    0: "未开始",
    1: "放置底板",
    2: "放PCB板1",
    3: "放泡棉",
    4: "放PCB板2",
    5: "完整产品"
}

# 读取JSON文件夹中的所有JSON文件
for json_filename in os.listdir(json_folder):
    if json_filename.endswith('.json'):
        json_path = os.path.join(json_folder, json_filename)

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

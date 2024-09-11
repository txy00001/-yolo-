import os
import json

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/pic'
# JSON文件夹路径
json_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/json'
# YOLO格式输出文件夹路径
output_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/txt'

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)
img_width = 1920
img_height = 1080
# YOLO类ID对应字典
bbox_class = {'2': 0, '3': 1}  # screwdrive类别ID是2，对应YOLO格式的类ID是0；nut类别ID是3，对应YOLO格式的类ID是1
keypoint_class = ['top1', 'top2', 'bottom']  # 假设关键点类别是top1, top2, 和bottom

# 遍历JSON文件夹中的所有JSON文件
for json_file in os.listdir(json_folder):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_folder, json_file)

        # 读取JSON文件
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for each_ann in data['items']:
            yolo_txt_name = each_ann['id']
            yolo_str_list = []
            for annotation in each_ann['annotations']:
                if annotation['type'] == 'bbox':
                    if str(annotation['label_id']) not in bbox_class:
                        continue
                    bbox_class_id = bbox_class[str(annotation['label_id'])]
                    yolo_str = '{} '.format(bbox_class_id)
                    # 左上角和右下角的 XY 像素坐标
                    bbox_top_left_x = int(annotation['bbox'][0])
                    bbox_top_left_y = int(annotation['bbox'][1])
                    bbox_bottom_right_x = int(annotation['bbox'][0] + annotation['bbox'][2])
                    bbox_bottom_right_y = int(annotation['bbox'][1] + annotation['bbox'][3])
                    # 框中心点的 XY 像素坐标
                    bbox_center_x = (bbox_top_left_x + bbox_bottom_right_x) / 2
                    bbox_center_y = (bbox_top_left_y + bbox_bottom_right_y) / 2
                    # 框宽度
                    bbox_width = bbox_bottom_right_x - bbox_top_left_x
                    # 框高度
                    bbox_height = bbox_bottom_right_y - bbox_top_left_y
                    # 框中心点归一化坐标
                    bbox_center_x_norm = bbox_center_x / img_width
                    bbox_center_y_norm = bbox_center_y / img_height
                    # 框归一化宽度
                    bbox_width_norm = bbox_width / img_width
                    # 框归一化高度
                    bbox_height_norm = bbox_height / img_height

                    yolo_str += '{:.5f} {:.5f} {:.5f} {:.5f} '.format(bbox_center_x_norm, bbox_center_y_norm, bbox_width_norm, bbox_height_norm)

                    # 如果是screwdriver类别，处理关键点
                    if bbox_class_id == 0:
                        # 找到该框中所有关键点，存在字典 bbox_keypoints_dict 中
                        bbox_keypoints_dict = {}
                        for point_ann in each_ann['annotations']:
                            if point_ann['type'] == 'points':
                                x = int(point_ann['points'][0])
                                y = int(point_ann['points'][1])
                                
                                if point_ann['label_id'] == 0:
                                    label = 'top'
                                if point_ann['label_id'] == 1:
                                    label = 'bottom'
                                if bbox_class_id == 0 and bbox_top_left_x <= x <= bbox_bottom_right_x and bbox_top_left_y <= y <= bbox_bottom_right_y:
                                    if label == "top":
                                        bbox_keypoints_dict['top1'] = [x, y]
                                        if len(point_ann['points']) == 4:
                                            bbox_keypoints_dict['top2'] = [int(point_ann['points'][2]), int(point_ann['points'][3])]
                                        else:
                                            bbox_keypoints_dict['top2'] = [0, 0]
                                    else:
                                        bbox_keypoints_dict[label] = [x, y]

                        # 把关键点按顺序排好
                        for each_class in keypoint_class:
                            if each_class in bbox_keypoints_dict:
                                x, y = bbox_keypoints_dict[each_class]
                                keypoint_x_norm = x / img_width
                                keypoint_y_norm = y / img_height
                                yolo_str += '{:.5f} {:.5f} {} '.format(keypoint_x_norm, keypoint_y_norm, 2)  # 2-可见不遮挡
                            else:
                                yolo_str += '0 0 0 '
                    yolo_str_list.append(yolo_str.strip())

            if yolo_str_list:
                with open(f'{output_folder}/{yolo_txt_name}.txt', 'w', encoding='utf-8') as f:
                    for yolo_str in yolo_str_list:
                        f.write(yolo_str + '\n')
            else:
                image_path = os.path.join(image_folder, yolo_txt_name + '.png')
                print(f"YOLO数据文件为空，删除文件：{output_folder}/{yolo_txt_name}.txt 和对应的图片文件：{image_path}")
                if os.path.exists(image_path):
                    os.remove(image_path)
                if os.path.exists(f'{output_folder}/{yolo_txt_name}.txt'):
                    os.remove(f'{output_folder}/{yolo_txt_name}.txt')

print("转换完成：YOLO格式的标注文件已保存到", output_folder)

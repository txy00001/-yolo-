import os
import cv2

# 定义关键点类别的顺序
keypoint_class = ['top1', 'top2', 'bottom', 'root', 'head']

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/pic_1'
# TXT文件夹路径
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/txt_1'
# 可视化输出文件夹
output_folder = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝_5点/vis_1'
os.makedirs(output_folder, exist_ok=True)

# 图片尺寸
img_width = 1920
img_height = 1080

# 遍历TXT文件夹中的所有TXT文件
for txt_file in os.listdir(txt_folder):
    if txt_file.endswith('.txt'):
        txt_path = os.path.join(txt_folder, txt_file)
        image_path = os.path.join(image_folder, txt_file.replace('.txt', '.png'))
        output_image_path = os.path.join(output_folder, txt_file.replace('.txt', '_vis.png'))

        # 读取图片
        img = cv2.imread(image_path)

        with open(txt_path, 'r') as f:
            for line in f.readlines():
                elements = line.strip().split(' ')
                class_id = int(elements[0])

                if class_id == 0:  # screwdriver类别
                    bbox_center_x = float(elements[1]) * img_width
                    bbox_center_y = float(elements[2]) * img_height
                    bbox_width = float(elements[3]) * img_width
                    bbox_height = float(elements[4]) * img_height

                    # 画出bbox
                    top_left_x = int(bbox_center_x - bbox_width / 2)
                    top_left_y = int(bbox_center_y - bbox_height / 2)
                    bottom_right_x = int(bbox_center_x + bbox_width / 2)
                    bottom_right_y = int(bbox_center_y + bbox_height / 2)
                    cv2.rectangle(img, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

                    # 画出关键点
                    for i in range(5):
                        keypoint_x = float(elements[5 + i * 3]) * img_width
                        keypoint_y = float(elements[6 + i * 3]) * img_height
                        visibility = int(elements[7 + i * 3])
                        if visibility == 2:  # 可见且未被遮挡
                            cv2.circle(img, (int(keypoint_x), int(keypoint_y)), 5, (0, 0, 255), -1)
                            cv2.putText(img, keypoint_class[i], (int(keypoint_x), int(keypoint_y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        # 保存可视化结果
        cv2.imwrite(output_image_path, img)

print("可视化完成，结果保存到", output_folder)

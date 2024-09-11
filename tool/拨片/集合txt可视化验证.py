import os
import cv2
import matplotlib.pyplot as plt

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/train_new/images'
# 标注文件夹路径
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/train_new/labels'
# 可视化输出文件夹路径
visualization_folder = '/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/train_new_vis'

# 确保可视化输出文件夹存在
os.makedirs(visualization_folder, exist_ok=True)

# 遍历图片文件夹中的所有文件
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # 处理图片文件
        image_path = os.path.join(image_folder, filename)
        txt_path = os.path.join(txt_folder, os.path.splitext(filename)[0] + '.txt')
        
        # 读取图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"无法读取图片：{image_path}")
            continue
        
        image_height, image_width = image.shape[:2]
        
        # 读取对应的txt文件
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                for line in file:
                    label_id, x_center, y_center, width, height = map(float, line.strip().split())
                    
                    # 计算边框的左上角和右下角坐标
                    x1 = int((x_center - width / 2) * image_width)
                    y1 = int((y_center - height / 2) * image_height)
                    x2 = int((x_center + width / 2) * image_width)
                    y2 = int((y_center + height / 2) * image_height)
                    
                    # 绘制边框
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # 在边框上绘制标签
                    cv2.putText(image, str(int(label_id)), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # 保存可视化图片
        vis_image_path = os.path.join(visualization_folder, filename)
        cv2.imwrite(vis_image_path, image)
        print(f"可视化图片已保存到：{vis_image_path}")

print("验证和可视化过程完成。")

import os
import cv2
from ultralytics import YOLO

# 定义输入和输出文件夹
input_folder = "/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/val_1000/images"
output_folder = "/mnt/P40_NFS/20_Research/30_算法项目/拨片检测/7月15日测试集/pred_1000"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 加载自定义模型
model = YOLO("qx_seg_popian_1000/m2/weights/best.pt")

# 获取输入文件夹中的所有图片文件
image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# 处理每张图片
for image_file in image_files:
    # 读取图片
    img_path = os.path.join(input_folder, image_file)
    img = cv2.imread(img_path)
    
    # 预测当前图片
    results = model(img, imgsz=640)
    
    # 绘制预测结果
    for result in results:
        annotated_img = result.plot()  # 渲染结果
    
    # 保存可视化图片到输出文件夹
    output_path = os.path.join(output_folder, image_file)
    cv2.imwrite(output_path, annotated_img)

print("图片处理完成，结果已保存到：", output_folder)

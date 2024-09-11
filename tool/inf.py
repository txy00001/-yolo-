import cv2
from ultralytics import YOLO

# 加载图像
source_image = "1.jpg"
image = cv2.imread(source_image)

# 加载自定义模型
model = YOLO("qx_daluosi_093_5点/s_pose/weights/epoch200.pt")

# 预测图像
results = model(image, imgsz=640)

# 绘制预测结果
for result in results:
    annotated_image = result.plot()  # 渲染结果

# 保存检测后的图像
output_image = "打螺丝_output.jpg"
cv2.imwrite(output_image, annotated_image)

print("图片处理完成，结果已保存到：", output_image)

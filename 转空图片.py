import cv2
import numpy as np

# 创建一个全白的空图片，尺寸为640x480
width, height = 640, 640
empty_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # 全白图像

# 保存空图片
cv2.imwrite("empty_image.jpg", empty_image)

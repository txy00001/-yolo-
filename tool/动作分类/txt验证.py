import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 图片文件夹路径
image_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/pic'
# 标注文件夹路径
txt_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/txt'
# 可视化输出文件夹路径
visualization_folder = '/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/vis'

# 确保可视化输出文件夹存在
os.makedirs(visualization_folder, exist_ok=True)

# 类别映射
label_map = {
    0: "未开始",
    1: "放置底板",
    2: "放PCB板1",
    3: "放泡棉",
    4: "放PCB板2",
    5: "完整产品"
}

# 定义颜色字典
color_map = {
    0: (255, 0, 0),   # Blue
    1: (0, 255, 0),   # Green
    2: (0, 0, 255),   # Red
    3: (255, 255, 0), # Cyan
    4: (255, 0, 255), # Magenta
    5: (0, 255, 255)  # Yellow
}

# 字体路径
font_path = "/usr/share/fonts/truetype/arphic/ukai.ttc"  # 替换为实际系统中的中文字体路径

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
        
        # 将OpenCV图像转换为PIL图像
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        font = ImageFont.truetype(font_path, 24)

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
                    
                    # 获取颜色和标签
                    color = color_map[int(label_id)]
                    label = label_map[int(label_id)]
                    
                    # 绘制边框
                    cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
                    
                    # 绘制标签 (Pillow)
                    draw.text((x1, y1 - 30), label, font=font, fill=color)

        # 将PIL图像转换回OpenCV图像
        image_with_text = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)
        
        # 保存可视化图片
        vis_image_path = os.path.join(visualization_folder, filename)
        cv2.imwrite(vis_image_path, image_with_text)
        print(f"可视化图片已保存到：{vis_image_path}")

print("验证和可视化过程完成。")

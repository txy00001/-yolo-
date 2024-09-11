import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def visualize_and_save_yolo_labels(image_dir, label_dir, save_dir, classes):
    classes = classes.split(',')
    image_paths = os.listdir(image_dir)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for image_path in image_paths:
        image_file = os.path.join(image_dir, image_path)
        label_file = os.path.join(label_dir, image_path.replace('jpg', 'txt').replace('png', 'txt'))

        if not os.path.exists(label_file):
            continue

        image = cv2.imread(image_file)
        h, w, _ = image.shape

        with open(label_file, 'r') as f:
            labels = f.readlines()

        for label in labels:
            label = label.strip().split()
            class_id = int(label[0])
            points = list(map(float, label[1:]))

            points = [(points[i] * w, points[i + 1] * h) for i in range(0, len(points), 2)]
            points = [(int(x), int(y)) for x, y in points]

            # Draw polygon
            cv2.polylines(image, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)
            # Put label text
            cv2.putText(image, classes[class_id], points[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Save the visualized image
        save_path = os.path.join(save_dir, image_path)
        cv2.imwrite(save_path, image)

        # Optionally, display the image
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title(image_path)
        plt.show()


if __name__ == "__main__":
    image_dir = '/mnt/P40_NFS/20_Research/20_私有数据集/60_Count/618-620/img_620'  # 图像文件夹路径
    label_dir = '/mnt/P40_NFS/20_Research/20_私有数据集/60_Count/618-620/txt_620'  # 标签文件夹路径
    save_dir = '/mnt/P40_NFS/20_Research/20_私有数据集/60_Count/618-620/vis'  # 保存可视化图像的文件夹路径
    classes = 'green paper,paper,file,plastic bag,wire,plastic sticks,box'

    visualize_and_save_yolo_labels(image_dir, label_dir, save_dir, classes)
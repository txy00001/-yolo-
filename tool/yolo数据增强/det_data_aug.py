import warnings
warnings.filterwarnings('ignore')
import os, shutil, cv2, tqdm
import numpy as np
import albumentations as A
from PIL import Image
from multiprocessing import Pool
from typing import Callable, List


IMAGE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/pic'
LABEL_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/txt'
AUG_IMAGE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/pic_impove'
AUG_LABEL_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/txt_impove'
SHOW_SAVE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/打螺丝/vis_impove'
CLASSES = ['0', '1','2']

ENHANCEMENT_LOOP = 5  # 增加增强循环次数
ENHANCEMENT_STRATEGY = A.Compose([
    A.Compose([
        A.Affine(scale=[0.8, 1.2], translate_percent=[0.1, 0.3], rotate=[-45, 45], shear=[-10, 10], keep_ratio=True, p=0.5),
        A.BBoxSafeRandomCrop(erosion_rate=0.2, p=0.1),
        A.ElasticTransform(p=0.1),
        A.Flip(p=0.5),
        A.GridDistortion(p=0.1),
        A.Perspective(p=0.1),
    ], p=1.0),
    A.Compose([
        A.GaussNoise(p=0.2),
        A.ISONoise(p=0.2),
        A.ImageCompression(quality_lower=50, quality_upper=100, p=0.2),
        A.RandomBrightnessContrast(p=0.2),
        A.RandomFog(p=0.2),
        A.RandomRain(p=0.2),
        A.RandomSnow(p=0.2),
        A.RandomShadow(p=0.2),
        A.RandomSunFlare(p=0.2),
        A.ToGray(p=0.2),
    ], p=1.0)
], bbox_params=A.BboxParams(format='yolo', min_visibility=0.1, label_fields=['class_labels']))

def parallelise(function: Callable, data: List, chunksize=100, verbose=True, num_workers=os.cpu_count()) -> List:
    num_workers = 1 if num_workers < 1 else num_workers
    pool = Pool(processes=num_workers)
    results = list(tqdm.tqdm(pool.imap(function, data, chunksize), total=len(data), disable=not verbose))
    pool.close()
    pool.join()
    return results

def draw_detections(box, name, img):
    height, width, _ = img.shape
    xmin, ymin, xmax, ymax = list(map(int, list(box)))
    line_thickness = max(1, int(min(height, width) / 200))
    font_scale = min(height, width) / 500
    font_thickness = max(1, int(min(height, width) / 200))
    text_offset_y = int(min(height, width) / 50)
    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 0, 255), line_thickness)
    cv2.putText(img, str(name), (xmin, ymin - text_offset_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), font_thickness, lineType=cv2.LINE_AA)
    return img

def show_labels(images_base_path, labels_base_path):
    if os.path.exists(SHOW_SAVE_PATH):
        shutil.rmtree(SHOW_SAVE_PATH)
    os.makedirs(SHOW_SAVE_PATH, exist_ok=True)
    
    for images_name in tqdm.tqdm(os.listdir(images_base_path)):
        file_heads, _ = os.path.splitext(images_name)
        images_path = f'{images_base_path}/{images_name}'
        labels_path = f'{labels_base_path}/{file_heads}.txt'
        if os.path.exists(labels_path):
            with open(labels_path) as f:
                labels = []
                for line in f.readlines():
                    if line.strip():  # 跳过空行
                        parts = line.strip().split()
                        if len(parts) == 5:  # 确保每行有5个元素
                            labels.append(np.array(parts, dtype=np.float64))
                        else:
                            print(f'Invalid label format in {labels_path}: {line.strip()}')
                labels = np.array(labels, dtype=np.float64)
            images = cv2.imread(images_path)
            height, width, _ = images.shape
            for cls, x_center, y_center, w, h in labels:
                x_center *= width
                y_center *= height
                w *= width
                h *= height
                draw_detections([x_center - w / 2, y_center - h / 2, x_center + w / 2, y_center + h / 2], CLASSES[int(cls)], images)
            cv2.imwrite(f'{SHOW_SAVE_PATH}/{images_name}', images)
            print(f'{SHOW_SAVE_PATH}/{images_name} save success...')
        else:
            print(f'{labels_path} label file not found...')

def data_aug_single(images_name):
    file_heads, postfix = os.path.splitext(images_name)
    images_path = f'{IMAGE_PATH}/{images_name}'
    labels_path = f'{LABEL_PATH}/{file_heads}.txt'
    if os.path.exists(labels_path):
        with open(labels_path) as f:
            labels = []
            for line in f.readlines():
                if line.strip():  # 跳过空行
                    parts = line.strip().split()
                    if len(parts) == 5:  # 确保每行有5个元素
                        labels.append(np.array(parts, dtype=np.float64))
                    else:
                        print(f'Invalid label format in {labels_path}: {line.strip()}')
            labels = np.array(labels, dtype=np.float64)
        images = Image.open(images_path)
        for i in range(ENHANCEMENT_LOOP):
            new_images_name = f'{AUG_IMAGE_PATH}/{file_heads}_{i:0>3}{postfix}'
            new_labels_name = f'{AUG_LABEL_PATH}/{file_heads}_{i:0>3}.txt'
            try:
                transformed = ENHANCEMENT_STRATEGY(image=np.array(images), bboxes=np.minimum(np.maximum(labels[:, 1:], 0), 1), class_labels=labels[:, 0])
            except Exception as e:
                print(f'Error in transformation: {e}')
                continue
            transformed_image = transformed['image']
            transformed_bboxes = transformed['bboxes']
            transformed_class_labels = transformed['class_labels']
            
            cv2.imwrite(new_images_name, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
            with open(new_labels_name, 'w+') as f:
                for bbox, cls in zip(transformed_bboxes, transformed_class_labels):
                    f.write(f'{cls} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n')
            print(f'{new_images_name} and {new_labels_name} save success...')
    else:
        print(f'{labels_path} label file not found...')

def data_aug():
    if os.path.exists(AUG_IMAGE_PATH):
        shutil.rmtree(AUG_IMAGE_PATH)
    if os.path.exists(AUG_LABEL_PATH):
        shutil.rmtree(AUG_LABEL_PATH)
        
    os.makedirs(AUG_IMAGE_PATH, exist_ok=True)
    os.makedirs(AUG_LABEL_PATH, exist_ok=True)

    for images_name in tqdm.tqdm(os.listdir(IMAGE_PATH)):
        data_aug_single(images_name)

if __name__ == '__main__':
    # 先进行数据增强
    data_aug()
    
    # 显示增强后的标签
    show_labels(AUG_IMAGE_PATH, AUG_LABEL_PATH)
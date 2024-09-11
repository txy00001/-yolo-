import warnings
warnings.filterwarnings('ignore')
import os, shutil, cv2, tqdm
import numpy as np
import albumentations as A
from PIL import Image
from multiprocessing import Pool
from typing import Callable, Dict, List, Union

IMAGE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/DF包装/713/pic_all'
LABEL_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/DF包装/713/txt_all'
AUG_IMAGE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/DF包装/713/pic_all_det'
AUG_LABEL_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/DF包装/713/txt_all_det'
SHOW_SAVE_PATH = '/mnt/P40_NFS/20_Research/30_算法项目/DF包装/713/results_det'
CLASSES = ['green paper','paper','file','plastic bag','wire','plastic sticks','box']

ENHANCEMENT_LOOP = 3
ENHANCEMENT_STRATEGY = A.Compose([
    A.Compose([
        A.Affine(scale=[0.5, 1.5], translate_percent=[0.0, 0.3], rotate=[-180, 180], shear=[-45, 45], keep_ratio=True, cval_mask=0, p=0.5),
        A.ElasticTransform(p=0.1),
    ], p=1.0),
    
    A.Compose([
        A.RandomBrightnessContrast(p=0.1),
        A.RandomShadow(p=0.1),
    ], p=1.0)
], bbox_params=A.BboxParams(format='yolo', min_visibility=0.1, label_fields=['class_labels']))

def parallelise(function: Callable, data: List, chunksize=100, verbose=True, num_workers=os.cpu_count()) -> List:
    num_workers = 1 if num_workers < 1 else num_workers
    pool = Pool(processes=num_workers)
    results = list(
        tqdm.tqdm(pool.imap(function, data, chunksize), total=len(data), disable=not verbose)
    )
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
                    parts = list(map(float, line.strip().split()))
                    if len(parts) > 0:  # Ensure there's at least one element
                        labels.append(parts)
                labels = np.array(labels, dtype=np.float64)
            images = cv2.imread(images_path)
            height, width, _ = images.shape
            for cls, *coords in labels:
                coords = np.array(coords).reshape(-1, 2)  # Reshape to pairs of coordinates
                for i in range(0, len(coords), 2):
                    x_center = coords[i][0] * width
                    y_center = coords[i + 1][0] * height
                    w = coords[i + 1][1] * width
                    h = coords[i][1] * height
                    draw_detections([x_center - w // 2, y_center - h // 2, x_center + w // 2, y_center + h // 2], CLASSES[int(cls)], images)
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
                parts = list(map(float, line.strip().split()))
                if len(parts) > 0:  # Ensure there's at least one element
                    cls = int(parts[0])  # First element is the class index
                    coords = parts[1:]  # Remaining elements are coordinates
                    if len(coords) % 2 == 0:  # Ensure coordinates are in pairs
                        labels.append([cls] + coords)  # Append class and coordinates
            labels = np.array(labels, dtype=object)  # Use dtype=object for variable-length arrays
            
        images = Image.open(images_path)
        for i in range(ENHANCEMENT_LOOP):
            new_images_name = f'{AUG_IMAGE_PATH}/{file_heads}_{i:0>3}{postfix}'
            new_labels_name = f'{AUG_LABEL_PATH}/{file_heads}_{i:0>3}.txt'
            try:
                # Prepare bboxes and class_labels for augmentation
                bboxes = []
                class_labels = []
                for label in labels:
                    cls = label[0]
                    coords = label[1:]
                    # Normalize coordinates to [0, 1]
                    bboxes.append(np.clip(np.array(coords), 0, 1))  # Ensure coordinates are within [0, 1]
                    class_labels.append(cls)
                
                transformed = ENHANCEMENT_STRATEGY(image=np.array(images), bboxes=bboxes, class_labels=class_labels)
            except Exception as e:
                print(f"Error during augmentation: {e}")
                continue
            
            transformed_image = transformed['image']
            transformed_bboxes = transformed['bboxes']
            transformed_class_labels = transformed['class_labels']
            
            cv2.imwrite(new_images_name, cv2.cvtColor(transformed_image, cv2.COLOR_RGB2BGR))
            with open(new_labels_name, 'w+') as f:
                for bbox, cls in zip(transformed_bboxes, transformed_class_labels):
                    f.write(f'{cls} {" ".join(map(str, bbox))}\n')
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
    data_aug()
    
    # show_labels(IMAGE_PATH, LABEL_PATH)
    # show_labels(AUG_IMAGE_PATH, AUG_LABEL_PATH)

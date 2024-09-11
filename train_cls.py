from ultralytics import YOLO
import torchvision.transforms as T

# Load a model
model = YOLO("yolov8m-cls.pt") 
# result = model.predict("empty_image.jpg", imgsz=640)  
# print(model.model.transforms)
# model.model.transforms = T.Compose([
#     T.Resize(640, max_size=640, interpolation=T.InterpolationMode.BILINEAR),
#     T.ToTensor(),
#     T.Normalize([0., 0., 0.], [1., 1., 1.]),
# ])

# print(model.model.transforms)

# Train the model
results = model.train(data="/mnt/P40_NFS/20_Research/30_算法项目/新能安_动作分类/640", 
                      epochs=200,imgsz=640,
                      batch=64,workers=2,device=0,
                      project='class_823',
                      name='m')


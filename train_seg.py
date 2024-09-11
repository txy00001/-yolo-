from ultralytics import YOLO

# Load a model
model = YOLO("ultralytics/cfg/models/v8/yolov8s-seg-all.yaml").load("qx_seg_impove/s/weights/best.pt")

# Train the model
results = model.train(data="ultralytics/cfg/datasets/qx_v8_640_320.yaml", 
                      epochs=200,imgsz=640,rect=True,
                      batch=16,workers=2,device=0,
                      project='qx_baozhuang_805',
                      name='s_seg')
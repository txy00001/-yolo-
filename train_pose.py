from ultralytics import YOLO

# Load a model
model = YOLO("ultralytics/cfg/models/v8/yolov8s-pose-big.yaml").load("qx_daluosi_094_5点_new/s_pose/weights/best.pt")

# Train the model
results = model.train(data="ultralytics/cfg/datasets/qx_daluosi_pose.yaml", 
                      epochs=270,imgsz=640,rect=True,
                      batch=64,workers=2,device=0,
                      project='qx_daluosi_095_5点_new',
                      name='s_pose')



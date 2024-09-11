from ultralytics import YOLO
###onnx
# Load a model
# model = YOLO("yolov8n-seg.pt")  # load an official model
#  # load a custom trained model

# # Export the model
# model.export(format="onnx")

####trt
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("qx_seg_popian/m/weights/best.pt")

# Export the model to TensorRT format
model.export(format="engine",
             imgsz=(384,640),
             int8=True,
             batch=8,
             workspace=4,
             data='ultralytics/cfg/datasets/qx_bopian_det.yaml')  # creates 'yolov8n.engine'

# Load the exported TensorRT model
# tensorrt_model = YOLO("qx_seg_impove/s/weights/best.engine")

# # # Run inference
# results = tensorrt_model("wire_test/2024062109_split2-0001.png")

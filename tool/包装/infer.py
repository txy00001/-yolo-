import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

# 加载模型
model = YOLO("qx_seg_int_2/workout_dir/weights/best.pt")  # segmentation model
# model.conf = 0.35  # 设置检测阈值为0.35
names = model.model.names

# 打开视频文件
cap = cv2.VideoCapture("/mnt/P40_NFS/10_Projects/伟创力-珠海/DF包装防错/20240621_09_22_05_403818-0/2024062109.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# 设置视频输出格式和文件
out = cv2.VideoWriter("output/实例分割_1024_0.20.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# 跳转到视频的10分钟位置
cap.set(cv2.CAP_PROP_POS_MSEC, 10 * 60 * 1000)

while True:
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)
    
    # 检查当前时间是否超过13分钟，如果超过则退出循环
    if current_time > 12 * 60 * 1000:
        break

    ret, im0 = cap.read()
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    results = model.predict(im0)
    annotator = Annotator(im0, line_width=2)

    if results[0].masks is not None:
        clss = results[0].boxes.cls.cpu().tolist()
        masks = results[0].masks.xy
        for mask, cls in zip(masks, clss):
            annotator.seg_bbox(mask=mask, mask_color=colors(int(cls), True), det_label=names[int(cls)])

    out.write(im0)
    # cv2.imshow("instance-segmentation", im0)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

out.release()
cap.release()
cv2.destroyAllWindows()

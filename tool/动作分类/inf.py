import cv2
from ultralytics import YOLO

# 定义时间段（以秒为单位）
start_time = 0 * 60  # 10分钟
end_time = 1 * 60  # 13分钟

# 加载视频
source = "动作分类.mp4"
cap = cv2.VideoCapture(source)

# 获取视频的帧率
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 定义要保存的视频文件路径和格式
output_file = "动作分类_output_DET.mp4"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# 跳到起始帧
cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

# 读取并处理视频
model = YOLO("qx_dongzuofenlei/s/weights/best.pt")  # 加载自定义模型

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 获取当前帧的时间戳（以毫秒为单位）
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)

    # 如果当前时间超过结束时间，则停止
    if current_time > end_time * 1000:
        break

    # 预测当前帧
    results = model(frame, imgsz=640,rect=True)
    
    # 绘制预测结果
    for result in results:
        annotated_frame = result.plot()  # 渲染结果
        out.write(annotated_frame)
    
    # 将帧写入输出视频
    out.write(annotated_frame)

# 释放资源
cap.release()
out.release()

print("视频处理完成，结果已保存到：", output_file)

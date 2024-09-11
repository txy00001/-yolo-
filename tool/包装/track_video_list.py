import cv2
import os
from ultralytics import YOLO

# 定义时间段（以秒为单位）
start_time = 0 * 60  # 0分钟
end_time = 1 * 60  # 1分钟

# 视频文件夹路径和生成新的保存视频的文件夹路径
input_folder = "/mnt/P40_NFS/10_Projects/新能安-厦门/20240717"
output_folder = "/mnt/P40_NFS/10_Projects/新能安-厦门/20240717/output_track"

# 检查输出文件夹是否存在，如果不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 加载自定义模型
model = YOLO("qx_seg_popian/m/weights/best.pt")

# 遍历文件夹中的所有视频文件
for video_file in os.listdir(input_folder):
    if video_file.endswith(".mp4"):
        source = os.path.join(input_folder, video_file)
        
        # 加载视频
        cap = cv2.VideoCapture(source)

        # 获取视频的帧率
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # 定义要保存的视频文件路径和格式
        output_file = os.path.join(output_folder, "output_bopian_" + video_file)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # 跳到起始帧
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time * 1000)

        # 读取并处理视频
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 获取当前帧的时间戳（以毫秒为单位）
            current_time = cap.get(cv2.CAP_PROP_POS_MSEC)

            # 如果当前时间超过结束时间，则停止
            if current_time > end_time * 1000:
                break

            # 预测当前帧并进行跟踪
            results = model.track(frame, imgsz=(384,640),persist=True,
                                  tracker='botsort.yaml'
                                  )

            # 绘制预测结果
            for result in results:
                annotated_frame = result.plot()  # 渲染结果
                out.write(annotated_frame)

        # 释放资源
        cap.release()
        out.release()

        print(f"视频 {video_file} 处理完成，结果已保存到：{output_file}")

print("所有视频处理完成。")

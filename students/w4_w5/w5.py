import cv2
import torch
import numpy as np
from absl import app, flags
from absl.flags import FLAGS
from deep_sort_realtime.deepsort_tracker import DeepSort
from models.common import DetectMultiBackend, AutoShape
import os
from shapely.geometry import Polygon

# 定義命令列參數
flags.DEFINE_string('video', './data/test.mp4', '輸入視頻或網路攝影機的路徑 (0)')
flags.DEFINE_string('output', './output/output.mp4', '輸出視頻的路徑')
flags.DEFINE_float('conf', 0.70, '信心閾值')
flags.DEFINE_integer('blur_id', None, '應用高斯模糊的類別 ID')
flags.DEFINE_string('coords_file', 'D:/Users/User/Downloads/project/CULane/output/coords.txt', '輸出坐標的檔案路徑')
flags.DEFINE_string('save_path', 'D:/Users/User/Downloads/project/TUSimple/train_set/clips/test/', '處理後圖片儲存的路徑')
flags.DEFINE_string('paths_file', 'D:/Users/User/Downloads/project/CULane/output/paths.txt', '儲存圖片路徑的檔案路徑')




def read_data_from_file(filename):
    # 讀取文件內容
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # 初始化
    data_matrices = []
    current_matrix = []
    
    # 逐行處理文件內容
    for line in lines:
        line = line.strip()  # 去除行首行尾空白字符
        
        if not line:
            continue
        
        # 判斷是否為數據段開始標識符，這些標識符通常由4個數字組成
        if line.isdigit() and len(line) == 4:  
            if current_matrix:  # 如果有正在處理的矩陣，將其添加到結果中
                data_matrices.append(current_matrix)
                current_matrix = []
            continue
        
        # 處理數據行
        points = line.split()  # 以空白分隔每一對坐標
        matrix_row = []
        for point in points:
            if ',' in point:  # 確保該點包含逗號
                try:
                    x, y = map(int, point.split(','))  # 分割逗號並轉換為整數
                    if (x, y) != (0, 0):
                        matrix_row.append((x, y))
                except ValueError:
                    print(f"Warning: Skipping invalid data point: {point}")
            else:
                print(f"Warning: Data point does not contain a comma: {point}")
        
        if matrix_row:  # 只添加非空行
            current_matrix.append(matrix_row)
    
    # 添加最後一個矩陣
    if current_matrix:
        data_matrices.append(current_matrix)
    
    return data_matrices


def main(_argv):

    last_index=0
    last_last_index=0
    last_flag=0
    val=[]
    last_val=[]
    last_keep_last_track=[]
    keep_last_track=[]
    filename = 'D:/Users/User/Downloads/project/CULane/output/lanes.txt'
    matrices = read_data_from_file(filename)
    lane_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 165, 255)]
    # 初始化視頻捕捉
    video_input = FLAGS.video
    cap = cv2.VideoCapture(int(video_input) if video_input.isdigit() else video_input)
    if not cap.isOpened():
        print('錯誤：無法開啟視頻來源。')
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # 創建視頻寫入對象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(FLAGS.output, fourcc, fps, (frame_width, frame_height))

    # 初始化 DeepSort 追蹤器
    tracker = DeepSort(max_age=50)
    
    # 選擇裝置（CPU 或 GPU）
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("裝置:", device)
    
    # 載入 YOLO 模型
    model = DetectMultiBackend(weights='./weights/yolov9-e.pt', device=device, fuse=True)
    model = AutoShape(model)

    # 載入 COCO 類別標籤
    classes_path = "../configs/coco.names"
    with open(classes_path, "r") as f:
        class_names = f.read().strip().split("\n")

    # 創建隨機顏色列表以表示每個類別
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names), 3))

    # 打開文件以寫入坐標
    with open(FLAGS.coords_file, 'w') as coords_file:
        # 打開文件以寫入圖片路徑
        with open(FLAGS.paths_file, 'w') as paths_file:
            frame_count = 0
            x1_last = -1  # 初始化 x1_last
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # 在每一幀上運行模型
                results = model(frame)
                detect = []
                for det in results.pred[0]:
                    label, confidence, bbox = det[5], det[4], det[:4]
                    x1, y1, x2, y2 = map(float, bbox)  # 將坐標轉換為浮點數
                    x1, y1, x2, y2 = [round(value, 2) for value in [x1, y1, x2, y2]]  # 四捨五入到小數點後兩位
                    class_id = int(label)

                    # 根據信心閾值過濾掉弱檢測，確保它是 '車輛'
                    if class_id in [2] and confidence >= FLAGS.conf:
                        detect.append([[x1, y1, x2 - x1, y2 - y1], confidence, class_id])

                tracks = tracker.update_tracks(detect, frame=frame)
                buffer=[]
                for track in tracks:
                    if not track.is_confirmed():
                        continue
                    
                    track_id = track.track_id
                    ltrb = track.to_ltrb()
                    class_id = track.get_det_class()
                    x1, y1, x2, y2 = map(float, ltrb)
                    x1, y1, x2, y2 = [round(value, 2) for value in [x1, y1, x2, y2]]
                    color = colors[class_id]
                    B, G, R = map(int, color)


                    # 應用高斯模糊
                    if FLAGS.blur_id is not None and class_id == FLAGS.blur_id:
                        if 0 <= x1 < x2 <= frame.shape[1] and 0 <= y1 < y2 <= frame.shape[0]:
                            frame[y1:y2, x1:x2] = cv2.GaussianBlur(frame[y1:y2, x1:x2], (99, 99), 3)

                    # 將坐標寫入文件
                    coords_file.write(f"Frame {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}, Track ID {track_id}, Class ID {class_id}, "
                                      f"Bounding Box: ({x1}, {y1}, {x2}, {y2})\n")







                    line_array=[]
                    temp=[]
                    reverse=[]
                    total_area=[]
                    stablize_index=-1
                    change_steady=-2





                    print("frame",frame_count,track_id)
                    for i in range(len(matrices[frame_count-1])-1):
                        temp=matrices[frame_count-1][i+1]
                        reverse=temp[::-1]
                        temp=[]
                        temp=matrices[frame_count-1][i]+reverse
                        line_array.append(temp)
                        temp=[]
                        reverse=[]

                    

                    
                    point = [(x1, (y1+y2)*0.5), (x2, (y1+y2)*0.5), (x2, y2), (x1, y2)]  # 第二個多邊形

                    # 創建多邊形對象
                    point = Polygon(point)
                    temp=[]

                    for i in range(len(matrices[frame_count-1])-1):
                        temp = Polygon(line_array[i])
                        intersection = temp.intersection(point)# 計算交集
                        intersection_area = intersection.area# 計算交集面積
                        total_area.append(intersection_area)

                    

                    all_of_area=sum(total_area)

                    if all_of_area != 0:
                        for i in range(len(matrices[frame_count-1])-1):
                            if float(total_area[i]/all_of_area) >= 0.79:
                                stablize_index=i
                            if float(total_area[i]/all_of_area) >= 0.2:
                                change_steady+=1
                        

                    if all_of_area==0:
                        print("車輛與車道線沒有共同面積")
                        text = f"error"
                    elif stablize_index != -1 & change_steady <0:
                        text = f"{stablize_index+1}"
                    elif change_steady==0:
                        for last_track in keep_last_track:
                            last_index+=1
                            print(track_id,last_index,last_last_index)
                            if last_track is not None and last_track.to_ltrb() is not NameError and last_track.track_id==track_id:
                                for last_last_track in last_keep_last_track:
                                    last_last_index+=1
                                    if last_last_track.track_id==track_id:
                                        last_flag=1
                                        last_track_id=last_track.track_id
                                        last_ltrb = last_track.to_ltrb()
                                        last_class_id = last_track.get_det_class()
                                        last_x1, last_y1, last_x2, last_y2 = map(float, last_ltrb)  
                                        last_x1, last_y1, last_x2, last_y2 = [round(value, 2) for value in [last_x1, last_y1, last_x2, last_y2]]
                                        break
                
                        if last_flag==1:
                            last_flag=0
                            print(frame_count,track_id,(x1+x2)*0.5,(last_val[last_index-2]),last_index-2,last_last_index)
                            if (x1+x2)*0.5<(last_val[last_last_index-1]):
                           #     text = f"{track_id}-left"
                                text = f"left"
                            elif (x1+x2)*0.5>(last_val[last_last_index-1]):
                               # text = f"{track_id}-right"
                                text = f"right"
                            else:
                                text = f"{track_id}-error-change"
                            last_index=0
                            last_last_index=0
                        else:
                            text = f"{track_id}"
                    else:
                        print(frame_count,total_area,all_of_area)
                        print("交於三個車道線上")
                        text = f"{track_id}-error"
                    






                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (B, G, R), 2)
                    cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 12, int(y1)), (B, G, R), -1)
                    cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
                    
                    x1_x2=(x1+x2)*0.5
                    x1_x2= round(x1_x2, 4)
                    val.append(x1_x2)
                    buffer.append(track)
                    

                last_last_val=last_val    
                print(val)
                last_val=val
                
                last_keep_last_track=keep_last_track
                
                keep_last_track=buffer
  
                val=[]
                


 #               print(frame_count,tracks,keep_last_track,last_keep_last_track)
                for ii, coords in enumerate(matrices[frame_count-1]):
                    for coord_x, coord_y in coords:
                        cv2.circle(frame, (coord_x, coord_y), 5, lane_colors[ii % len(lane_colors)], -1)  # 繪製點
                  

                # 顯示處理後的幀
                cv2.imshow('YOLOv9 物體追蹤', frame)
                writer.write(frame)

                # 儲存處理後的幀
                save_img_path = os.path.join(FLAGS.save_path, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(save_img_path, frame)
                
                # 寫入圖片路徑
                paths_file.write(f"{save_img_path}\n")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # 釋放視頻捕捉和寫入對象
    cap.release()
    writer.release()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    import cv2
import torch
import numpy as np
from absl import app, flags
from absl.flags import FLAGS
from deep_sort_realtime.deepsort_tracker import DeepSort
from models.common import DetectMultiBackend, AutoShape
import os

# 定義命令列參數
flags.DEFINE_string('video', './data/test.mp4', '輸入視頻或網路攝影機的路徑 (0)')
flags.DEFINE_string('output', './output/output.mp4', '輸出視頻的路徑')
flags.DEFINE_float('conf', 0.50, '信心閾值')
flags.DEFINE_integer('blur_id', None, '應用高斯模糊的類別 ID')
flags.DEFINE_string('coords_file', 'D:/Users/User/Downloads/project/CULane/output/coords.txt', '輸出坐標的檔案路徑')
flags.DEFINE_string('save_path', 'D:/Users/User/Downloads/project/TUSimple/train_set/clips/test/', '處理後圖片儲存的路徑')
flags.DEFINE_string('paths_file', 'D:/Users/User/Downloads/project/CULane/output/paths.txt', '儲存圖片路徑的檔案路徑')




def read_data_from_file(filename):
    # 讀取文件內容
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # 初始化
    data_matrices = []
    current_matrix = []
    
    # 逐行處理文件內容
    for line in lines:
        line = line.strip()  # 去除行首行尾空白字符
        
        if not line:
            continue
        
        # 判斷是否為數據段開始標識符，這些標識符通常由4個數字組成
        if line.isdigit() and len(line) == 4:  
            if current_matrix:  # 如果有正在處理的矩陣，將其添加到結果中
                data_matrices.append(current_matrix)
                current_matrix = []
            continue
        
        # 處理數據行
        points = line.split()  # 以空白分隔每一對坐標
        matrix_row = []
        for point in points:
            if ',' in point:  # 確保該點包含逗號
                try:
                    x, y = map(int, point.split(','))  # 分割逗號並轉換為整數
                    matrix_row.append((x, y))
                except ValueError:
                    print(f"Warning: Skipping invalid data point: {point}")
            else:
                print(f"Warning: Data point does not contain a comma: {point}")
        
        if matrix_row:  # 只添加非空行
            current_matrix.append(matrix_row)
    
    # 添加最後一個矩陣
    if current_matrix:
        data_matrices.append(current_matrix)
    
    return data_matrices


def main(_argv):
    last_index=0
    last_last_index=0
    val=[]
    last_val=[]
    last_last_val=[]
    last_flag=0
    last_keep_last_track=[]
    keep_last_track=[]
    filename = 'D:/Users/User/Downloads/project/CULane/output/lanes.txt'
    matrices = read_data_from_file(filename)
    lane_colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 165, 255)]
    # 初始化視頻捕捉
    video_input = FLAGS.video
    cap = cv2.VideoCapture(int(video_input) if video_input.isdigit() else video_input)
    if not cap.isOpened():
        print('錯誤：無法開啟視頻來源。')
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    # 創建視頻寫入對象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(FLAGS.output, fourcc, fps, (frame_width, frame_height))

    # 初始化 DeepSort 追蹤器
    tracker = DeepSort(max_age=50)
    
    # 選擇裝置（CPU 或 GPU）
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("裝置:", device)
    
    # 載入 YOLO 模型
    model = DetectMultiBackend(weights='./weights/yolov9-e.pt', device=device, fuse=True)
    model = AutoShape(model)

    # 載入 COCO 類別標籤
    classes_path = "../configs/coco.names"
    with open(classes_path, "r") as f:
        class_names = f.read().strip().split("\n")

    # 創建隨機顏色列表以表示每個類別
    np.random.seed(42)
    colors = np.random.randint(0, 255, size=(len(class_names), 3))

    # 打開文件以寫入坐標
    with open(FLAGS.coords_file, 'w') as coords_file:
        # 打開文件以寫入圖片路徑
        with open(FLAGS.paths_file, 'w') as paths_file:
            frame_count = 0
            x1_last = -1  # 初始化 x1_last
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # 在每一幀上運行模型
                results = model(frame)
                detect = []
                for det in results.pred[0]:
                    label, confidence, bbox = det[5], det[4], det[:4]
                    x1, y1, x2, y2 = map(float, bbox)  # 將坐標轉換為浮點數
                    x1, y1, x2, y2 = [round(value, 2) for value in [x1, y1, x2, y2]]  # 四捨五入到小數點後兩位
                    class_id = int(label)

                    # 根據信心閾值過濾掉弱檢測，確保它是 '車輛'
                    if class_id in [2] and confidence >= FLAGS.conf:
                        detect.append([[x1, y1, x2 - x1, y2 - y1], confidence, class_id])

                tracks = tracker.update_tracks(detect, frame=frame)
                buffer=[]
                for track in tracks:
                    if not track.is_confirmed():
                        continue
                    
                    track_id = track.track_id
                    ltrb = track.to_ltrb()
                    class_id = track.get_det_class()
                    x1, y1, x2, y2 = map(float, ltrb)
                    x1, y1, x2, y2 = [round(value, 2) for value in [x1, y1, x2, y2]]
                    color = colors[class_id]
                    B, G, R = map(int, color)
  #                  text = f"{track_id}-{class_names[class_id]}"

                    # 繪製邊界框
   #                 cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (B, G, R), 2)
   #                 cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 12, int(y1)), (B, G, R), -1)
   #                 cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)

                    # 應用高斯模糊
                    if FLAGS.blur_id is not None and class_id == FLAGS.blur_id:
                        if 0 <= x1 < x2 <= frame.shape[1] and 0 <= y1 < y2 <= frame.shape[0]:
                            frame[y1:y2, x1:x2] = cv2.GaussianBlur(frame[y1:y2, x1:x2], (99, 99), 3)

                    # 將坐標寫入文件
                    coords_file.write(f"Frame {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}, Track ID {track_id}, Class ID {class_id}, "
                                      f"Bounding Box: ({x1}, {y1}, {x2}, {y2})\n")








                    targets = []
                    target_index = []
                    car_state = []
                    car_left = []
                    car_right = []

                    for index, sublist in enumerate(matrices[frame_count-1]):
                        min_diff = float('inf')
                        closest_point = None
                        closest_index = None
    
                        # 遍歷當前層的所有點
                        for i, point in enumerate(sublist):
                            x, y = point
                            diff = abs(y - y2)  # 計算Y座標的差值
                            if diff < min_diff:       # 如果差值小於當前最小差值
                                min_diff = diff       # 更新最小差值
                                closest_point = point # 更新最接近的點
                                closest_index = i     # 更新最接近的點的索引
    
                        # 儲存每一層的結果
                        targets.append(closest_point)
                        target_index.append(closest_index)

                        if (x1 + ((x2 - x1) * 0.2)) < closest_point[0]:
                            car_left.append(0)
                        elif (x1 + ((x2 - x1) * 0.2)) > closest_point[0]:
                            car_left.append(1)
                        else:
                            if (((x1 + x2)*0.5)) < closest_point[0]:
                                car_left.append(0)
                            else:
                                car_left.append(1)
  #                              print("have 2", frame_count, track_id, "car_left", car_left,x1,x2,closest_point[0])

                        if (x2 - ((x2 - x1) * 0.3)) < closest_point[0]:
                            car_right.append(0)
                        elif (x2 - ((x2 - x1) * 0.3)) > closest_point[0]:
                            car_right.append(1)
                        else:
                            if (((x1 + x2)*0.5)) <= closest_point[0]:
                                car_right.append(0)
                            else:
                                car_right.append(1)
      #                          print("have 2", frame_count, track_id, "car_right", car_right)
                    
                    step_num1 = next((i for i, x in enumerate(car_right) if x != 1), 4)
                    step_num = next((i for i, x in enumerate(car_left) if x != 1), 4)

 #                   print(frame_count,track_id,car_left,car_right,step_num,step_num1)

                    if step_num1 is not None and step_num is not None:
                        if car_left == car_right:
                            if all(x == 1 for x in car_left) or all(x == 0 for x in car_left):
                                text = f"outside"
                            else:
                                text = f"{step_num}"
      #                      cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 9, int(y1)), (B, G, R), -1)
     #                       cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
                        elif step_num1 > step_num:
                            



                            for last_track in keep_last_track:
                                last_index+=1
     #                           print("frame",frame_count,last_track.track_id,last_track)
                                if last_track is not None and last_track.to_ltrb() is not NameError and last_track.track_id==track_id:
      #                              print("ck",frame_count,last_track.track_id,last_track)
                                    for last_last_track in last_keep_last_track:
                                        last_last_index+=1
                                        if last_last_track.track_id==track_id:
                                            last_flag=1
                                            last_track_id=last_track.track_id
                                            last_ltrb = last_track.to_ltrb()
                                            last_class_id = last_track.get_det_class()
                                            last_x1, last_y1, last_x2, last_y2 = map(float, last_ltrb)  
                                            last_x1, last_y1, last_x2, last_y2 = [round(value, 2) for value in [last_x1, last_y1, last_x2, last_y2]]
       #                                     print("frame",frame_count,last_track_id,x1,x2,x1+x2,last_val[last_index-1],last_last_val[last_last_index-1])
                                     
                                            
                                            break                       
  #                          if last_flag==1:
   #                             print("judge",frame_count,track_id,x1,last_x1)
    #                        elif last_flag==0:
     #                           print("judge",frame_count,track_id,step_num,step_num1,x1,x2,0.5*(x1+x2))



           #                 print("frame_count",frame_count,"track_id",track_id,"car_left",car_left,"car_right",car_right,"step_num",step_num,"step_num1",step_num1,"x1",(x1 + int((x2 - x1) * 0.1)))
                            if step_num1==4 and targets[step_num-1][0]==4:
      #                          print("frame_count",frame_count,"track_id",track_id,"car_left",car_left,"car_right",car_right,"step_num",step_num,"step_num1",step_num1,targets[step_num-1][0],targets[step_num1-1][0],int((x2+x1)*0.5))
                                text = f"outside+++"
                            else:
                                if last_flag==1:
                                    last_flag=0
                                    print(frame_count,track_id,"last_val",last_val[last_index-2],"index",last_index,(x1+x2)*0.5,(last_val[last_index-2]) < (x1+x2)*0.5,(last_val[last_index-2]) > (x1+x2)*0.5)
                                    print(track_id,last_val[last_index-2],(x1+x2)*0.5,last_val)
                                    if (last_val[last_index-2]) < (x1+x2)*0.5:
                                        text = f"right"
                                    elif (last_val[last_index-2])>(x1+x2)*0.5:
          #                              print("frame_count",frame_count,"track_id",track_id,"car_left",car_left,"car_right",car_right,"step_num",step_num,"step_num1",step_num1,targets[step_num-1][0],targets[step_num1-1][0],int((x2+x1)*0.5))
                                        text = f"left"
                                    else:
                                        print(frame_count,track_id,"不是左轉跟右轉")
                                        text = f"error-11"
                                else:
                                    text = f"{track_id}-{class_names[class_id]}"
                                last_index=0
                                last_last_index=0
     #                       cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 9, int(y1)), (B, G, R), -1)
    #                        cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
                        else:
                            text = f"error"
     #                       cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 9, int(y1)), (B, G, R), -1)
    #                        cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
                    else:
                        print("frame_count",frame_count,"track_id",track_id,"car_left",car_left,"car_right",car_right,"step_num",step_num,"step_num1",step_num1)


                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (B, G, R), 2)
                    cv2.rectangle(frame, (int(x1) - 1, int(y1) - 20), (int(x1) + len(text) * 12, int(y1)), (B, G, R), -1)
                    cv2.putText(frame, text, (int(x1) + 5, int(y1) - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 2)
                    
                    x1_x2=(x1+x2)*0.5
                    x1_x2= round(x1_x2, 4)
                    val.append(x1_x2)
                    buffer.append(track)
 #               if frame_count>9:
  #                  print("frame_count",frame_count,"track_id",track_id,0.5*(x1+x2),last_val,last_last_val)
                last_last_val=last_val    

                last_val=val

                last_keep_last_track=keep_last_track
                
                keep_last_track=buffer
                val=[]
                


 #               print(frame_count,tracks,keep_last_track,last_keep_last_track)
                for ii, coords in enumerate(matrices[frame_count-1]):
                    for coord_x, coord_y in coords:
                        cv2.circle(frame, (coord_x, coord_y), 5, lane_colors[ii % len(lane_colors)], -1)  # 繪製點
                  

                # 顯示處理後的幀
                cv2.imshow('YOLOv9 物體追蹤', frame)
                writer.write(frame)

                # 儲存處理後的幀
                save_img_path = os.path.join(FLAGS.save_path, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(save_img_path, frame)
                
                # 寫入圖片路徑
                paths_file.write(f"{save_img_path}\n")

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # 釋放視頻捕捉和寫入對象
    cap.release()
    writer.release()


if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
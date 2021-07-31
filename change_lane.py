import pandas as pd
import os
import cv2
import timeit
# 把 视频， output.csv 和 lane.csv 以及 stop_detection_area.csv 放在 video(i)/路径内即可


def distance(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5


def video_to_frames():
    # convert the input video to images, store in video1//frames
    cap = cv2.VideoCapture('video1/change_lane_1.mp4')

    final_directory = os.path.join(os.getcwd(), r'video1/frames')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite('video1/frames/' + str(i) + '.jpg', frame)
        i += 1

    cap.release()
    cv2.destroyAllWindows()


def read_lane_equation():
    # read lane equation from video1/lane.csv (get from makesense.ai)
    file_in = open('video1/lane.csv', 'r')
    lines = file_in.readlines()

    lanes = []
    for line in lines:
        line = line.split(',')
        x1, y1, x2, y2 = int(line[1]), int(line[2]), int(line[3]), int(line[4])

        k = (y2 - y1) / (x2 - x1)
        b = y1 - k * x1

        lanes.append((k, b))

    return lanes


def read_stop_detection_area():
    # read stop detection area from video1/stop_detection_area.csv (get from makesense.ai)
    # return x1, y1 of upper left point, x2, y2 of bottom right point

    try:
        file_in = open('video1/stop_detection_area.csv', 'r')
        lines = file_in.readlines()
        file_in.close()
    except FileNotFoundError:
        return []
    boxes = []
    for line in lines:
        line = line.split(',')
        x1, y1, w, h = int(line[1]), int(line[2]), int(line[3]), int(line[4])

        boxes.append((x1, y1, x1+w, y1+h))

    return boxes


def read_vehicles():
    # read vehicle traces from video1/stop_detection_area.csv (get from makesense.ai)
    dataframe = pd.read_csv('video1/output.csv')
    vehicle_trace = {i: [] for i in range(1000)}
    vehicle_frame = {i: [] for i in range(1000)}
    for i in range(dataframe.shape[0]):
        vehicle_id = dataframe['id'][i]
        frame_id = dataframe['frame_id'][i]
        center_x, center_y = dataframe['x1'][i] + dataframe['w'][i] / 2, dataframe['y1'][i] + dataframe['h'][i] / 2
        vehicle_trace[vehicle_id].append((center_x, center_y))
        vehicle_frame[vehicle_id].append(frame_id)

    # vehicle_trace: key: vehicle id, value: [bounding box centers]
    # vehicle_frame: key: vehicle id, value: [frame_ids]
    return vehicle_trace, vehicle_frame


def detect_passing_lane(lane_equation, trace):
    # input: one lane equation and one vehicle trace
    # output: -1 if the vehicle doesn't pass the lane
    #         frame_index if the vehicle passes the lane
    
    prev_sign = 0

    index = 0
    for point in trace:
        sign = point[1] - lane_equation[0] * point[0] - lane_equation[1]
        if prev_sign * sign < 0 or abs(sign) < 1:
            return index
        else:
            prev_sign = sign
        index += 1
    return -1


def detect_stop(stop_areas, trace):
    # input: stop areas and one vehicle trace
    # output: -1 if the vehicle doesn't stop in any of the stop areas
    #        1 if the vehicle doesn't stop in any of the stop areas
    
    if not trace or not stop_areas:
        return -1
    sum_distance = 0

    count = 0
    for i in range(1, len(trace)):
        if distance(trace[i-1], trace[i]) < 5:
            count += 1
        sum_distance += distance(trace[i-1], trace[i])

    if sum_distance < 50 or distance(trace[0], trace[-1]) < 10 or count > 100:
        for stop_area in stop_areas:
            if stop_area[2] >= trace[0][0] >= stop_area[0] and stop_area[3] >= trace[0][1] >= stop_area[1]:
                return 1
    return -1


def find_changing_lane_vehicles(lanes, vehicle_trace):
    # input: lanes and vehicle traces
    # output: passing_lane_vehicle_info: [(vehicle_id, passing_lane_frame_id)]
    
    passing_lane_vehicle_info = []
    for vehicle_id, moving_trace in vehicle_trace.items():
        for lane in lanes:
            pass_lane_info = detect_passing_lane(lane, moving_trace)
            if pass_lane_info != -1:
                passing_lane_vehicle_info.append((vehicle_id, pass_lane_info))
                break
    return passing_lane_vehicle_info


def find_stop_vehicles(stop_areas, vehicle_trace):
    # input: stop_areas and vehicle traces
    # output: stop_vehicle_info: [(vehicle_id)]
    
    stop_vehicle_info = []
    for vehicle_id, moving_trace in vehicle_trace.items():

        if moving_trace:
            pass_lane_info = detect_stop(stop_areas, moving_trace)
            if pass_lane_info != -1:
                stop_vehicle_info.append(vehicle_id)
    return stop_vehicle_info


def mark(vehicle_trace, vehicle_frame, passing_lane_vehicle_info, stop_vehicles):
    # Mark the vehicles which pass the lanes or stop in the stop detection areas
    final_directory = os.path.join(os.getcwd(), r'video1/marked_frames')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    radius = 20
    thickness = 5
    
    max_frame = 0

    pass_lane_frames = {i: [] for i in range(5000)}
    stop_frames = {i: [] for i in range(5000)}

    for vehicle_info in passing_lane_vehicle_info:
        vehicle_id, pass_lane_frame = vehicle_info

        trace = vehicle_trace[vehicle_id]
        frames = vehicle_frame[vehicle_id]
        for i in range(len(frames)):
            frame = frames[i]
            if frame >= pass_lane_frame:
                point = trace[i]
                pass_lane_frames[frame].append(point)

                if frame > max_frame:
                    max_frame = frame

    for stop_vehicle_id in stop_vehicles:

        trace = vehicle_trace[stop_vehicle_id]
        frames = vehicle_frame[stop_vehicle_id]
        for i in range(len(frames)):
            frame = frames[i]
            point = trace[i]
            stop_frames[frame].append(point)
            if frame > max_frame:
                max_frame = frame

    for frame in range(max_frame + 1):

        if frame in pass_lane_frames or frame in stop_frames:

            image_path = 'video1/frames/' + str(frame) + '.jpg'
            image = cv2.imread(image_path)
            if image is not None:

                if frame in pass_lane_frames:
                    points = pass_lane_frames[frame]

                    for point in points:
                        circle_center = (int(point[0]), int(point[1]))
                        image = cv2.circle(image, circle_center, radius, (255, 0, 0), thickness)

                if frame in stop_frames:
                    points = stop_frames[frame]
                    for point in points:
                        circle_center = (int(point[0]), int(point[1]))
                        image = cv2.circle(image, circle_center, radius, (0, 255, 0), thickness)
                cv2.imwrite('video1/marked_frames/' + str(frame) + '.jpg', image)
    
    return max_frame


def merge_images_to_video(max_frame):
    img_array = []
    filename = 'video1/marked_frames/' + str(0) + '.jpg'
    img = cv2.imread(filename)

    height, width, layers = img.shape
    size = (width, height)

    for i in range(max_frame+1):
        try:
            img = cv2.imread('video1/marked_frames/' + str(i) + '.jpg')
            img_array.append(img)
            i += 1
        except:
            pass

    out = cv2.VideoWriter('video1/result.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def main():
    # video_to_frames()

    # return

    start = timeit.default_timer()
    lane_equations = read_lane_equation()
    stop_areas = read_stop_detection_area()
    vehicle_traces, vehicle_frames = read_vehicles()
    passing_lane_vehicles = find_changing_lane_vehicles(lane_equations, vehicle_traces)
    stop_vehicles = find_stop_vehicles(stop_areas, vehicle_traces)

    print("Vehicle IDs that stop in the stop detection area", stop_vehicles)
    print("Vehicle IDs and the frame ids they pass the lane", passing_lane_vehicles)
    stop = timeit.default_timer()

    print('Time: ', stop - start)
    return
    # 可以不跑后面的，后面两个函数是用来输出标注的图像和视频的
    max_frame = mark(vehicle_traces, vehicle_frames, passing_lane_vehicles, stop_vehicles)
    print('mark_finish')
    merge_images_to_video(max_frame)


main()
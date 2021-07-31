# Change-Lane-Detection

Pre-process:
  Configuration File Required for lane and stop-detection-area marking.
  Mark on first frame of video by the tool "object detection" on makesense.ai. 
  Mark two types of label "stop_detection_area" and "Lane", export two kinds of label as stop_detection_area.csv and lane.csv, put them under path video(i)/
  
Then run change_lane.py, the vehicle id of those pass the lanes or stop in the detection area will be printed out.
No need to run function mark() and merge_images_to_video() in change_lane.py if video output is not requireed

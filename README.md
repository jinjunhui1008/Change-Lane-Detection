# Change-Lane-Detection

Pre-process:
  Configuration File Required for lane and stop-detection-area marking.
  Mark on first frame of video by the tool "object detection" on makesense.ai. 
  ![mark_stop](https://user-images.githubusercontent.com/71064257/127727214-a5302de2-f3ea-4252-b4bf-353d2deb3927.png)
  ![mark_lane](https://user-images.githubusercontent.com/71064257/127727227-845daadd-cf19-44c1-86a2-eb79b6a3cd9a.png)
  Mark two types of label "stop_detection_area" and "Lane", export two kinds of label as stop_detection_area.csv and lane.csv, put them under path video(i)/
  ![output](https://user-images.githubusercontent.com/71064257/127727237-22a836d0-bf2f-4f39-a794-b81484cc4283.png)

Then run change_lane.py, the vehicle id of those pass the lanes or stop in the detection area will be printed out.
  ![1627701871(1)](https://user-images.githubusercontent.com/71064257/127727284-fdb5ca9b-3eb4-45fd-8424-9291043318ac.png)

No need to run function mark() and merge_images_to_video() in change_lane.py if video output is not required

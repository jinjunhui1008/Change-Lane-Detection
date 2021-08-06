# Change-Lane-Detection

Pre-process:
  Configuration files required for lane and stop-detection-area marking.
  Mark on first frame of video by the tool "object detection" on makesense.ai. 
  
  Click "Get Started", upload first image and click "Object Detection"
  ![cc5edc6ca2d08fef6e08ea59d2d89cf](https://user-images.githubusercontent.com/71064257/128514912-5fb65127-e914-444d-80da-fdc35abc3cdd.png)
  ![812f9fccd41129a95800e98db22531e](https://user-images.githubusercontent.com/71064257/128514924-4b76cd5e-e5f4-456d-a999-b7edaf314024.png)

  Initialize the Label: "Stop_detection_area" and "Lane" by clicking the '+' button.
  ![b142d1b0b333b5b23457096a17cd064](https://user-images.githubusercontent.com/71064257/128515021-27d64d6d-a982-49f9-89d9-17a2baeb7cb3.png)
  
  Select type "Rect"
  ![0d784a76d1d9f511da26306d3cd238c](https://user-images.githubusercontent.com/71064257/128515038-626d8fec-8480-46c2-8069-6823e7850785.png)
  Draw the region on figure and select their labels as "Stop_detection_area"
  ![939712d334f25da2245fe3f1b4a8e5a](https://user-images.githubusercontent.com/71064257/128515134-04da6014-c4d6-4d29-a580-1e9b3bc2b9bc.png)

  Click Button "Actions" -> Export Annotations -> Export Rect Labels
  ![10dd720cacc2d72c132ef1344ad48e2](https://user-images.githubusercontent.com/71064257/128515200-5301c734-4929-48f0-b1a9-af26896365bf.png)

  Similiarly, you may get the Annotations for Lane:
  ![0183dc81411297354b9157cc021bfc0](https://user-images.githubusercontent.com/71064257/128515340-49fc4372-3c6b-4681-b965-7ec8a206f319.png)

  Then you get two types of label "Stop_detection_area" and "Lane", export two kinds of label as stop_detection_area.csv and lane.csv, put them under path video(i)/
  ![output](https://user-images.githubusercontent.com/71064257/127727237-22a836d0-bf2f-4f39-a794-b81484cc4283.png)

Then run change_lane.py, the vehicle id of those pass the lanes or stop in the detection area will be printed out.
  ![1627701871(1)](https://user-images.githubusercontent.com/71064257/127727284-fdb5ca9b-3eb4-45fd-8424-9291043318ac.png)

No need to run function mark() and merge_images_to_video() in change_lane.py if video output is not required

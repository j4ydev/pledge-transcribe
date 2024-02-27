import glob
import os
import random
import time

import cv2
import pandas as pd
from deepface import DeepFace
from icecream import ic

from config import (FACE_CAPTURE_CSV_PATH, FACE_IMAGE_DIRECTORY,
                    FACE_IMAGE_FILE_FORMAT, FAILED_FACE_CAPTURE_CSV_PATH,
                    FLATTEN_VIDEO_DIRECTORY, INPUT_VIDEO_FILE_FORMAT)

happy_case = "6340308344112_pauravi_rahane.mp4"
person_with_mask = "6339319955112_jasna_vk.mp4"
incompatible = "6339427012112_tanmay_mhaske.mp4" # many frames, blur/shiny
very_dark_person = "6339526034112_ayan_dirghangi.mp4"
very_bright_backlight = "6339832782112_priya_arak.mp4"
almost_no_light = "6340043673112_pankaj_shinde.mp4"
multiple_person_1 = "6340074881112_swati_anarthe.mp4"
multiple_person_2 = "6340351092112_alka_gobare.mp4"
multiple_person_3 = "6341658088112_prashant_palghdmal.mp4" # detectable 2 person
entire_face_covered = "6340128612112_maseera_momin.mp4"
no_person = "6340265046112_akash_giri.mp4"
shiny_spectacles = "6340742314112_shreya_thota.mp4"
VIDEO_FILE_PATH = f"{FLATTEN_VIDEO_DIRECTORY}/{multiple_person_3}"

debug_demo = True

class SAVE_FRAME_WITH_FACE():
    def __init__(self):
      self.counter = 0

    def check_frames_has_same_faces(self, frame1, frame2):
        cv2.imwrite(f"frame_1.png", frame1)
        cv2.imwrite(f"frame_2.png", frame2)
        frames_has_same_faces = False
        try:
            result = DeepFace.verify("frame_1.png" , "frame_2.png")
            frames_has_same_faces = result["verified"]
        except Exception as e:
            print("exception in check_frames_has_same_faces", e)
            frames_has_same_faces = False
        return frames_has_same_faces

    def get_count_of_faces_in_frame(self, frame):
      count = 0
      try:
        face_objs = DeepFace.extract_faces(frame)
        return len(face_objs)
      except Exception as e:
          count = 0
      return count

    def get_frames_with_same_person(self, path):
      video = cv2.VideoCapture(path, cv2.CAP_FFMPEG)
      total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
      initial_frame_position= 0 # int(total_frames/4) # start at 25%

      skip_frame_count = 20
      frame_1 = []
      frame_2 = []

      video.set(cv2.CAP_PROP_POS_FRAMES, initial_frame_position)
      frame_index = initial_frame_position - 1
      while True:
        frame_index = frame_index+1
        ret, frame = video.read()
        if not ret:
            break

        if debug_demo:
          cv2.imwrite(f"frame_2.png", frame)

        rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_count = saveFrameWithFace_obj.get_count_of_faces_in_frame(rgbFrame)
        found = False
        if face_count == 1:
          if len(frame_2) == 0:
            frame_2 = frame
            frame_index = frame_index + skip_frame_count
            video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
          else:
            check_frames_has_same_faces = self.check_frames_has_same_faces(frame, frame_2)
            if check_frames_has_same_faces:
              frame_1 = frame
              found = True
              break
            else:
              print("ni match kiya: ", frame_index)
              frame_2 = frame
              frame_index = frame_index + skip_frame_count
              video.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        else:
          if face_count > 1:
            print(" ---- case with multiple persons ------ ", face_count)

      if not found:
        video.set(cv2.CAP_PROP_POS_FRAMES, int(total_frames/2))
        ret, frame = video.read()
        cv2.imwrite(f"frame_2.png", frame)

      video.release()
      print("frame_index: ", frame_index, "total_frames:", total_frames)
      return frame_1, frame_2, frame_index

    def process(self):
      frame_1, frame_2, i = self.get_frames_with_same_person(VIDEO_FILE_PATH)
      if len(frame_1) > 0:
        print("mil gai: ", i)

if __name__ == "__main__":
    saveFrameWithFace_obj = SAVE_FRAME_WITH_FACE()
    print(VIDEO_FILE_PATH)
    start_time = time.time()
    saveFrameWithFace_obj.process()
    end_time = time.time()
    time_consumed_by_face_capture = end_time - start_time
    print("time_consumed_by_face_capture: ", time_consumed_by_face_capture)



# loop the video to
#   get frame_1 and frame_2 (irrespective of logic) that contains face
#   compare the 2 frames with faces to see if the face is of same person
#     if not then - get other frames to process
#     if yes save frame 1






  # from accepted videos
  # 2 person in 1
  #   photo 6346221230112_kamesh_tamboli__brute
  # dark photo
  #   6346221095112_ajay_thakare_brute
  #   6337189580112_vandana_sharma_brute
  # with mask
  #   6346222433112_punam_kumari__brute
  #   6346214365112_manisha_z_brute
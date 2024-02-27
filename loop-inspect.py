import glob
import os
import shutil

import cv2
import pandas as pd
from deepface import DeepFace

from config import (CAPTURE_FACE_BRUT_FORCE_CSV_PATH,
                    CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH,
                    CAPTURE_FACES_BRUT_FORCE_DIRECTORY,
                    CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY,
                    FACE_IMAGE_FILE_FORMAT, FLATTEN_VIDEO_CSV_FILE_PATH,
                    INSPECT_DATAFRAME_PATH, VIDEO_FILE_FORMAT)
from utils import is_value_present_in_dataframe

STATS_CSV = "stats.csv"
STATS_CSV_COLUMNS = ['video_id', '']

class LOOP_INSPECT():
    def __init__(self):
        print(INSPECT_DATAFRAME_PATH)
        print("--------------------------------")
        self.inspect_dataframe = pd.read_csv(INSPECT_DATAFRAME_PATH)
        print(self.inspect_dataframe.head())

        self.flatten_video_dataframe = pd.read_csv(FLATTEN_VIDEO_CSV_FILE_PATH)

        if os.path.isfile(STATS_CSV):
          try:
              self.stats_dataframe = pd.read_csv(STATS_CSV)
          except Exception as e:
              print(f"{STATS_CSV}: error in reading .")
              print(e)
              self.stats_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])
        else:
            self.stats_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])

    def get_video_file_path(self, video_id):
      flatten_video_row = self.flatten_video_dataframe.loc[self.flatten_video_dataframe['video_id'] == video_id, 'input_video_file_path']
      if len(flatten_video_row) == 0:
        print("video missing: ", video_id)
        return False
      video_file_path = flatten_video_row.iloc[0]
      if not video_file_path:
        print("video missing: ", video_id)
        return False
      return True, video_file_path

    def process(self):
      for index, row in self.inspect_dataframe.iterrows():
        video_id = row['vid']
        status, video_file_path = self.get_video_file_path(video_id)

        # if row["InvigilationState"]=="Accept":
        #   print()
        # else:
        #   print()

if __name__ == "__main__":
    loop_inspect = LOOP_INSPECT()
    loop_inspect.process()
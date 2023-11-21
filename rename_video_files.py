import glob
import os
import re
import shutil

import pandas as pd

from config import *


class RENAME_VIDEO_FILES():
    def __init__(self):
        if os.path.isfile(RENAME_FILES_DATAFRAME_PATH):
            try:
                self.video_rename_dataframe = pd.read_csv(RENAME_FILES_DATAFRAME_PATH)
            except:
                self.video_rename_dataframe = pd.DataFrame(columns=['original_video_path', 'new_video_path'])
        else:
            self.video_rename_dataframe = pd.DataFrame(columns=['original_video_path', 'new_video_path'])


    def rename_video_file_name(self, video_file_name):
        video_id_and_name = video_file_name.split("_")[3:]
        new_video_file_name = '_'.join(video_id_and_name)
        new_video_file_name  = re.sub(r'[^a-zA-Z0-9-_.]', '', new_video_file_name) #remove unnecessary characters (except alphanumeric,-,_, and .)
        return new_video_file_name.lower()


    def insert_in_dataframe(self, original_video_path, new_video_path):
        new_video_rename_row = {'original_video_path':original_video_path, 'new_video_path': new_video_path}
        new_video_rename_dataframe = pd.DataFrame(new_video_rename_row, index=[0])
        self.video_rename_dataframe = pd.concat([self.video_rename_dataframe, new_video_rename_dataframe], ignore_index=True)
        self.video_rename_dataframe.to_csv(RENAME_FILES_DATAFRAME_PATH, index=False)

    def copy_video_to_unique_directory(self,video_file_path, new_video_file_name):
        if not os.path.isdir(ONLY_UNIQUE_VIDEO_DIRECTORY):
            os.mkdir(ONLY_UNIQUE_VIDEO_DIRECTORY)
        new_path_of_video = f"{ONLY_UNIQUE_VIDEO_DIRECTORY}/{new_video_file_name}"

        if not os.path.isfile(new_path_of_video):
            self.insert_in_dataframe(video_file_path, new_path_of_video)
            shutil.copy(video_file_path, new_path_of_video)
        else:
            print(f"{new_video_file_name} already present in {ONLY_UNIQUE_VIDEO_DIRECTORY} directory.")

    def process(self):
        input_video_file_path_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
        for video_file_path in input_video_file_path_list:
            video_file_name = video_file_path.split("/")[-1]
            new_video_file_name = self.rename_video_file_name(video_file_name)
            self.copy_video_to_unique_directory(video_file_path, new_video_file_name)


if __name__ == "__main__":
    rename_video_files_obj = RENAME_VIDEO_FILES()
    rename_video_files_obj.process()



import glob
import os
import re
import shutil

import pandas as pd

from config import *


class RENAMEVIDEOFILES():
    def __init__(self):
        if os.path.isfile(RENAME_FILES_DATAFRAME_PATH):
            try:
                self.rename_video_dataframe = pd.read_csv(RENAME_FILES_DATAFRAME_PATH)
            except:
                self.rename_video_dataframe = pd.DataFrame(columns=['video_id', 'new_video_filename', 'original_video_filename'])
        else:
            self.rename_video_dataframe = pd.DataFrame(columns=['video_id', 'new_video_filename', 'original_video_filename'])

    def rename_video_file_name(self, original_video_file_name):
        video_id_and_name = original_video_file_name.split("_")[3:]
        new_video_file_name = '_'.join(video_id_and_name)
        new_video_file_name  = re.sub(r'[^a-zA-Z0-9-_.]', '_', new_video_file_name) #remove unnecessary characters (except alphanumeric,-,_, and .)
        return new_video_file_name.lower().replace('__', '_').replace('_'+INPUT_VIDEO_FILE_FORMAT, INPUT_VIDEO_FILE_FORMAT)


    def insert_in_dataframe(self, vid, new_video_filename, original_video_filename):
        new_row = {'video_id': vid, 'new_video_filename': new_video_filename, 'original_video_filename': original_video_filename}
        new_dataframe = pd.DataFrame(new_row, index=[0])
        self.rename_video_dataframe = pd.concat([self.rename_video_dataframe, new_dataframe], ignore_index=True)
        self.rename_video_dataframe.to_csv(RENAME_FILES_DATAFRAME_PATH, index=False)

    def copy_video_to_unique_directory(self, original_video_file_path, new_video_file_name):
        if not os.path.isdir(ONLY_UNIQUE_VIDEO_DIRECTORY):
            os.mkdir(ONLY_UNIQUE_VIDEO_DIRECTORY)
        new_path_of_video = f"{ONLY_UNIQUE_VIDEO_DIRECTORY}/{new_video_file_name}"

        if not os.path.isfile(new_path_of_video):
            original_video_file_name = original_video_file_path.split("/")[-1]
            vid = new_video_file_name.split("_")[0]
            self.insert_in_dataframe(vid, new_video_file_name, original_video_file_name)
            shutil.copy(original_video_file_path, new_path_of_video)
        else:
            print(f"{original_video_file_path} already present in {ONLY_UNIQUE_VIDEO_DIRECTORY} directory.")

    def process(self):
        input_video_file_path_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
        for original_video_file_path in input_video_file_path_list:
            original_video_file_name = original_video_file_path.split("/")[-1]
            new_video_file_name = self.rename_video_file_name(original_video_file_name)
            self.copy_video_to_unique_directory(original_video_file_path, new_video_file_name)


if __name__ == "__main__":
    rename_video_files_obj = RENAMEVIDEOFILES()
    rename_video_files_obj.process()



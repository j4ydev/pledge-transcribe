import glob
import pandas as pd
from config import INPUT_VIDEO_DIRECTORY, FLATTEN_VIDEO_DIRECTORY, VIDEO_FILE_FORMAT, FLATTEN_VIDEO_CSV_FILE_PATH, FLATTEN_VIDEO_ERROR_CSV_FILE_PATH
import shutil
import os
from utils import get_metadata_from_file_name

class FLATTENORIGINALVIDEOS():
    def __init__(self):
        if os.path.isfile(FLATTEN_VIDEO_CSV_FILE_PATH):
            try:
                self.flatten_dataframe = pd.read_csv(FLATTEN_VIDEO_CSV_FILE_PATH)
            except Exception as e:
                print(f"{FLATTEN_VIDEO_CSV_FILE_PATH} already present.")
                self.flatten_dataframe = pd.DataFrame(columns=['video_id', 'input_video_file_path'])
        else:
            self.flatten_dataframe = pd.DataFrame(columns=['video_id', 'input_video_file_path'])

        if os.path.isfile(FLATTEN_VIDEO_ERROR_CSV_FILE_PATH):
            try:
                self.error_flatten_dataframe = pd.read_csv(FLATTEN_VIDEO_ERROR_CSV_FILE_PATH)
            except Exception as e:
                print(f"{FLATTEN_VIDEO_ERROR_CSV_FILE_PATH} already present.")
                self.error_flatten_dataframe = pd.DataFrame(columns=['video_path'])
        else:
            self.error_flatten_dataframe = pd.DataFrame(columns=['video_path'])

        if not os.path.isdir(FLATTEN_VIDEO_DIRECTORY):
            os.makedirs(FLATTEN_VIDEO_DIRECTORY)


    def process(self):

        input_video_folder_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*")
        print(input_video_folder_list)
        for index, input_video_folder in enumerate(input_video_folder_list):
            input_video_file_list = glob.glob(f"{input_video_folder}/*{VIDEO_FILE_FORMAT}")
            print(input_video_folder)
            print(len(input_video_file_list))
            for video_path in input_video_file_list:
                # print(video_path)
                try:
                    video_name = video_path.split("/")[-1].replace(VIDEO_FILE_FORMAT, "")
                    file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(video_name)
                    if not os.path.isfile(f"{FLATTEN_VIDEO_DIRECTORY}/{video_name}{VIDEO_FILE_FORMAT}"):
                        shutil.copy(video_path, f"{FLATTEN_VIDEO_DIRECTORY}/{video_name}{VIDEO_FILE_FORMAT}")

                        new_flatten_raw = {'video_id': str(video_id_),  'input_video_file_path': f"{FLATTEN_VIDEO_DIRECTORY}/{video_name}{VIDEO_FILE_FORMAT}"}
                        new_flatten_dataframe = pd.DataFrame(new_flatten_raw, index=[0])

                        self.flatten_dataframe = pd.concat([self.flatten_dataframe, new_flatten_dataframe], ignore_index=True)
                        self.flatten_dataframe.to_csv(FLATTEN_VIDEO_CSV_FILE_PATH, index=False)
                except:
                    
                    new_error_flatten_raw = {'video_path': str(video_path)}
                    new_error_flatten_dataframe = pd.DataFrame(new_error_flatten_raw, index=[0])

                    self.error_flatten_dataframe = pd.concat([self.error_flatten_dataframe, new_error_flatten_dataframe], ignore_index=True)
                    self.error_flatten_dataframe.to_csv(FLATTEN_VIDEO_ERROR_CSV_FILE_PATH, index=False)

                    
        
if __name__ == "__main__":
    flatten_obj = FLATTENORIGINALVIDEOS()
    flatten_obj.process()

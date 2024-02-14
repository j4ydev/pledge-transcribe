import glob
import pandas as pd
from config import MANUAL_FACE_CAPTURE_DIRECTORY, FLATTEN_IMAGE_DIRECTORY, FACE_IMAGE_FILE_FORMAT, FLATTEN_CSV_FILE_PATH, FACE_IMAGE_FILE_FORMAT, MANUAL_FACE_IMAGE_FILE_FORMAT, FLATTEN_ERROR_CSV_FILE_PATH
import shutil
import os
from utils import get_metadata_from_file_name

class FLATTENMANUALIMAGES():
    def __init__(self):
        if os.path.isfile(FLATTEN_CSV_FILE_PATH):
            try:
                self.flatten_dataframe = pd.read_csv(FLATTEN_CSV_FILE_PATH)
            except Exception as e:
                print(f"{FLATTEN_CSV_FILE_PATH} already present.")
                self.flatten_dataframe = pd.DataFrame(columns=['video_id', 'manual_image_file_path'])
        else:
            self.flatten_dataframe = pd.DataFrame(columns=['video_id', 'manual_image_file_path'])


        if os.path.isfile(FLATTEN_ERROR_CSV_FILE_PATH):
            try:
                self.error_flatten_dataframe = pd.read_csv(FLATTEN_ERROR_CSV_FILE_PATH)
            except Exception as e:
                print(f"{FLATTEN_ERROR_CSV_FILE_PATH} already present.")
                self.error_flatten_dataframe = pd.DataFrame(columns=['image_path'])
        else:
            self.error_flatten_dataframe = pd.DataFrame(columns=['image_path'])

        if not os.path.isdir(FLATTEN_IMAGE_DIRECTORY):
            os.makedirs(FLATTEN_IMAGE_DIRECTORY)


    def process(self):
        input_video_folder_list = glob.glob(f"{MANUAL_FACE_CAPTURE_DIRECTORY}/*")
        print(input_video_folder_list)
        for index, input_video_folder in enumerate(input_video_folder_list):
            input_video_file_list = glob.glob(f"{input_video_folder}/*")
            print(input_video_folder)
            print(len(input_video_file_list))
            for image_path in input_video_file_list:
                # print(image_path)
                try:
                    image_name = image_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "").replace(MANUAL_FACE_IMAGE_FILE_FORMAT, "").replace(".jpg", "").replace(".JPG", "")
                    file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)
                    if not os.path.isfile(f"{FLATTEN_IMAGE_DIRECTORY}/{image_name}{FACE_IMAGE_FILE_FORMAT}"):
                        shutil.copy(image_path, f"{FLATTEN_IMAGE_DIRECTORY}/{image_name}{FACE_IMAGE_FILE_FORMAT}")

                        new_flatten_raw = {'video_id': str(video_id_),  'manual_image_file_path': f"{FLATTEN_IMAGE_DIRECTORY}/{image_name}{FACE_IMAGE_FILE_FORMAT}"}
                        new_flatten_dataframe = pd.DataFrame(new_flatten_raw, index=[0])

                        self.flatten_dataframe = pd.concat([self.flatten_dataframe, new_flatten_dataframe], ignore_index=True)
                        self.flatten_dataframe.to_csv(FLATTEN_CSV_FILE_PATH, index=False)
                except:
                    
                    new_error_flatten_raw = {'image_path': str(image_path)}
                    new_error_flatten_dataframe = pd.DataFrame(new_error_flatten_raw, index=[0])

                    self.error_flatten_dataframe = pd.concat([self.error_flatten_dataframe, new_error_flatten_dataframe], ignore_index=True)
                    self.error_flatten_dataframe.to_csv(FLATTEN_ERROR_CSV_FILE_PATH, index=False)

                    
        
if __name__ == "__main__":
    flatten_obj = FLATTENMANUALIMAGES()
    flatten_obj.process()

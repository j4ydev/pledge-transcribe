import glob
import json
import os
import time
import pandas as pd
import requests

from config import (ADD_IMAGES_TO_API_CSV_1, ADD_IMAGES_TO_API_ERROR_CSV_1,
                    API_KEY, FACE_IMAGE_FILE_FORMAT,
                    FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY_1,
                    FACE_MATCH_ADD_IMAGES_1_INPUT)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe

class ADDFACES():
    def __init__(self):

        self.key__ =API_KEY
        self.headers = {"Authorization": f"Bearer {self.key__}"}
        self.add_face_url = "https://api.edenai.run/v2/image/face_recognition/add_face"
        self.providers = "amazon"
        self.payload = {"providers": self.providers}

        if not os.path.isdir(FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY_1):
            os.mkdir(FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY_1)

        if os.path.isfile(ADD_IMAGES_TO_API_CSV_1):
            try:
                self.add_images_to_api_dataframe = pd.read_csv(ADD_IMAGES_TO_API_CSV_1)
            except Exception as e:
                print(f"{ADD_IMAGES_TO_API_CSV_1} already present. but could not load.")
                self.add_images_to_api_dataframe = pd.DataFrame(columns=['video_id', 'face_id', 'image_file_path'])
        else:
            self.add_images_to_api_dataframe = pd.DataFrame(columns=['video_id', 'face_id', 'image_file_path'])

        if os.path.isfile(ADD_IMAGES_TO_API_ERROR_CSV_1):
            try:
                self.add_images_to_api_error_dataframe = pd.read_csv(ADD_IMAGES_TO_API_ERROR_CSV_1)
            except Exception as e:
                print(f"{ADD_IMAGES_TO_API_ERROR_CSV_1} already present. but could not load.")
                self.add_images_to_api_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.add_images_to_api_error_dataframe = pd.DataFrame(columns=['video_id'])

    
    def process(self, face_path):
        ## add face images
        face_image_name = face_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "")
        _, video_id_, _ = get_metadata_from_file_name(face_image_name)

        is_value_present_flag = is_value_present_in_dataframe(video_id_, self.add_images_to_api_dataframe)
        is_value_present_flag_in_error = is_value_present_in_dataframe(video_id_, self.add_images_to_api_error_dataframe)
        already_processed = is_value_present_flag or is_value_present_flag_in_error

        if not already_processed:
            try:
                files = {"file": open(face_path, "rb")}
                print(f"{video_id_}: uploading  {face_path}")
                response = requests.post(
                    self.add_face_url, data=self.payload, files=files, headers=self.headers
                )
                
                face_id = eval(response.text)["amazon"]["face_ids"][0]
                with open(f"{FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY_1}/{video_id_}_{face_id}.json", "w") as json_file:
                    json.dump(response.json(), json_file)

                new_add_images_to_api_raw = {'video_id': str(video_id_), 'face_id': str(face_id), 'image_file_path' : str(face_path),}
                new_add_images_to_api_dataframe = pd.DataFrame(new_add_images_to_api_raw, index=[0])

                self.add_images_to_api_dataframe = pd.concat([self.add_images_to_api_dataframe, new_add_images_to_api_dataframe], ignore_index=True)
                self.add_images_to_api_dataframe.to_csv(ADD_IMAGES_TO_API_CSV_1, index=False)
                time.sleep(0.1)
            except:
                print(f"{video_id_}: -------------- upload failed --------------  {face_path}")
                new_add_images_to_api_error_raw = {'video_id': str(video_id_)}
                new_add_images_to_api_error_dataframe = pd.DataFrame(new_add_images_to_api_error_raw, index=[0])
                self.add_images_to_api_error_dataframe = pd.concat([self.add_images_to_api_error_dataframe, new_add_images_to_api_error_dataframe], ignore_index=True)
                self.add_images_to_api_error_dataframe.to_csv(ADD_IMAGES_TO_API_ERROR_CSV_1, index=False)


if __name__ == "__main__":
    add_faces_obj = ADDFACES()

    face_images_list = glob.glob(f"{FACE_MATCH_ADD_IMAGES_1_INPUT}/*{FACE_IMAGE_FILE_FORMAT}")
    # print(face_images_list)
    for face_image_path in face_images_list:
        # print(face_image_path)
        add_faces_obj.process(face_image_path)
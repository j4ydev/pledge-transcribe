import glob
import os
import time

import pandas as pd
import requests
import json
from config import (ADD_IMAGES_TO_API_CSV, ADD_IMAGES_TO_API_ERROR_CSV,
                    API_KEY, FACE_IMAGE_FILE_FORMAT, FINAL_FACES_DIRECTORY, FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe


class ADDFACES():
    def __init__(self):

        self.key__ =API_KEY
        self.headers = {"Authorization": f"Bearer {self.key__}"}
        self.add_face_url = "https://api.edenai.run/v2/image/face_recognition/add_face"
        self.providers = "amazon"
        self.payload = {"providers": self.providers}
        # print("-------------------")

        if not os.path.isdir(FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY):
            os.mkdir(FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY)

        if os.path.isfile(ADD_IMAGES_TO_API_CSV):
            try:
                self.add_images_to_api_dataframe = pd.read_csv(ADD_IMAGES_TO_API_CSV)
            except Exception as e:
                print(f"{ADD_IMAGES_TO_API_CSV} already present.")
                self.add_images_to_api_dataframe = pd.DataFrame(columns=['video_id', 'image_file_path','face_id'])
        else:
            self.add_images_to_api_dataframe = pd.DataFrame(columns=['video_id', 'image_file_path', 'face_id'])

        if os.path.isfile(ADD_IMAGES_TO_API_ERROR_CSV):
            try:
                self.add_images_to_api_error_dataframe = pd.read_csv(ADD_IMAGES_TO_API_ERROR_CSV)
            except Exception as e:
                print(f"{ADD_IMAGES_TO_API_ERROR_CSV} already present.")
                self.add_images_to_api_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.add_images_to_api_error_dataframe = pd.DataFrame(columns=['video_id'])

    def process(self, face_path):
        ## add face images
        face_image_name = face_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "")
        file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(face_image_name)
        is_value_present_flag = is_value_present_in_dataframe(video_id_, self.add_images_to_api_dataframe)

        if not is_value_present_flag:
            try:
                files = {"file": open(face_path, "rb")}
                print(f"{video_id_}: uploading  {face_path}")
                response = requests.post(
                    self.add_face_url, data=self.payload, files=files, headers=self.headers
                )
                
                with open(f"{FACE_MATCH_ADD_IMAGES_RESPONSE_DIRECTORY}/{video_id_}.json", "w") as json_file:
                    json.dump(response.json(), json_file)

                face_id = eval(response.text)["amazon"]["face_ids"][0]
                new_add_images_to_api_raw = {'video_id': str(video_id_), 'image_file_path' : str(face_path), 'face_id': str(face_id)}
                new_add_images_to_api_dataframe = pd.DataFrame(new_add_images_to_api_raw, index=[0])

                self.add_images_to_api_dataframe = pd.concat([self.add_images_to_api_dataframe, new_add_images_to_api_dataframe], ignore_index=True)
                self.add_images_to_api_dataframe.to_csv(ADD_IMAGES_TO_API_CSV, index=False)
                time.sleep(0.75)
            except:
                new_add_images_to_api_error_raw = {'video_id': str(video_id_)}
                new_add_images_to_api_error_dataframe = pd.DataFrame(new_add_images_to_api_error_raw, index=[0])

                self.add_images_to_api_error_dataframe = pd.concat([self.add_images_to_api_error_dataframe, new_add_images_to_api_error_dataframe], ignore_index=True)
                self.add_images_to_api_error_dataframe.to_csv(ADD_IMAGES_TO_API_ERROR_CSV, index=False)


if __name__ == "__main__":
    add_faces_obj = ADDFACES()

    face_images_list = glob.glob(f"{FINAL_FACES_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
    print(face_images_list)
    for face_image_path in face_images_list:
        print(face_image_path)
        add_faces_obj.process(face_image_path)
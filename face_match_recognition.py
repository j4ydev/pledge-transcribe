import glob
import os
import shutil
import time

import pandas as pd
import requests

from config import (ADD_IMAGES_TO_API_CSV, API_KEY, FACE_IMAGE_FILE_FORMAT,
                    FINAL_FACES_DIRECTORY, FIND_FACES_API_CSV,
                    FIND_FACES_API_ERROR_CSV, FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY,
                    SIMILAR_PLEDGE_TAKERS_API_DIRECTORY)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe
import json

class FINDFACESAPI():
    def __init__(self):

        self.key__ = API_KEY
        self.headers = {"Authorization": f"Bearer {self.key__}"}
        self.recognize_url = "https://api.edenai.run/v2/image/face_recognition/recognize" # TODO:Done not needed
        self.providers = "amazon"
        self.payload = {"providers": self.providers}
        self.add_images_to_api_dataframe = pd.read_csv(ADD_IMAGES_TO_API_CSV)

        if os.path.isfile(FIND_FACES_API_CSV):
            try:
                self.find_faces_api_dataframe = pd.read_csv(FIND_FACES_API_CSV)
            except Exception as e:
                print(f"{FIND_FACES_API_CSV} already present.")
                self.find_faces_api_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_faces_api_dataframe = pd.DataFrame(columns=['video_id'])

        if os.path.isfile(FIND_FACES_API_ERROR_CSV):
            try:
                self.find_faces_api_error_dataframe = pd.read_csv(FIND_FACES_API_ERROR_CSV)
            except Exception as e:
                print(f"{FIND_FACES_API_ERROR_CSV} already present.")
                self.find_faces_api_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_faces_api_error_dataframe = pd.DataFrame(columns=['video_id'])

        if not os.path.isdir(SIMILAR_PLEDGE_TAKERS_API_DIRECTORY):
            os.mkdir(SIMILAR_PLEDGE_TAKERS_API_DIRECTORY)

        if not os.path.isdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY):
            os.mkdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY)


    def process(self, face_path):
        face_image_name = face_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "")
        file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(face_image_name)
        is_value_present_flag = is_value_present_in_dataframe(video_id_, self.find_faces_api_dataframe)

        if not is_value_present_flag:
            try:
                time.sleep(0.75)
                # print("--" * 20)
                face_to_recognize = {"file": open(face_path, 'rb')}
                # recognize_url = "https://api.edenai.run/v2/image/face_recognition/recognize" # TODO:Done move up
                recognize_response = requests.post(
                    self.recognize_url, data=self.payload, files=face_to_recognize, headers=self.headers
                )
                # TODO:Done edenai_recognize -> vid.json
                with open(f"{FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY}/{video_id_}.json", "w") as json_file:
                    json.dump(recognize_response.json(), json_file)

                print("response::", recognize_response)
                matches = recognize_response.json()[self.providers]["items"]
                # print("matches::", matches)
                if len(matches) == 0:
                    match_found_status = False
                else:
                    match_found_status = True

                new_face_match_api_row = {'video_id': str(video_id_), 'match_found': match_found_status, 'face_match_0': video_id_, 'confidence_0': 100}

                i=0
                for matching_face_file_info in matches:
                    i= i+1
                    print("-- ++ " * 20 )
                    # print("matching_face_file_info::", matching_face_file_info) # TODO: Done
                    face_id = matching_face_file_info["face_id"]
                    confidence = matching_face_file_info["confidence"]
                    image_file_path = self.add_images_to_api_dataframe.loc[self.add_images_to_api_dataframe['face_id'] == str(face_id), 'image_file_path'].iloc[0]
                    print("image_file_path::", image_file_path)
                    _, face_video_id, face_video_suffix = get_metadata_from_file_name(image_file_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, ""))
                    new_face_match_api_row[f"face_match_{i}"] = face_video_id
                    new_face_match_api_row[f"confidence_{i}"] = confidence * 100

                print("new_face_match_api_row::", new_face_match_api_row)
                new_face_match_dataframe = pd.DataFrame(new_face_match_api_row, index=[0])
                self.find_faces_api_dataframe = pd.concat([self.find_faces_api_dataframe, new_face_match_dataframe], ignore_index=True)
                self.find_faces_api_dataframe.to_csv(FIND_FACES_API_CSV, index=False)

            except:
                new_find_faces_api_error_raw = {'video_id': str(video_id_)}
                new_find_face_api_error_dataframe = pd.DataFrame(new_find_faces_api_error_raw, index=[0])
                self.find_faces_api_error_dataframe = pd.concat([self.find_faces_api_error_dataframe, new_find_face_api_error_dataframe], ignore_index=True)
                self.find_faces_api_error_dataframe.to_csv(FIND_FACES_API_ERROR_CSV, index=False)


if __name__ == "__main__":
    find_faces_obj = FINDFACESAPI()

    face_images_list = glob.glob(f"{FINAL_FACES_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
    for face_image_path in face_images_list:
        # print("=================", face_image_path)
        find_faces_obj.process(face_image_path)




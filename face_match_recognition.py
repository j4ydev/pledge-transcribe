import glob
import json
import os
import shutil
import time

import pandas as pd
import requests
from icecream import ic

from config import (ADD_IMAGES_TO_API_CSV, API_KEY, FACE_IMAGE_FILE_FORMAT,
                    FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY,
                    FINAL_FACES_DIRECTORY, FIND_FACES_API_CSV,
                    FIND_FACES_API_ERROR_CSV)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe

# Unique to each thread
# FINAL_FACES_DIRECTORY, # input
# FIND_FACES_API_CSV, # o/p
# FIND_FACES_API_ERROR_CSV, # o/p

class FINDFACESAPI():
    def __init__(self):

        self.key__ = API_KEY
        self.headers = {"Authorization": f"Bearer {self.key__}"}
        self.recognize_url = "https://api.edenai.run/v2/image/face_recognition/recognize"
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

        if not os.path.isdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY):
            os.mkdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY)


    def process(self, face_path):
        face_image_name = face_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, "")
        file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(face_image_name)
        is_value_present_flag = is_value_present_in_dataframe(video_id_, self.find_faces_api_dataframe)

        if not is_value_present_flag:
            try:
                # time.sleep(0.6)
                print(video_id_, ":----:", face_path)
                face_to_recognize = {"file": open(face_path, 'rb')}
                recognize_response = requests.post(
                    self.recognize_url, data=self.payload, files=face_to_recognize, headers=self.headers
                )
                ic(recognize_response.json())
                with open(f"{FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY}/{video_id_}.json", "w") as json_file:
                    json.dump(recognize_response.json(), json_file)

                print(video_id_, ":: recognize_response ", recognize_response)
                new_face_match_api_row = {'video_id': str(video_id_), 'match_found': False, 'face_match_0': video_id_, 'confidence_0': 100}

                try:
                    matches = recognize_response.json()[self.providers]["items"]
                    if len(matches) == 0:
                        match_found_status = False
                    else:
                        match_found_status = True

                    print(video_id_, ":: matches ::", len(matches))
                    new_face_match_api_row['match_found'] = match_found_status

                    i=0
                    for matching_face_file_info in matches:
                        i= i+1
                        face_id = matching_face_file_info["face_id"]
                        confidence = matching_face_file_info["confidence"]
                        print("---------", i)
                        row = self.add_images_to_api_dataframe.loc[self.add_images_to_api_dataframe['face_id'] == str(face_id), 'image_file_path']
                        face_video_id = face_id
                        print(type(row))
                        if not row.empty:
                            image_file_path = row.iloc[0]
                            print("image_file_path::", image_file_path)
                            _, face_video_id, face_video_suffix = get_metadata_from_file_name(image_file_path.split("/")[-1].replace(FACE_IMAGE_FILE_FORMAT, ""))
                        new_face_match_api_row[f"face_match_{i}"] = face_video_id
                        new_face_match_api_row[f"confidence_{i}"] = confidence * 100
                except Exception as e:
                   print(f"An error occurred: {e}")

                new_face_match_dataframe = pd.DataFrame(new_face_match_api_row, index=[0])
                self.find_faces_api_dataframe = pd.concat([self.find_faces_api_dataframe, new_face_match_dataframe], ignore_index=True)
                self.find_faces_api_dataframe.to_csv(FIND_FACES_API_CSV, index=False)
                return True

            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"{video_id_}: ", face_path, "::---failed---::", )
                new_find_faces_api_error_raw = {'video_id': str(video_id_)}
                new_find_face_api_error_dataframe = pd.DataFrame(new_find_faces_api_error_raw, index=[0])
                self.find_faces_api_error_dataframe = pd.concat([self.find_faces_api_error_dataframe, new_find_face_api_error_dataframe], ignore_index=True)
                self.find_faces_api_error_dataframe.to_csv(FIND_FACES_API_ERROR_CSV, index=False)
                return False
        return True

if __name__ == "__main__":
    find_faces_obj = FINDFACESAPI()

    face_images_list = glob.glob(f"{FINAL_FACES_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
    face_images_list.sort()
    count = len(face_images_list)

    i=0
    for face_image_path in face_images_list:
        start_time = time.time()
        res = find_faces_obj.process(face_image_path)
        end_time = time.time()
        time_consumed_by_face_capture = end_time - start_time
        print(i,count, ": time_consumed_by_face_capture: ", time_consumed_by_face_capture, face_image_path)
        if not res:
            break
        if i>4000:
            break
        i=i+1




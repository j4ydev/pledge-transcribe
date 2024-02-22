import json
import os
import time
import pandas as pd
import requests

from config import (ADD_IMAGES_TO_API_CSV_1,  
                    API_KEY,
                    FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY_1,
                    FIND_FACES_API_CSV_1, FIND_FACES_API_ERROR_CSV_1)
from utils import  is_value_present_in_dataframe



class FINDFACESAPI():
    def __init__(self):

        self.key__ = API_KEY
        self.headers = {"Authorization": f"Bearer {self.key__}"}
        self.recognize_url = "https://api.edenai.run/v2/image/face_recognition/recognize"
        self.providers = "amazon"
        self.payload = {"providers": self.providers}
        

        if not os.path.isdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY_1):
            os.mkdir(FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY_1)

        if os.path.isfile(FIND_FACES_API_CSV_1):
            try:
                self.find_faces_api_dataframe = pd.read_csv(FIND_FACES_API_CSV_1)
            except Exception as e:
                print(f"{FIND_FACES_API_CSV_1} already present. but could not load.")
                self.find_faces_api_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_faces_api_dataframe = pd.DataFrame(columns=['video_id'])

        if os.path.isfile(FIND_FACES_API_ERROR_CSV_1):
            try:
                self.find_faces_api_error_dataframe = pd.read_csv(FIND_FACES_API_ERROR_CSV_1)
            except Exception as e:
                print(f"{FIND_FACES_API_ERROR_CSV_1} already present.but could not load.")
                self.find_faces_api_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_faces_api_error_dataframe = pd.DataFrame(columns=['video_id'])



    def process(self, row):

        face_path = row["image_file_path"]
        face_id = row["face_id"]
        video_id_ = row["video_id"]
        
        is_value_present_flag = is_value_present_in_dataframe(video_id_, self.find_faces_api_dataframe)
        ## we are just checking successful images only we are not checking if the video_id is been added to error or not.
        if not is_value_present_flag:
            try:
                # time.sleep(0.6)
                print(video_id_, ":----:", face_path)
                face_to_recognize = {"file": open(face_path, 'rb')}
                recognize_response = requests.post(
                    self.recognize_url, data=self.payload, files=face_to_recognize, headers=self.headers
                )
                
                with open(f"{FACE_MATCH_RECOGNITION_RESPONSE_DIRECTORY_1}/{video_id_}_{face_id}.json", "w") as json_file:
                    json.dump(recognize_response.json(), json_file)

                print(video_id_, ":: recognize_response ", recognize_response)
                new_face_match_api_row = {'video_id': str(video_id_), "face_id": str(face_id), "image_file_path": face_path}

                try:
                    matches = recognize_response.json()[self.providers]["items"]
                    
                    print(video_id_, ":: matches ::", len(matches))
                    i=0
                    for matching_face_file_info in matches:
                        i = i+1
                        face_id = matching_face_file_info["face_id"]
                        confidence = matching_face_file_info["confidence"]
                        print("---------", i)
                        
                        new_face_match_api_row[f"face_match_{i}"] = face_id
                        new_face_match_api_row[f"confidence_{i}"] = confidence * 100
                except Exception as e:
                   print("video_id_", str(video_id_), "Face not found in image....")
                   print(f"An error occurred: {e}")

                new_face_match_dataframe = pd.DataFrame(new_face_match_api_row, index=[0])
                self.find_faces_api_dataframe = pd.concat([self.find_faces_api_dataframe, new_face_match_dataframe], ignore_index=True)
                self.find_faces_api_dataframe.to_csv(FIND_FACES_API_CSV_1, index=False)
                return True

            except Exception as e:
                print(f"An error occurred: {e}")
                print(f"{video_id_}: ", face_path, "::---failed---::", )
                new_find_faces_api_error_raw = {'video_id': str(video_id_)}
                new_find_face_api_error_dataframe = pd.DataFrame(new_find_faces_api_error_raw, index=[0])
                self.find_faces_api_error_dataframe = pd.concat([self.find_faces_api_error_dataframe, new_find_face_api_error_dataframe], ignore_index=True)
                self.find_faces_api_error_dataframe.to_csv(FIND_FACES_API_ERROR_CSV_1, index=False)
                return False
        return True


    
if __name__ == "__main__":
    find_faces_obj = FINDFACESAPI()

    add_images_to_api_dataframe = pd.read_csv(ADD_IMAGES_TO_API_CSV_1)
    start_point = 0
    end_point = 4000
    for index, row in add_images_to_api_dataframe.iterrows():
        if index >= start_point and index <= end_point:
            # face_image_path = row["image_file_path"]
            start_time = time.time()
            res = find_faces_obj.process(row)
            end_time = time.time()
            time_consumed_by_face_capture = end_time - start_time
            print(index, ": time_consumed_by_face_capture: ", time_consumed_by_face_capture, row["video_id"])
        else:
            break
            
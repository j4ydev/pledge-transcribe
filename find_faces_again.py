from deepface import DeepFace

import pandas as pd
import numpy as np

import cv2
import glob

from config import (FINAL_FACES_CSV_PATH, FINAL_FACES_DIRECTORY, FINAL_FACES_CSV_PATH, VIDEO_FILE_FORMAT,
                    FLATTEN_VIDEO_DIRECTORY, FLATTEN_VIDEO_CSV_FILE_PATH, FACE_IMAGE_FILE_FORMAT, FINDING_FACE_AGAIN_CSV_PATH,
                    FINDING_FACE_AGAIN_ERROR_CSV_PATH)
from utils import is_value_present_in_dataframe
import shutil

import os


class FINDFACESAGAIN():

    def __init__(self):
        self.accepted_video_faces = pd.read_csv(FINAL_FACES_CSV_PATH)
        self.filtered_df = self.accepted_video_faces[(self.accepted_video_faces['auto_face_found'] == False) & 
                        (self.accepted_video_faces['file_gathered'] == True) & 
                        (self.accepted_video_faces['face_found'] == False)]
        self.face_not_found_video_id_list = list(self.filtered_df['video_id'])
        self.all_video_files_list = glob.glob(f"{FLATTEN_VIDEO_DIRECTORY}/*")
        self.flatten_video_dataframe = pd.read_csv(FLATTEN_VIDEO_CSV_FILE_PATH)



        if os.path.isfile(FINDING_FACE_AGAIN_CSV_PATH):
            try:
                self.find_face_again_dataframe = pd.read_csv(FINDING_FACE_AGAIN_CSV_PATH)
            except Exception as e:
                print(f"{FINDING_FACE_AGAIN_CSV_PATH} already present.")
                self.find_face_again_dataframe = pd.DataFrame(columns=['video_id', 'face_found'])
        else:
            self.find_face_again_dataframe = pd.DataFrame(columns=['video_id', 'face_found'])


        if os.path.isfile(FINDING_FACE_AGAIN_ERROR_CSV_PATH):
            try:
                self.find_face_again_error_dataframe = pd.read_csv(FINDING_FACE_AGAIN_ERROR_CSV_PATH)
            except Exception as e:
                print(f"{FINDING_FACE_AGAIN_ERROR_CSV_PATH} already present.")
                self.find_face_again_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.find_face_again_error_dataframe = pd.DataFrame(columns=['video_id'])


    def find_face(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = True
        except Exception as e:
            found_face_flag = False
        return found_face_flag

    def find_face_from_video(self, video_file, video_id):
        print(video_file)
        video = cv2.VideoCapture(video_file)        
        frame_count = 0
        
        while True:
            ret, frame = video.read()
            if not ret:
                break
            # if frame_count % 2 == 0:
            cv2.imwrite(f"temp_face.png", frame)
            validation = self.find_face("temp_face.png","temp_face.png")

            if validation:
                video_file_name = video_file.split("/")[-1].replace(VIDEO_FILE_FORMAT, "")
                face_image_path = f"{FINAL_FACES_DIRECTORY}/{video_file_name}{FACE_IMAGE_FILE_FORMAT}"
                shutil.copy("temp_face.png", face_image_path)
                self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'auto_face_found'] = True
                self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'file_gathered'] = True
                self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'face_found'] = True
                self.accepted_video_faces.to_csv(FINAL_FACES_CSV_PATH, index=False)
                return True

            frame_count += 1     
        # Release the video object
        return False
        video.release()




    def process(self):
        
        for video_id in self.face_not_found_video_id_list:
            
            try:
                is_value_present_flag = is_value_present_in_dataframe(video_id, self.find_face_again_dataframe)

                if not is_value_present_flag:
                    print(len(self.face_not_found_video_id_list))
                    print("video_id::", video_id)
                    video_file_path = self.flatten_video_dataframe.loc[self.flatten_video_dataframe['video_id'] == video_id, 'input_video_file_path'].iloc[0]
                    face_find_status = self.find_face_from_video(video_file_path, video_id)
                    new_find_face_again_raw = {'video_id': video_id, 'face_found': face_find_status}
                    print(new_find_face_again_raw)
                    print("----------------------")
                    new_find_face_again_dataframe = pd.DataFrame(new_find_face_again_raw, index=[0])
                    self.find_face_again_dataframe = pd.concat([self.find_face_again_dataframe, new_find_face_again_dataframe], ignore_index=True)
                    self.find_face_again_dataframe.to_csv(FINDING_FACE_AGAIN_CSV_PATH, index=False)
            except:
                new_find_face_again_error_raw = {'video_id': video_id}
                new_find_face_again_error_dataframe = pd.DataFrame(new_find_face_again_error_raw, index=[0])
                self.find_face_again_error_dataframe = pd.concat([self.find_face_again_error_dataframe, new_find_face_again_error_dataframe], ignore_index=True)
                self.find_face_again_error_dataframe.to_csv(FINDING_FACE_AGAIN_ERROR_CSV_PATH, index=False)

if __name__  == "__main__":
    find_face_again_obj = FINDFACESAGAIN()
    find_face_again_obj.process()





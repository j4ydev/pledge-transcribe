import glob
import os
import shutil

import cv2
import pandas as pd
from deepface import DeepFace

from config import (CAPTURE_FACE_BRUT_FORCE_25_PER_CSV_PATH,
                    CAPTURE_FACE_BRUT_FORCE_25_PER_ERROR_CSV_PATH,
                    CAPTURE_FACES_BRUT_FORCE_25_PER_DIRECTORY,
                    CAPTURE_FACES_BRUT_FORCE_25_PER_ERROR_DIRECTORY,
                    SCREENSHOT_NOT_FOUND_DATAFRAME_PATH,
                    FACE_IMAGE_FILE_FORMAT, FLATTEN_VIDEO_CSV_FILE_PATH,
                    VIDEO_FILE_FORMAT)
from utils import is_value_present_in_dataframe


class CAPTUREFACEBRUT():
    def __init__(self):
        
        self.inspect_dataframe = pd.read_csv(SCREENSHOT_NOT_FOUND_DATAFRAME_PATH)
        self.flatten_video_dataframe = pd.read_csv(FLATTEN_VIDEO_CSV_FILE_PATH)

        if not os.path.isdir(CAPTURE_FACES_BRUT_FORCE_25_PER_DIRECTORY):
            os.mkdir(CAPTURE_FACES_BRUT_FORCE_25_PER_DIRECTORY)
        if not os.path.isdir(CAPTURE_FACES_BRUT_FORCE_25_PER_ERROR_DIRECTORY):
            os.mkdir(CAPTURE_FACES_BRUT_FORCE_25_PER_ERROR_DIRECTORY)

        if os.path.isfile(CAPTURE_FACE_BRUT_FORCE_25_PER_CSV_PATH):
            try:
                self.capture_face_brut_force_dataframe = pd.read_csv(CAPTURE_FACE_BRUT_FORCE_25_PER_CSV_PATH)
            except Exception as e:
                print(f"{CAPTURE_FACE_BRUT_FORCE_25_PER_CSV_PATH} already present.")
                self.capture_face_brut_force_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])
        else:
            self.capture_face_brut_force_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])


        if os.path.isfile(CAPTURE_FACE_BRUT_FORCE_25_PER_ERROR_CSV_PATH):
            try:
                self.capture_face_brut_force_error_dataframe = pd.read_csv(CAPTURE_FACE_BRUT_FORCE_25_PER_ERROR_CSV_PATH)
            except Exception as e:
                print(f"{CAPTURE_FACE_BRUT_FORCE_25_PER_ERROR_CSV_PATH} already present.")
                self.capture_face_brut_force_error_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.capture_face_brut_force_error_dataframe = pd.DataFrame(columns=['video_id'])

    def find_face(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = True
        except Exception as e:
            
            found_face_flag = False
        return found_face_flag

    def find_face_from_video(self, video_file, video_id):

        video = cv2.VideoCapture(video_file)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count_start = int(total_frames * 0.25)
        frame_count = 0

        while True:
            frame_count += 1
            if frame_count_start > frame_count and frame_count <= total_frames:
                ret, frame = video.read()
                if not ret:
                    break

                cv2.imwrite(f"temp_face.png", frame)
                validation = self.find_face("temp_face.png","temp_face.png")

                if validation:
                    video_file_name = video_file.split("/")[-1].replace(VIDEO_FILE_FORMAT, "")
                    face_image_path = f"{CAPTURE_FACES_BRUT_FORCE_25_PER_DIRECTORY}/{video_file_name}{FACE_IMAGE_FILE_FORMAT}"
                    shutil.copy("temp_face.png", face_image_path)
                    video.release()
                    return True
            else:
                break
        print("FACE NOT FOUND: {video_id}")
        # Release the video object
        video.release()
        return False

    def process(self,):
        for index, row in self.inspect_dataframe.iterrows():
            print("INDEX::", index)
            # if row["InvigilationState"]=="Accept":
            video_id = row['vid']
            # print(video_id)
            try:
                is_value_present_flag = is_value_present_in_dataframe(video_id, self.capture_face_brut_force_dataframe)
                is_error_value_present_flag = is_value_present_in_dataframe(video_id, self.capture_face_brut_force_error_dataframe)
                print(is_value_present_flag)
                if not is_value_present_flag and not is_error_value_present_flag:
                    print("video_id::", video_id)
                    video_file_path = self.flatten_video_dataframe.loc[self.flatten_video_dataframe['video_id'] == video_id, 'input_video_file_path'].iloc[0]
                    face_find_status = self.find_face_from_video(video_file_path, video_id)
                    new_capture_face_brut_force_row = {'video_id': int(video_id), 'face_found_brut': face_find_status}
                    print(new_capture_face_brut_force_row)
                    print("----------------------")
                    new_capture_face_brut_force_dataframe = pd.DataFrame(new_capture_face_brut_force_row, index=[0])
                    self.capture_face_brut_force_dataframe = pd.concat([self.capture_face_brut_force_dataframe, new_capture_face_brut_force_dataframe], ignore_index=True)
                    self.capture_face_brut_force_dataframe.to_csv(CAPTURE_FACE_BRUT_FORCE_25_PER_CSV_PATH, index=False)


            except Exception as e:
                print(f"An error occurred: {e}")
                face_image_path = f"{CAPTURE_FACES_BRUT_FORCE_25_PER_ERROR_DIRECTORY}/{video_id}{FACE_IMAGE_FILE_FORMAT}"
                shutil.copy("temp_face.png", face_image_path)
                new_capture_face_brut_force_error_raw = {'video_id': video_id}
                new_capture_face_brut_force_error_dataframe = pd.DataFrame(new_capture_face_brut_force_error_raw, index=[0])
                self.capture_face_brut_force_error_dataframe = pd.concat([self.capture_face_brut_force_error_dataframe, new_capture_face_brut_force_error_dataframe], ignore_index=True)
                self.capture_face_brut_force_error_dataframe.to_csv(CAPTURE_FACE_BRUT_FORCE_25_PER_ERROR_CSV_PATH, index=False)
            
            print("-- -- -- -- " * 10)
            # a = input()




if __name__ == "__main__":
    capture_face_brut_obj = CAPTUREFACEBRUT()
    capture_face_brut_obj.process()


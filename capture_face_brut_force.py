import glob
import os
import shutil

import cv2
import pandas as pd
from deepface import DeepFace

from config import (CAPTURE_FACE_BRUT_FORCE_CSV_PATH,
                    CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH,
                    CAPTURE_FACES_BRUT_FORCE_DIRECTORY,
                    CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY,
                    FACE_IMAGE_FILE_FORMAT, FLATTEN_VIDEO_CSV_FILE_PATH,
                    INSPECT_DATAFRAME_PATH, VIDEO_FILE_FORMAT)
from utils import is_value_present_in_dataframe


class CAPTUREFACEBRUT():
    def __init__(self):
        print(INSPECT_DATAFRAME_PATH)
        print("--------------------------------")
        self.inspect_dataframe = pd.read_csv(INSPECT_DATAFRAME_PATH)
        print(self.inspect_dataframe.head())
        self.inspect_dataframe["Capture Face"] = self.inspect_dataframe["Capture Face"].fillna("yes")
        self.flatten_video_dataframe = pd.read_csv(FLATTEN_VIDEO_CSV_FILE_PATH)

        if not os.path.isdir(CAPTURE_FACES_BRUT_FORCE_DIRECTORY):
            os.mkdir(CAPTURE_FACES_BRUT_FORCE_DIRECTORY)

        if not os.path.isdir(CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY):
            os.mkdir(CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY)

        if os.path.isfile(CAPTURE_FACE_BRUT_FORCE_CSV_PATH):
            try:
                self.capture_face_brut_force_dataframe = pd.read_csv(CAPTURE_FACE_BRUT_FORCE_CSV_PATH)
            except Exception as e:
                print(f"{CAPTURE_FACE_BRUT_FORCE_CSV_PATH} already present.")
                self.capture_face_brut_force_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])
        else:
            self.capture_face_brut_force_dataframe = pd.DataFrame(columns=['video_id', 'face_found_brut'])


        if os.path.isfile(CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH):
            try:
                self.capture_face_brut_force_error_dataframe = pd.read_csv(CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH)
            except Exception as e:
                print(f"{CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH} already present.")
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
        print(video_file)
        video = cv2.VideoCapture(video_file)
        frame_count = 0

        while True:
            frame_count += 1
            ret, frame = video.read()
            if not ret:
                video.release()
                break

            # if frame_count % 2 == 0:
            cv2.imwrite(f"temp_face.png", frame)
            validation = self.find_face("temp_face.png","temp_face.png")

            if validation:
                video_file_name = video_file.split("/")[-1].replace(VIDEO_FILE_FORMAT, "")
                face_image_path = f"{CAPTURE_FACES_BRUT_FORCE_DIRECTORY}/{video_file_name}{FACE_IMAGE_FILE_FORMAT}"
                shutil.copy("temp_face.png", face_image_path)
                # self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'auto_face_found'] = True
                # self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'file_gathered'] = True
                # self.accepted_video_faces.loc[self.accepted_video_faces['video_id'] == video_id, 'face_found'] = True
                # self.accepted_video_faces.to_csv(FINAL_FACES_CSV_PATH, index=False)
                return True

        # Release the video object
        video.release()
        return False

    def process(self,):
        for index, row in self.inspect_dataframe.iterrows():
            # print(row["Capture Face"])
            # print(row["InvigilationState"])
            if row["Capture Face"]== "yes" and row["InvigilationState"]=="Accept":
                video_id = row['vid']
                # print(video_id)
                try:
                    is_value_present_flag = is_value_present_in_dataframe(video_id, self.capture_face_brut_force_dataframe)
                    # print(is_value_present_flag)
                    if not is_value_present_flag:
                        print("video_id::", video_id)
                        video_file_path = self.flatten_video_dataframe.loc[self.flatten_video_dataframe['video_id'] == video_id, 'input_video_file_path'].iloc[0]
                        face_find_status = self.find_face_from_video(video_file_path, video_id)
                        new_capture_face_brut_force_row = {'video_id': int(video_id), 'face_found_brut': face_find_status}
                        print(new_capture_face_brut_force_row)
                        print("----------------------")
                        new_capture_face_brut_force_dataframe = pd.DataFrame(new_capture_face_brut_force_row, index=[0])
                        self.capture_face_brut_force_dataframe = pd.concat([self.capture_face_brut_force_dataframe, new_capture_face_brut_force_dataframe], ignore_index=True)
                        self.capture_face_brut_force_dataframe.to_csv(CAPTURE_FACE_BRUT_FORCE_CSV_PATH, index=False)


                except:
                    face_image_path = f"{CAPTURE_FACES_BRUT_FORCE_ERROR_DIRECTORY}/{video_id}{FACE_IMAGE_FILE_FORMAT}"
                    shutil.copy("temp_face.png", face_image_path)
                    new_capture_face_brut_force_error_raw = {'video_id': video_id}
                    new_capture_face_brut_force_error_dataframe = pd.DataFrame(new_capture_face_brut_force_error_raw, index=[0])
                    self.capture_face_brut_force_error_dataframe = pd.concat([self.capture_face_brut_force_error_dataframe, new_capture_face_brut_force_error_dataframe], ignore_index=True)
                    self.capture_face_brut_force_error_dataframe.to_csv(CAPTURE_FACE_BRUT_FORCE_ERROR_CSV_PATH, index=False)




if __name__ == "__main__":
    capture_face_brut_obj = CAPTUREFACEBRUT()
    capture_face_brut_obj.process()


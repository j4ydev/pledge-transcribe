import glob
import os
import random
import time

import cv2
import pandas as pd
from deepface import DeepFace
from icecream import ic

from config import (DIRECTORY_OF_INPUT_VIDEO_DIRECTORY, FACE_CAPTURE_CSV_PATH,
                    FACE_IMAGE_DIRECTORY, FACE_IMAGE_FILE_FORMAT,
                    FAILED_FACE_CAPTURE_CSV_PATH, INPUT_VIDEO_FILE_FORMAT, APPROVAL_DATAFRAME_PATH)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe


class GETFRAME():
    def __init__(self):
        if os.path.isfile(FACE_CAPTURE_CSV_PATH):
            try:
                self.face_capture_dataframe = pd.read_csv(FACE_CAPTURE_CSV_PATH)
            except Exception as e:
                print(f"{FACE_CAPTURE_CSV_PATH} already present.")
                self.face_capture_dataframe = pd.DataFrame(columns=['video_id', 'face_found', 'attempt', 'time_consumed'])
        else:
            self.face_capture_dataframe = pd.DataFrame(columns=['video_id', 'face_found', 'attempt', 'time_consumed'])
        self.counter = 0
        if os.path.isfile(FAILED_FACE_CAPTURE_CSV_PATH):
            try:
                self.failed_capture_face_dataframe = pd.read_csv(FAILED_FACE_CAPTURE_CSV_PATH)
            except Exception as e:
                print(f"{FAILED_FACE_CAPTURE_CSV_PATH} already present.")
                self.failed_capture_face_dataframe = pd.DataFrame(columns=['video_id'])
        else:
            self.failed_capture_face_dataframe = pd.DataFrame(columns=['video_id'])     
        self.inspect_dataframe = pd.read_csv(APPROVAL_DATAFRAME_PATH)

    def remove_file_if_exists(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_image_from_video(self, video_path):
        video_capture = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frame = random.randint(1, total_frames-5)
        current_frame = 0
        while True:
            ret, frame = video_capture.read()
            if not ret or current_frame == random_frame:
                break
            current_frame += 1
        if current_frame == random_frame:
            return frame


    def find_face(self, img1_path, img2_path):
        found_face_flag = False
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = result["verified"]
        except Exception as e:
            found_face_flag = False
        return found_face_flag

    def capture_face_image(self, video_file_path, image_file_path_without_extension):
        reference_frame_file_path = f'{FACE_IMAGE_DIRECTORY}/{image_file_path_without_extension}{FACE_IMAGE_FILE_FORMAT}'
        frame_to_compare_file_path = f'{FACE_IMAGE_DIRECTORY}/{image_file_path_without_extension}_2{FACE_IMAGE_FILE_FORMAT}'

        if self.counter == 0:
            print("Attempting to find face in video: ", image_file_path_without_extension)

        self.counter = self.counter + 1

        reference_frame = self.get_image_from_video(video_file_path)
        cv2.imwrite(reference_frame_file_path, reference_frame)
        frame_to_compare = self.get_image_from_video(video_file_path)
        cv2.imwrite(frame_to_compare_file_path, frame_to_compare)

        if self.counter > 30:
            self.remove_file_if_exists(reference_frame_file_path)
            self.remove_file_if_exists(frame_to_compare_file_path)
            print("No face present in video. Attempts: ", self.counter)
            capture_face_status = "False"
            return capture_face_status

        face_found = self.find_face(reference_frame_file_path, frame_to_compare_file_path)

        if face_found == True:
            self.remove_file_if_exists(frame_to_compare_file_path)
            print("Face Found, Attempts: ", self.counter)
            capture_face_status = "True"
            return capture_face_status
        else:
            self.capture_face_image(video_file_path, image_file_path_without_extension)

    def add_failed_capture_face_csv(self, video_path):
        # INSERT DATA IN DATAFRAME

        video_file_name = video_path.split("/")[-1]
        file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(video_file_name)

        # is_value_present_flag = is_value_present_in_dataframe(file_video_id, self.failed_transcribe_dataframe)
        # if not is_value_present_flag:
        new_failed_capture_face_row = {'video_id': file_video_id}
        new_failed_capture_face_dataframe = pd.DataFrame(new_failed_capture_face_row, index=[0])
        self.failed_capture_face_dataframe = pd.concat([self.failed_capture_face_dataframe, new_failed_capture_face_dataframe], ignore_index=True)
        self.failed_capture_face_dataframe.to_csv(FAILED_FACE_CAPTURE_CSV_PATH, index=False)


    def process(self, input_video_file_list):
        for video_file_path in input_video_file_list:
            self.counter = 0
            try:
                video_file_name = video_file_path.split("/")[-1]
                video_file_name = video_file_name.replace(INPUT_VIDEO_FILE_FORMAT, "")
                file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(video_file_name)
                image_file_name_without_extension = video_file_path.split("/")[-1].replace(INPUT_VIDEO_FILE_FORMAT, "")

                approval_status = self.inspect_dataframe.loc[self.inspect_dataframe['video_id'] == file_video_id, 'approval'].iloc[0]
                if approval_status == "Accept":
                    screenshot_present_flag = is_value_present_in_dataframe(file_video_id, self.face_capture_dataframe)
                    if not screenshot_present_flag:
                        self.counter = 0
                        start_time = time.time()
                        capture_face_status = self.capture_face_image(video_file_path, image_file_name_without_extension)
                        end_time = time.time()
                        time_consumed_by_face_capture = end_time - start_time

                        if capture_face_status == None :
                            capture_face_status = "False"
                        
                        if self.counter <= 30:
                            capture_face_status = "True"
                else:
                    capture_face_status = "False"
                    time_consumed_by_face_capture = 0
                    
                new_face_capture_raw = {'video_id': file_video_id, 'face_found': capture_face_status, 'attempt': self.counter, "inspect_csv_status": approval_status, 'time_consumed': time_consumed_by_face_capture}

                print("##" * 20)
                ic(new_face_capture_raw)
                print("##" * 20)

                new_face_capture_dataframe = pd.DataFrame(new_face_capture_raw, index=[0])
                self.face_capture_dataframe = pd.concat([self.face_capture_dataframe, new_face_capture_dataframe], ignore_index=True)
                self.face_capture_dataframe.to_csv(FACE_CAPTURE_CSV_PATH, index=False)       
            except Exception as e:
                print(f"{video_file_path} error occurred.")
                self.add_failed_capture_face_csv(video_file_path)
        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()
    input_video_folder_list = glob.glob(f"{DIRECTORY_OF_INPUT_VIDEO_DIRECTORY}/*")
    input_video_folder_list.sort()
    start_index = 0
    end_index = 50
    # for input_video_folder in input_video_folder_list:
    for index, input_video_folder in enumerate(input_video_folder_list):
        if start_index <= index and index < end_index:
            input_video_file_list = glob.glob(f"{input_video_folder}/*{INPUT_VIDEO_FILE_FORMAT}")
            input_video_file_list.sort()
            getframe_obj.process(input_video_file_list)


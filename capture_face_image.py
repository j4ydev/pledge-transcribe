import glob
import os
import random
import time

import cv2
from deepface import DeepFace
from icecream import ic
import pandas as pd
from utils import *
from config import *  # TODO: Import only needed names or import the module and then use its members. google to know more





# TODO: Jay we should generate an output CSV for this too, and also avoid face capture if already done for that video-id,
# the CSV will have following columns -- video_id, face_found, attempt, time_consumed

class GETFRAME():
    def __init__(self):
        if os.path.isfile(FACE_CAPTURE_CSV_PATH):
            try:
                self.face_capture_dataframe = pd.read_csv(FACE_CAPTURE_CSV_PATH)
            except:
                self.face_capture_dataframe = pd.DataFrame(columns=['video_id', 'face_found', 'attempt', 'time_consumed'])
        else:
            self.face_capture_dataframe = pd.DataFrame(columns=['video_id', 'face_found', 'attempt', 'time_consumed'])

        self.counter = 0

    def remove_file_if_exists(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

    def get_image_from_video(self, video_path):
        video_capture = cv2.VideoCapture(video_path)
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

    # def check_if_screenshot_present(self, image_file_name_without_extension):
    #     possible_screenshot_path = f"{FACE_IMAGE_DIRECTORY}/{image_file_name_without_extension}{FACE_IMAGE_FILE_FORMAT}"
    #     if os.path.isfile(possible_screenshot_path):
    #         return True
    #     else:
    #         return False

    def find_face(self, img1_path, img2_path):
        found_face_flag = False
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = result["verified"]
        except:
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

    def process(self, input_video_file_list):
        for video_file_path in input_video_file_list:
            video_file_name = video_file_path.replace(INPUT_VIDEO_FILE_FORMAT, "")
            file_bid, file_video_id, file_name_suffix = get_metadata_from_file_name(video_file_name)
            image_file_name_without_extension = video_file_path.split("/")[-1].replace(INPUT_VIDEO_FILE_FORMAT, "")
            screenshot_present_flag = is_value_present_in_dataframe(file_video_id, self.face_capture_dataframe)
            if not screenshot_present_flag:
                self.counter = 0
                start_time = time.time()
                capture_face_status = self.capture_face_image(video_file_path, image_file_name_without_extension)
                end_time = time.time()
                time_consumed_by_face_capture = end_time - start_time

                if capture_face_status == None:
                    capture_face_status = "False"
                new_face_capture_raw = {'video_id': file_video_id, 'face_found': capture_face_status, 'attempt': self.counter, 'time_consumed': time_consumed_by_face_capture}

                print("##" * 20)
                ic(new_face_capture_raw)
                print("##" * 20)

                new_face_capture_dataframe = pd.DataFrame(new_face_capture_raw, index=[0])
                self.face_capture_dataframe = pd.concat([self.face_capture_dataframe, new_face_capture_dataframe], ignore_index=True)
                self.face_capture_dataframe.to_csv(FACE_CAPTURE_CSV_PATH, index=False)


        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()
    input_video_file_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*{INPUT_VIDEO_FILE_FORMAT}")
    input_video_file_list.sort()
    getframe_obj.process(input_video_file_list)

import glob
import os
import random

import cv2
from deepface import DeepFace
from icecream import ic
from numpy.linalg import norm

from config import *  # # TODO: Import only needed names or import the module and then use its members. google to know more


class GETFRAME():
    def __init__(self):
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

    def check_if_screenshot_present(self, image_file_name_without_extension):
        possible_screenshot_path = f"{FACE_IMAGE_DIRECTORY}/{image_file_name_without_extension}{FACE_IMAGE_FILE_FORMAT}"
        if os.path.isfile(possible_screenshot_path):
            return True
        else:
            return False

    def find_face(self, img1_path, img2_path):
        found_face_flag = False
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = result["verified"]
        finally:
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
            return

        face_found = self.find_face(reference_frame_file_path, frame_to_compare_file_path)

        if face_found == True:
            self.remove_file_if_exists(frame_to_compare_file_path)
            print("Face Found, Attempts: ", self.counter)
            return
        else:
            self.capture_face_image(video_file_path, image_file_path_without_extension)

    def process(self, input_video_files_list):
        for video_file_path in input_video_files_list:
            image_file_name_without_extension = video_file_path.split("/")[-1].replace(INPUT_VIDEO_FILE_FORMAT, "")
            screenshot_present_flag = self.check_if_screenshot_present(image_file_name_without_extension)
            if not screenshot_present_flag:
                self.counter = 0
                self.capture_face_image(video_file_path, image_file_name_without_extension)
        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()
    input_video_files_list = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    input_video_files_list.sort()
    getframe_obj.process(input_video_files_list)

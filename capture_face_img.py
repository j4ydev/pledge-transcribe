import glob
import os
import random

import cv2
from deepface import DeepFace
from icecream import ic
from numpy.linalg import norm

from config import *


# IMAGE_SAVE_DIRECTORY = "output/screenshots" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
# VIDEO_DIRECTORY = "/Users/khasgiwa/Downloads/GWR/16_20" # PATH OF VIDEO DIRECTORY (DO NOT ADD / AT THE END OF PATH)
# IMAGE_INDEX_DIRECTORY = "output/image_index"
class GETFRAME():

    def __init__(self):
        self.ref_image_path = "ref_image.png"

    def getImageFromVideo(self, video_path):
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

    def check_if_screenshot_present(self, imageFileName):
        possible_screenshot_path = f"{IMAGE_SAVE_DIRECTORY}/{imageFileName}"
        if os.path.isfile(possible_screenshot_path):
            return True
        else:
            return False

    def find_face(self, new_image_path):
        try:
            result, result_2 = DeepFace.verify(img1_path = self.ref_image_path, img2_path = new_image_path)
            foundFaceFlag = True
        except:
            foundFaceFlag = False
            print("face not detected")

        return foundFaceFlag


    def capture_face_image(self, videoFilePath, imageFileName):
        frame = self.getImageFromVideo(videoFilePath)
        frameFilePath = f'{IMAGE_SAVE_DIRECTORY}/{imageFileName}'
        # Save the frame as an image
        print(frameFilePath)
        print("--")
        cv2.imwrite(frameFilePath, frame)

        face_found = self.find_face(frameFilePath)

        if face_found == False:
            face_found = self.capture_face_image(videoFilePath, imageFileName)
        else:
            pass
        return frameFilePath


    def process(self, inputVideoFilesList):
        for videoFilePath in inputVideoFilesList:
            imageFileName = videoFilePath.split("/")[-1].replace(".mp4", ".png")
            screenshot_present_flag = self.check_if_screenshot_present(imageFileName)

            if not screenshot_present_flag:
                self.capture_face_image(videoFilePath, imageFileName)
        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()

    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()
    getframe_obj.process(inputVideoFilesList)

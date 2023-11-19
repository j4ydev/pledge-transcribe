import glob
import os
import random

import cv2
from deepface import DeepFace
from icecream import ic
from numpy.linalg import norm

from config import *  # TODO: Import only needed names or import the module and then use its members. google to know more

SCREENSHOT_FILE_FORMAT = 'png' # TODO: Jay move this to config file and use it from there
VIDEO_FILE_FORMAT = 'mp4' # TODO: Jay move this to config file and use it from there

class GETFRAME():
    def __init__(self):
        self.counter = 0

    def remove_file_if_exists(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

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

    def find_face(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path , img2_path)
            foundFaceFlag = result["verified"]
        except:
            foundFaceFlag = False
        return foundFaceFlag

    def capture_face_image(self, videoFilePath, imageFilePathWithoutExtension):
        referenceFrameFilePath = f'{IMAGE_SAVE_DIRECTORY}/{imageFilePathWithoutExtension}.{SCREENSHOT_FILE_FORMAT}'
        frameToCompareFilePath = f'{IMAGE_SAVE_DIRECTORY}/{imageFilePathWithoutExtension}_2.{SCREENSHOT_FILE_FORMAT}'

        if self.counter == 0:
            print("Attempting to find face in video: ", imageFilePathWithoutExtension)

        self.counter = self.counter + 1

        frameToCompare = self.getImageFromVideo(videoFilePath)
        cv2.imwrite(frameToCompareFilePath, frameToCompare)

        referenceFrame = self.getImageFromVideo(videoFilePath)
        cv2.imwrite(referenceFrameFilePath, referenceFrame)

        if self.counter > 30:
            self.remove_file_if_exists(referenceFrameFilePath)
            self.remove_file_if_exists(frameToCompareFilePath)
            print("No face present in video. Attempts: ", self.counter)
            return

        face_found = self.find_face(referenceFrameFilePath, frameToCompareFilePath)

        if face_found == True:
            self.remove_file_if_exists(frameToCompareFilePath)
            print("Face Found, Attempts: ", self.counter)
            return
        else:
            self.capture_face_image(videoFilePath, referenceFrameFilePath)

    def process(self, inputVideoFilesList):
        for videoFilePath in inputVideoFilesList:
            imageFileName = videoFilePath.split("/")[-1].replace(".mp4", ".png")
            imageFilePathWithoutExtension = imageFileName.replace(".mp4", "")
            screenshot_present_flag = self.check_if_screenshot_present(imageFileName)
            if not screenshot_present_flag:
                self.counter = 0
                self.capture_face_image(videoFilePath, imageFilePathWithoutExtension)
        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()
    getframe_obj.process(inputVideoFilesList)

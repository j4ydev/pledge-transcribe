import glob
import os
import random

import cv2
from deepface import DeepFace
from icecream import ic
from numpy.linalg import norm

from config import *


class GETFRAME():
    def __init__(self):
        self.ref_image_path = "ref_image.png"
        self.counter = 0

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
        return foundFaceFlag

    def capture_face_image(self, videoFilePath, imageFileName):

        if self.counter == 0:
            print("ATTEMPTING TO FIND FACE: ", frameFilePath)

        self.counter = self.counter + 1
        frame = self.getImageFromVideo(videoFilePath)
        frameFilePath = f'{IMAGE_SAVE_DIRECTORY}/{imageFileName}'


        cv2.imwrite(frameFilePath, frame) # Save the frame as an image
        face_found = self.find_face(frameFilePath)

        if self.counter > 30:
            return "NO FACE PRESENT IN VIDEO."

        if face_found == False:
            frameFilePath = self.capture_face_image(videoFilePath, imageFileName)
        else:
            pass
        return frameFilePath

    def process(self, inputVideoFilesList):
        for videoFilePath in inputVideoFilesList:
            imageFileName = videoFilePath.split("/")[-1].replace(".mp4", ".png")
            screenshot_present_flag = self.check_if_screenshot_present(imageFileName)
            if not screenshot_present_flag:
                self.counter = 0
                frameFilePath = self.capture_face_image(videoFilePath, imageFileName)
                print(frameFilePath)
        return "Complete"

if __name__ == "__main__":
    getframe_obj = GETFRAME()
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()
    getframe_obj.process(inputVideoFilesList)

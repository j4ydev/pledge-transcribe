import glob
import random

import cv2
from icecream import ic
from numpy.linalg import norm

IMAGE_SAVE_DIRECTORY = "output/screenshots" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
VIDEO_DIRECTORY = "/Users/khasgiwa/Downloads/GWR/16_20" # PATH OF VIDEO DIRECTORY (DO NOT ADD / AT THE END OF PATH)
IMAGE_INDEX_DIRECTORY = "output/image_index"
class GETFRAME():

    def __init__(self):
        pass

    def getImageFromVideo(self, video_path):
        video_capture = cv2.VideoCapture(video_path)
        total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # try:
        random_frame = random.randint(1, total_frames-5)
        # except:
        #     random_frame = 0

        current_frame = 0

        while True:
            ret, frame = video_capture.read()
            if not ret or current_frame == random_frame:
                break
            current_frame += 1
        if current_frame == random_frame:
            return frame

    def process(self, dir_path, frame_save_dir):
        filesList = glob.glob(f"{dir_path}/*.mp4")
        filesList.sort()

        for videoFilePath in filesList:
            videoFileName = videoFilePath.split("/")[-1].replace(".mp4", ".png")
            # for i in range (0,5):
            frame = self.getImageFromVideo(videoFilePath)
            frame_filename = f'{frame_save_dir}/{videoFileName}'
            # Save the frame as an image
            print(frame_filename)
            print("--")
            cv2.imwrite(frame_filename, frame)


            ### create image_index file
            imageIndexFileName = videoFilePath.split("/")[-1].replace(".mp4", ".txt")
            imageIndexFilePath = f"{IMAGE_INDEX_DIRECTORY}/{imageIndexFileName}"

            with open(imageIndexFilePath, 'w') as f:
                f.write("")


if __name__ == "__main__":

    lowest_diff = 10
    lowest_diff_path = ""
    dir_path = VIDEO_DIRECTORY
    frame_save_dir = IMAGE_SAVE_DIRECTORY
    getframe_obj = GETFRAME()
    getframe_obj.process(dir_path, frame_save_dir)


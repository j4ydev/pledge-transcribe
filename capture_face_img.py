import cv2
from numpy.linalg import norm
import glob
from icecream import ic
import random

class GETFRAME():
    
    def __init__(self):
        pass

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
        
    def process(self, dir_path, frame_save_dir):
        filesList = glob.glob(f"{dir_path}/*.mp4")
        filesList.sort()

        for files in filesList:
            for i in range (0,5):
                frame = self.getImageFromVideo(files)
                frame_filename = f'{frame_save_dir}/{files.split("/")[-1].replace(".mp4", f"_{i}.png")}'
                # Save the frame as an image
                print(frame_filename)
                print("--")
                cv2.imwrite(frame_filename, frame)
        
if __name__ == "__main__":

    lowest_diff = 10
    lowest_diff_path = ""
    dir_path = "/Users/jay/work/transcribe_pledge/all_mp4" # PATH OF VIDEO DIRECTORY (DO NOT ADD / AT THE END OF PATH)
    frame_save_dir = "face_images" # PATH DIR OF SAVE FRAME FROM VIDEO (DO NOT ADD / AT THE END OF PATH)
    getframe_obj = GETFRAME()
    getframe_obj.process(dir_path, frame_save_dir)
    

import glob

from icecream import ic

from capture_face_img import GETFRAME
from config import *
from face_embedding import FACEEMBEDDINGS
from video_transcribe import TRANSCRIBE

transcribe_obj = TRANSCRIBE()
getframe_obj = GETFRAME()
faceembedding_obj = FACEEMBEDDINGS()


### MAIN LOOP ###
def process():
    inputVideoFilesList = glob.glob(f"{INPUT_VIDEO_DIRECTORY}/*.mp4")
    inputVideoFilesList.sort()

    transcribeStatus = transcribe_obj.process(inputVideoFilesList)
    faceCaptureStatus = getframe_obj.process(inputVideoFilesList)

    faceImageFilesList = glob.glob(f"{IMAGE_SAVE_DIRECTORY}/*.png")
    faceImageFilesList.sort()

    getEmbeddingStatus = faceembedding_obj.process(faceImageFilesList)

    ic(transcribeStatus)
    ic(faceCaptureStatus)
    ic(getEmbeddingStatus)

if __name__  == "__main__":
    process()
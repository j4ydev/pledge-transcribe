import glob
import os
from deepface import DeepFace
from config import *
# TODO: extract config directories, clean, refactor
class FACEEMBEDDINGS():
    def __init__(self):
        self.ref_image_path = "ref_image.png"

    def find_face_embedding(self, new_image_path):
        try:
            result, result_2 = DeepFace.verify(img1_path = self.ref_image_path, img2_path = new_image_path)
        except:
            result_2 = "face not detected"
            print("face not detected")
        return result_2

    def check_if_embedding_present(self, imageFileName):
        possible_screenshot_path = f"{IMAGE_INDEX_DIRECTORY}/{imageFileName}"
        if os.path.isfile(possible_screenshot_path):
            return True
        else:
            return False

    def process(self, faceImageFilesList):
        for faceImagesPath in faceImageFilesList:
            imageIndexFileName = faceImagesPath.split("/")[-1].replace(".png", ".txt")
            imageIndexFilePath = f"{IMAGE_INDEX_DIRECTORY}/{imageIndexFileName}"
            embeddingPresentFlag = self.check_if_embedding_present(imageIndexFilePath)
            if embeddingPresentFlag == False:
                result, result_2_embedding_data = DeepFace.verify(img1_path = self.ref_image_path, img2_path = faceImagesPath)
            else:
                print("EMBEDDING ALREADY PRESENT IN DIRECTORY.")
            with open(imageIndexFilePath, 'w') as f:
                f.write(str(result_2_embedding_data))
        return "Complete"


if __name__ == "__main__":
    faceembedding_obj = FACEEMBEDDINGS()
    faceImageFilesList = glob.glob(f"{IMAGE_SAVE_DIRECTORY}/*.png")
    faceImageFilesList.sort()
    faceembedding_obj.process(faceImageFilesList)
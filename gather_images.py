import glob
import pandas as pd
from config import (INSPECT_DATAFRAME_PATH, FACE_CAPTURE_CSV_PATH, FACE_IMAGE_DIRECTORY, 
                    FACE_IMAGE_FILE_FORMAT, MANUAL_FACE_CAPTURE_DIRECTORY, FINAL_FACES_DIRECTORY, 
                    FINAL_FACES_CSV_PATH, MANUAL_FACE_IMAGE_FILE_FORMAT, MANUAL_FACE_IMAGE_FILE_FORMAT)
from utils import get_metadata_from_file_name, is_value_present_in_dataframe
import os
import shutil
from deepface import DeepFace


class GATHERFACES():
    def __init__(self):
        self.capture_face_dataframe = pd.read_csv(FACE_CAPTURE_CSV_PATH)
        self.inspect_dataframe = pd.read_csv(INSPECT_DATAFRAME_PATH)
        self.manually_captured_image_list = glob.glob(f"{MANUAL_FACE_CAPTURE_DIRECTORY}/*{MANUAL_FACE_IMAGE_FILE_FORMAT}")
        self.auto_captured_image_list = glob.glob(f"{FACE_IMAGE_DIRECTORY}/*{FACE_IMAGE_FILE_FORMAT}")
        # self.ledger_dataframe = pd.read_csv(LEDGER_CSV_PATH)

        if os.path.isfile(FINAL_FACES_CSV_PATH):
            try:
                self.final_face_dataframe = pd.read_csv(FINAL_FACES_CSV_PATH)
            except Exception as e:
                print(f"{FINAL_FACES_CSV_PATH} already present.")
                self.final_face_dataframe = pd.DataFrame(columns=['video_id', 'vid_accepted', 'auto_face_found', 'file_gathered', 'face_found'])
        else:
            self.final_face_dataframe = pd.DataFrame(columns=['video_id', 'vid_accepted', 'auto_face_found', 'file_gathered', 'face_found'])


        if not os.path.isdir(FINAL_FACES_DIRECTORY):
            os.makedirs(FINAL_FACES_DIRECTORY)

    def remove_unnecessary_columns(self):
        df = self.inspect_dataframe
        headings = df.columns.tolist()
        # Drop unnecessary columns.
        df.drop(columns=headings[1], inplace=True)
        df.drop(columns=headings[2], inplace=True)
        df.drop(columns=headings[3], inplace=True)
        df.drop(columns=headings[4], inplace=True)
        df.drop(columns=headings[5], inplace=True)
        df.drop(columns=headings[6], inplace=True)
        df.drop(columns=headings[7], inplace=True)
        df.drop(columns=headings[8], inplace=True)
        df.drop(columns=headings[9], inplace=True)
        df.drop(columns=headings[10], inplace=True)
        df.drop(columns=headings[11], inplace=True)
        df.drop(columns=headings[12], inplace=True)
        df.drop(columns=headings[13], inplace=True)
        df.drop(columns=headings[15], inplace=True)
        df.drop(columns=headings[16], inplace=True)
        df.drop(columns=headings[17], inplace=True)

        headings = ['video_id', 'approval']  
        df.columns = headings

        df['approval'].replace('Doubt', 'Reject', inplace=True)
        df['approval'].replace('InvigilationState', 'Reject', inplace=True)
        df['approval'].fillna('Reject', inplace=True)

        return df

    def verify_video_id(self, approval_dataframe, video_id):
        try:
            approval_status = approval_dataframe.loc[approval_dataframe['video_id'] == str(video_id), 'approval'].iloc[0]
            return True
        except:
            print(f"{video_id} not present in approval_dataframe.")
            return False
        
    def verify_face(self, img1_path, img2_path):
        try:
            result = DeepFace.verify(img1_path , img2_path)
            found_face_flag = True
        except Exception as e:
            found_face_flag = False
        return found_face_flag


    def process(self):
        
        approval_dataframe = self.remove_unnecessary_columns()
        for index, row in self.capture_face_dataframe.iterrows():
            video_id = row['video_id']
            is_value_present_flag = is_value_present_in_dataframe(video_id, self.final_face_dataframe)
            
            if self.verify_video_id(approval_dataframe, video_id):
                if not is_value_present_flag:
                    face_found_status = self.capture_face_dataframe.loc[self.capture_face_dataframe['video_id'] == video_id, 'face_found'].iloc[0]
                    approval_status = approval_dataframe.loc[approval_dataframe['video_id'] == str(video_id), 'approval'].iloc[0]
                    # video_file_path = self.ledger_dataframe.loc[self.ledger_dataframe['vid'] == video_id, 'fileName'].iloc[0]
                    
                    #CASE:1
                    if approval_status == "Accept" and face_found_status == True:
                        copy_status = False
                        
                        for image_path in self.auto_captured_image_list:
                            image_name = image_path.split("/")[-1].replace(f"{FACE_IMAGE_FILE_FORMAT}", "")
                            file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)
                            
                            if str(video_id) == str(video_id_):
                                print("-- copying image. --")
                                shutil.copy(image_path , f"{FINAL_FACES_DIRECTORY}/")
                                copy_status = True
                                new_final_face_raw = {'video_id': video_id, 'vid_accepted': True, 'auto_face_found': True, 'file_gathered': True, "face_found": True}
                                new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                                self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                                self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)

                    #CASE:2
                    elif approval_status == "Accept" and face_found_status == False:
                        video_id_found_status = False
                        for image_path in self.manually_captured_image_list:
                            image_name = image_path.split("/")[-1].replace(f"{MANUAL_FACE_IMAGE_FILE_FORMAT}", "")
                            file_bid, video_id_, file_name_suffix = get_metadata_from_file_name(image_name)

                            if str(video_id) == str(video_id_):
                                if self.verify_face(image_path,image_path):
                                    print(f" {video_id} -------------- copying image. --")
                                    shutil.copy(image_path , f"{FINAL_FACES_DIRECTORY}/{image_name}{FACE_IMAGE_FILE_FORMAT}")
                                    video_id_found_status = True

                                    new_final_face_raw = {'video_id': video_id, 'vid_accepted': True, 'auto_face_found': False, 'file_gathered': True, "face_found": True}
                                    new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                                    self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                                    self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)
                                else:
                                    print(f"{video_id} ------- face not found in image. ---")
                                    video_id_found_status = True
                                    new_final_face_raw = {'video_id': video_id, 'vid_accepted': True, 'auto_face_found': False, 'file_gathered': True, "face_found": False}
                                    new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                                    self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                                    self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)

                        if not video_id_found_status:
                            new_final_face_raw = {'video_id': video_id, 'vid_accepted': True, 'auto_face_found': False, 'file_gathered': False, "face_found": False}
                            new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])
                            a = input()
                            print(f"{video_id} videoid not found in manually uploaded face images.")
                    else:
                        # if approval_status == "Reject"
                        continue
                    # self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                    # self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)
            else:
                new_final_face_raw = {'video_id': video_id, 'vid_accepted': False, 'auto_face_found': False, 'file_gathered': False, "face_found": False}
                new_final_face_dataframe = pd.DataFrame(new_final_face_raw, index=[0])

                self.final_face_dataframe = pd.concat([self.final_face_dataframe, new_final_face_dataframe], ignore_index=True)
                self.final_face_dataframe.to_csv(FINAL_FACES_CSV_PATH, index=False)

            
                        

if __name__ == "__main__":
    gather_faces_obj = GATHERFACES()
    gather_faces_obj.process()
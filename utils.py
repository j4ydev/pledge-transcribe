import numpy as np

# TODO: Import only needed names or import the module and then use its members. google to know more
from config import *

USE_OLD_VIDEO_FILE_NAME = False

# current video file name format is 500_6340863312112_naresh_ch.mp4
def get_metadata_from_file_name(file_name):
    file_name_separate_list = file_name.split('_')
    if USE_OLD_VIDEO_FILE_NAME:
        file_bid = "_"
        file_video_id = file_name_separate_list[0]
        file_name_suffix = file_name_separate_list[1]
    else:
        file_bid = file_name_separate_list[0]
        file_video_id = file_name_separate_list[1]
        file_name_suffix = file_name_separate_list[2]
    return file_bid, file_video_id, file_name_suffix

def is_value_present_in_dataframe(file_video_id, dataframe):
    if np.int64(file_video_id) in dataframe['video_id'].values:
        return True
    else:
        return False

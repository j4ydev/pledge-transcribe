    ### GET DETAILS FROM VIDEO FILE NAME ###
import numpy as np


def get_details_from_video_name(file_name):

    file_name_separate_list = file_name.split("_")
    file_row = file_name_separate_list[1]
    file_column = file_name_separate_list[2]
    file_index = 4*(int(file_row)-1) + int(file_column)
    file_pagenumber = file_name_separate_list[0]
    file_video_id = file_name_separate_list[3]

    return file_row, file_column, file_index, file_pagenumber, file_video_id

def is_value_present_in_dataframe(file_video_id, dataframe):

    if np.int64(file_video_id) in dataframe["vid"].values:
        return True
    else:
        return False

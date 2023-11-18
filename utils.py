    ### GET DETAILS FROM VIDEO FILE NAME ###


def get_details_from_video_name(file_name):
    file_name_separate_list = file_name.split("_")
    file_row = file_name_separate_list[1]
    file_column = file_name_separate_list[2]
    file_index = 4*(int(file_row)-1) + int(file_column)
    file_pagenumber = file_name_separate_list[0]
    file_videoid = file_name_separate_list[3]

    return file_row, file_column, file_index, file_pagenumber, file_videoid

def is_value_present_in_dataframe(index_number, dataframe):
    if index_number in dataframe["index"].values:
        return True
    else:
        return False

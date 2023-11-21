# PART - 0
# util function to read file and extract information ( video_id, batch_index, serial_number, page_number, row, column, nid, bid, file_name_suffix, file_type )

# PART-1.1
# 1. for the INPUT_VIDEO_DIRECTORY loop to extract the audio files,
# 2. save the output in the csv file named output/extract_audio_from_video.csv - having columns -- video_id, extract_audio_time, video_duration, audio_duration
# 3. if the video file that we are processing is already processed - skip re processing
# 4 note: do not keep this  audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_file_name}/vocals.mp3"  instead use
#  audio_file_path = f"{BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY}/{video_id}/vocals.mp3"

# PART-1.2
# NOTE: i somewhere read that the audio can be trimmed if there is no voice in start or end, if this will save the transcribe time we should do it - when we do this add one more column named audio_duration after video_duration

# PART-2
# rename transcribe.py to audio_transcription.py and the input to this process will be BACKGROUND_NOISE_REMOVED_AUDIO_DIRECTORY
# do generate a o/p csv it will have the following columns -- video_id, transcribe_time, transcribe_text
# skip the files that were previously processed
# output csv file name will be output/audio_transcription.csv

# sequence of execution PART-0, PART-1.1, # PART-2, # PART-1.2

Script#1 Get Transcribe and Image Indexes

Phase#1 Base RnD

Phase#2
input:: a directory having videos with file name having metadata - `${pageNumber}_${row}_${column}_${video_id}_${name}`
output::

1. A csv with folllowing columns (do not give header) row, column, index, pageNumber, video-id, transcribed text
2. screenshot, create a file (with same file name as video) in directory named screenshot - that will be used in next step
3. image index, create a file (with same file name as video) in directory named image_index - that will be used later

Phase#3 (TBD)
input:: (a csv or a json that is to be looped)

---

Script#2 Identify potential duplicates

Phase#1 Base RnD

Phase#2
input:: a directory image_index having image hash (one file per video)
output:: CSV file - row, column, index, pageNumber, video-id, video-id:similarity_score, video-id:similarity_score, video-id:similarity_score
Note: o/p csv - column 6, 7, 8 will have top 3 matches in form of video-id:similarity_score, where in the 1st match should always be from itself indicating that with self it is matching 100% :-D

Phase#3 (TBD)
input: (a csv or a json that is to be looped)
output: a csv/json

---

Info: `index: 4 * (row - 1) + column`

---

we will create a directory with value of vid as the directory name in "output/similar_pledge_takers"
and in that vid directory we will store 5 files (1 file will be the reference image from the video)
for example if we are processing 1_1_2_6340954574112_Rahul_VP.png
directory name will be 6340954574112
prefix the similarity rank to the file name and store; example the most matching file will be
1-difference_indicator-1_1_2_6340954574112_Rahul_VP.png
where difference_indicator is stringified 1000\*"VGG-Face_cosine" - this should be exact 4 chars, so in case of exact match it will be
1-0000-1_1_2_6340954574112_Rahul_VP.png

6340954574112, 6340954574113:difference_indicator, 6340954574114:difference_indicator,

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

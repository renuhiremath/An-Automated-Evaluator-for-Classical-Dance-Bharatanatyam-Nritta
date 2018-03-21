from UpperBodyDetection import *
from LowerBodyDetection import *
from FaceDetection import *
from video_to_frames_with_db import *

convert_video_to_frames("bhat","videos\\shreya\\d1.mp4","d1",1)
convert_video_to_frames("bhat","videos\\shreya\\dd.mp4","d2",2)
convert_video_to_frames("bhat","videos\\shreya\\d33.mp4","d3",3)
convert_video_to_frames("bhat","videos\\shreya\\d4.mp4","d4",4)
convert_video_to_frames("bhat","videos\\shreya\\d5.mp4","d5",5)

eval_id = 1
face_detect_main(eval_id,"bhat_1_1", "r1")
eval_id = 2
face_detect_main(eval_id,"bhat_2_2", "r2")
eval_id = 3
face_detect_main(eval_id,"bhat_3_3", "r3")
eval_id = 4
face_detect_main(eval_id,"bhat_4_4", "r4")
eval_id = 5
face_detect_main(eval_id,"bhat_5_5", "r5")


eval_id = 3
upperbody_detect_main(eval_id,"r3", "r3")
eval_id = 4
upperbody_detect_main(eval_id,"r4", "r4")
eval_id = 5
upperbody_detect_main(eval_id,"r5", "r5")
eval_id = 1
upperbody_detect_main(eval_id,"r1", "r1")
eval_id = 2
upperbody_detect_main(eval_id,"r2", "r2")

eval_id = 1
lowerbody_detect_main(eval_id,"r1", "r1")
eval_id = 2
lowerbody_detect_main(eval_id,"r2", "r2")
eval_id = 3
lowerbody_detect_main(eval_id,"r3", "r3")
eval_id = 4
lowerbody_detect_main(eval_id,"r4", "r4")
eval_id = 5
lowerbody_detect_main(eval_id,"r5", "r5")
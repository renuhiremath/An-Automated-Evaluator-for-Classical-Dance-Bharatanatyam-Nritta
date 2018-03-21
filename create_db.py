import sqlite3

con = sqlite3.connect("dance_eval.db")
cur = con.cursor()

cur.execute("create table if not exists user_list(eval_id integer primary key autoincrement, user_name text, video_type int)")
cur.execute("create table if not exists image_list(eval_id integer, image_name text, score int)")
#cur.execute("create table if not exists images(eval_id integer, image_name text, original_pic blob, modified_pic blob)")
cur.execute("create table if not exists joint_details_face(eval_id int,image_name text, facex int, facey int,neckx int,necky int)")

cur.execute("create table if not exists joint_details_upperbody(eval_id int,image_name text,shoulder_rightx int,shoulder_righty int, shoulder_leftx int, shoulder_lefty int)")
#cur.execute("drop table joint_details_lowerbody")
cur.execute("create table if not exists if not exists joint_details_lowerbody(eval_id int,image_name text, hip_rightx int, hip_righty int, hip_leftx int, hip_lefty int,knee_rightx int,knee_righty int, knee_leftx int, knee_lefty int)")
cur.execute("create table if not exists upperbody_posture(eval_id int,image_name text, posture_name text)")

print "All tables created.."
con.commit()
con.close()
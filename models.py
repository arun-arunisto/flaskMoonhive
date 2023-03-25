import sqlite3
import hashlib

conn = sqlite3.connect(database='discussion.db', check_same_thread=False)

cur = conn.cursor()

def register_user(username, password):
    encrypted_pass = hashlib.md5(password.encode("utf-8"))
    cur.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{encrypted_pass.hexdigest()}')")
    conn.commit()

def select_user(username, password):
    encrypted_pass = hashlib.md5(password.encode("utf-8"))
    cur.execute(f"SELECT username FROM users where username='{username}' AND password='{encrypted_pass.hexdigest()}'")
    user_data = cur.fetchall()
    print(user_data)
    return user_data

def insert_discussions(username, question, answer):
    cur.execute(f"INSERT INTO discussions (username, question, answer) VALUES ('{username}', '{question}', '{answer}')")
    conn.commit()

def insert_courses(course, image_name):
    cur.execute(f"INSERT INTO courses (course, image) VALUES ('{course}', '{image_name}')")
    conn.commit()

def select_course():
    cur.execute("SELECT * FROM courses")
    data = cur.fetchall()
    return data

def enroll_course(id):
    cur.execute(f"SELECT * FROM courses WHERE id={id}")
    data = cur.fetchall()
    print(data[0])
    cur.execute(f"INSERT INTO enroll_course (courseid, coursename, image, id) VALUES ({data[0][0]}, '{data[0][1]}', '{data[0][2]}', {data[0][0]})")
    conn.commit()

def select_enroll():
    cur.execute("SELECT * FROM enroll_course")
    data = cur.fetchall()
    return data

def select_discussions():
    cur.execute("SELECT * FROM discussions")
    data = cur.fetchall()
    return data

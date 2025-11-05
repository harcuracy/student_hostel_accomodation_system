import sqlite3
import random

DB_PATH = "hostel.db"
HALLS = ["Hall A", "Hall B"]
ROOM_CAPACITY = 4

def create_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            matric_no TEXT UNIQUE,
            hall TEXT,
            room INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def fetch_all_students():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, matric_no, hall, room FROM students ORDER BY hall, room")
    students = c.fetchall()
    conn.close()
    return students

def save_student_to_db(name, matric_no):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check if student already exists
    c.execute("SELECT hall, room FROM students WHERE matric_no=?", (matric_no,))
    existing = c.fetchone()
    if existing:
        conn.close()
        return existing[0], existing[1], False  # hall, room, new=False

    # Allocate hall and room
    allocated = False
    hall, room = None, None

    # Try random halls until a room with space is found
    random_halls = HALLS.copy()
    random.shuffle(random_halls)

    for h in random_halls:
        for r in range(1, 11):  # 10 rooms per hall
            c.execute("SELECT COUNT(*) FROM students WHERE hall=? AND room=?", (h, r))
            count = c.fetchone()[0]
            if count < ROOM_CAPACITY:
                hall, room = h, r
                allocated = True
                break
        if allocated:
            break

    if not allocated:
        conn.close()
        return None, None, False  # hostel full

    # Insert student
    c.execute("INSERT INTO students (name, matric_no, hall, room) VALUES (?, ?, ?, ?)",
              (name, matric_no, hall, room))
    conn.commit()
    conn.close()
    return hall, room, True


if __name__ == "__main__":
    create_table()
    print("✅ Database initialized successfully!")

import cv2
import threading
import time

import sqlconnectivity
import studentracking
from simple_facerec import SimpleFacerec

# Part 1 - Define functions for adding and deleting entries from person_dict
person_dict = {}


def add_person_data(fname, result):
    if results is None or not result:
        return
    division, mobile, year = result[0][5], result[0][6], result[0][4]
    current_timee = time.time()
    if fname in person_dict:
        # Update time if person already exists in dictionary
        person_dict[fname] = (division, mobile, year, current_timee)
    else:
        # Add new person to dictionary with current time
        person_dict[fname] = (division, mobile, year, current_timee)
        studentracking.insert_student_record(fname, year, division, mobile)


def delete_old_entries():
    curren_time = time.time()
    # Iterate over a copy of the dictionary keys to avoid "dictionary changed size during iteration" error
    for name in list(person_dict.keys()):
        data = person_dict[name]
        # Check if person was added more than 10 minutes ago
        if curren_time - data[3] > 600:  # 10 minutes in seconds
            del person_dict[name]


def run_delete_old_entries():
    # Run the delete_old_entries() function every 10 minutes
    while True:
        delete_old_entries()
        time.sleep(600)  # 10 minutes in seconds


# Start a separate thread to run delete_old_entries() function
delete_thread = threading.Thread(target=run_delete_old_entries)
delete_thread.start()

# Part 2 - Detect faces and add new people to person_dict
# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

# Set the threshold time for removal (in minutes)
threshold_time = 15
current_time = time.time()

while True:
    ret, frame = cap.read()

    # Delete old entries from person_dict
    if current_time - time.time() > 900:  # 15 minutes in seconds
        delete_old_entries()
        current_time = time.time()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        results = sqlconnectivity.get_student_details(name)
        fullname = (results[0][1])+(results[0][3])
        add_person_data(fullname, results)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

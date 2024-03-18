import numpy
from datetime import datetime
import cv2
import face_recognition
import csv
import cmake


video_capture = cv2.VideoCapture(0)

# Load known faces
dom_image =  face_recognition.load_image_file("faces/sharuk.jpeg")
dom_encoding = face_recognition.face_encodings(dom_image)[0]

kittu_image =  face_recognition.load_image_file("faces/salmaan.jpeg")
kittu_encoding = face_recognition.face_encodings(kittu_image)[0]

known_face_encodings =[dom_encoding,kittu_encoding]
known_faces_names =["Sharuk","salmaan"]
# list of expected students
students = known_faces_names.copy()

face_locations = []
face_encodings = []

# get the current date
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

f= open(f"{current_date}.csv","w+",newline="")
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)

    # Recognise the faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
    for face_encoding in face_encodings:
        matchs = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = numpy.argmin(face_distance)

        name = "Unknown"
        if (matchs[best_match_index]):
            name = known_faces_names[best_match_index]

        # adding text to a person
        if name in known_faces_names:
            font = cv2.FONT_HERSHEY_SIMPLEX
            bottomLeftCornerOfText = (10, 100)
            fontScale = 1.5
            fontColor = (255, 0, 0)
            thickness = 3
            lineType = 2
            cv2.putText(frame, name + "Present", bottomLeftCornerOfText, font, fontScale, fontColor, thickness,
                        lineType)
            if name in students:
                students.remove(name)  # remove the recognized student from the list

    cv2.imshow("Attendance", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Write present students to CSV file
    for student in known_faces_names:
        if student in students:
            lnwriter.writerow([student, "ABSENT"])
        else:
            lnwriter.writerow([student, "PRESENT"])

video_capture.release()
cv2.destroyAllWindows()
f.close()























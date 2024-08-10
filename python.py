import os
import cv2
import face_recognition
from tkinter import Tk, Label, Button, filedialog, simpledialog

known_criminals_folder = "C:\\Users\\pc\\Desktop\\face-Recog\\images"
known_encodings = []
known_names = []
flag = 0

def load_known_criminals():
    for file_name in os.listdir(known_criminals_folder):
        image_path = os.path.join(known_criminals_folder, file_name)
        name = os.path.splitext(file_name)[0]
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_names.append(name)

def match_criminal():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            flag = 1
            if True in matches:
                matched_indices = [index for index, match in enumerate(matches) if match]
                first_match_index = matched_indices[0]
                name = known_names[first_match_index]
                flag = 0
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (237, 255, 32), 2)
            if flag == 0:
                cv2.putText(frame, "Matched Criminal: "+name, (left-40, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (158, 49, 255), 2)
            else:
                cv2.putText(frame, "Not Matched", (left, top - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 37), 2)
            match_label.config(text="Matched Criminal: " + name)
        cv2.imshow('TechVidvan', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def add_criminal():
    file_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                           filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
    if file_path:
        image = cv2.imread(file_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        encoding = face_recognition.face_encodings(rgb_image)[0]
        name = simpledialog.askstring("Add Criminal", "Enter the name of the criminal:")
        if name:
            known_encodings.append(encoding)
            known_names.append(name)
            file_name = name + ".jpg"
            save_path = os.path.join(known_criminals_folder, file_name)
            cv2.imwrite(save_path, image)
            print("Criminal added successfully.")

load_known_criminals()

root = Tk()
root.title("Criminal Identification System")
root.geometry("500x300")

label = Label(root, text="Welcome to the Criminal Identification System by TechVidvan")
label.pack()

match_button = Button(root, text="Match Criminal", command=match_criminal)
match_button.pack()
add_button = Button(root, text="Add Criminal", command=add_criminal)
add_button.pack()
match_label = Label(root, text="Matched Criminal: ")
match_label.pack()
root.mainloop()
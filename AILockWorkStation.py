import face_recognition
import cv2
import numpy as np
import ctypes
import platform
import os
from time import time, sleep

class AILockWorkStation:
    """Facial recognition AI in Python to lock your screen when you're not in front of it
    """
    def __init__(self) -> None:
        self.known_face_encodings: list = []
        self.known_face_names: list = []
        self.directory: str = "./known_people/"
        self.current_os = platform.system()
        self.lock: bool = True


    def run(self, time_to_wait: int = 5) -> None:
        """_summary_

        Args:
            time_to_wait (int, optional): time to wait before checking if we need to lock the work station. (Defaults to 5)
        """
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        
        self.load_known_person()
        
        # Initialize some variables
        face_locations: list = []
        face_names: list = []
        process_this_frame: bool = True
        start_time: float = time()
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            
            # Only process every other frame of video to save time
            if process_this_frame:
               face_locations, face_names = self.process_frame(frame)
               
            process_this_frame = not process_this_frame

            self.display_result(face_locations, face_names, frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if self.to_be_locked(start_time, time_to_wait):
                break
            

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


    def load_known_person(self) -> None:
        """Create arrays of known face encodings and their names
        """
        train_dir = os.listdir(self.directory)
        # https://www.geeksforgeeks.org/python-multiple-face-recognition-using-dlib/#
        for person in train_dir:
            pix = os.listdir(self.directory + person)

            for person_img in pix:
                face = face_recognition.load_image_file(self.directory + person + "/" + person_img)
                face_bounding_boxes = face_recognition.face_encodings(face)

                if len(face_bounding_boxes) == 1:
                    self.known_face_encodings.append(face_bounding_boxes[0])
                    self.known_face_names.append(person)
                else:
                    print(f"{person}/{person_img} can't be used for training")
                    
                    
    def process_frame(self, frame) -> tuple[list, list]:
        """Process the current frame to extract information

        Args:
            frame (_type_): current frame
            face_locations (list): List of all the face locations on the current frame
            face_encodings (list): List of all the face encoding on the current frame
            
        Returns:
            tuple[list, list]: return the face_locations and face_names list
        """
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        #https://stackoverflow.com/questions/75926662/face-recognition-problem-with-face-encodings-function
        rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        # Find all the faces and face encodings in the current frame of video
        face_locations: list = face_recognition.face_locations(rgb_small_frame)
        face_encodings: list = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names: list = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            face_names.append(name)
        
        return face_locations, face_names
        


    def display_result(self, face_locations: list, face_names: list, frame) -> None:
        """_summary_

        Args:
            face_locations (list): List of all the face locations in the current frame
            face_names (list): List of all the names in the current frame
            frame (_type_): Current france
        """
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if name in self.known_face_names:
                self.lock = False

        # Display the resulting image
        cv2.imshow('Video', frame)


    def to_be_locked(self, start_time: float, time_to_wait: int) -> bool:
        """Check if the person allow in front of the computer have been present in the last X seconds

        Args:
            start_time (float): Time at the start of the script
            time_to_wait (int): Time to wait to check if we need to lock the screen

        Returns:
            bool: Define if we should stop the script, after locking the screen
        """
        current_time: float = round(time() - start_time, 1)
        print(current_time, self.lock)
        if current_time % time_to_wait == 0 and current_time != 0.0:
            if self.lock:
                if self.current_os == 'Windows':
                    ctypes.windll.user32.LockWorkStation()
                elif self.current_os == 'Darwin':  # macOS
                    os.system('osascript -e "tell application \\"System Events\\" to keystroke \\"q\\" using {control down, command down}"')
                elif self.current_os == 'Linux':
                    desktop_environment = os.environ.get('DESKTOP_SESSION')
                    if desktop_environment in ['gnome', 'ubuntu']:  # GNOME desktop environment
                        os.system('xdg-screensaver lock')
                    elif desktop_environment == 'kde':  # KDE Plasma desktop environment
                        os.system('loginctl lock-session')
                    else:  # Other Linux desktop environments (e.g., XScreenSaver)
                        os.system('xscreensaver-command -lock')
                else:
                    print('Screen locking is not supported on this operating system.')
                return True
            self.lock = True
            sleep(0.1) # Fix the problem when we go have multiple frame in 5X.0s

        return False

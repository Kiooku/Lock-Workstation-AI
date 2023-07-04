# Lock Workstation AI

## What is that?!

> **Warning** Work in progress but you can try it *(see the [TODO](#todo) section for more information)*

It's a facial recognition AI in Python to lock your screen when you're not in front of it.

The script recognizes your face and lock it if you're not in front of your screen for more than X seconds *(default: 5 seconds)*.

## Getting Started

Python library to install:
- [face-recognition](https://pypi.org/project/face-recognition/).
- [numpy](https://numpy.org/install/)
- [OpenCV](https://pypi.org/project/opencv-python/)

In the `known_people` folder, create a folder for each person you want to register. In each of these sub-folders, add as many images as you want (1 may be enough) of the same person.

> **Note** You can look at the example with the **MrBean** folder

You can now run the project using the command: `python3 main.py`.

## How it works?

**OpenCV** is used for the face detection, then **face-recognition** allow to identify the person on the video.

If no known person *(persons registered in the script database)* is present in front of the screen for 5 seconds, the script automatically locks the workstation.

## TODO

- Improve face detection
    - Side View
    - Face detection on dark video
- Improve face recognition
    - Multithreading
    - Detect when it's a picture and not a real person
- Add GUI to make the application more user friendly

## Ressources

- [Face-recognition](https://pypi.org/project/face-recognition/)

- [Face-recognition GitHub](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py)

- [Python multiple face recognition using dlib](https://www.geeksforgeeks.org/python-multiple-face-recognition-using-dlib/#)

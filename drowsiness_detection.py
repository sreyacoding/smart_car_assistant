import cv2
import dlib
import pygame
import numpy as np

# Initialize pygame mixer for sound
pygame.mixer.init()
pygame.mixer.music.load('Alarm.mp3')  

# Load the face detector and shape predictor
svm_detector = dlib.get_frontal_face_detector()
svm_predictor_path = 'shape_predictor_68_face_landmarks.dat' 
svm_predictor = dlib.shape_predictor(svm_predictor_path)

# Define the facial landmarks indices for eyes
(lStart, lEnd) = (36, 42)  # Left eye landmarks
(rStart, rEnd) = (42, 48)  # Right eye landmarks

# Function to calculate the eye aspect ratio
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Start monitoring function
def start_monitoring():
    drowsy = False
    alarm_playing = False
    
    # Start the camera feed
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = svm_detector(gray, 0)

        for rect in rects:
            shape = svm_predictor(gray, rect)
            shape = np.array([[p.x, p.y] for p in shape.parts()])

            # Extract the left and right eye landmarks
            left_eye = shape[lStart:lEnd]
            right_eye = shape[rStart:rEnd]

            # Calculate the eye aspect ratio for both eyes
            left_ear = eye_aspect_ratio(left_eye)
            right_ear = eye_aspect_ratio(right_eye)

            # Average the two eye aspect ratios
            ear = (left_ear + right_ear) / 2.0

            # Check for drowsiness
            if ear < 0.25:  # Adjust this threshold as needed
                drowsy = True
                if not alarm_playing:
                    pygame.mixer.music.play(-1)  # Play alarm indefinitely
                    alarm_playing = True
                    print("Drowsy detected! Alarm is playing.")
            else:
                drowsy = False
                if alarm_playing:
                    pygame.mixer.music.stop()  # Stop the alarm
                    alarm_playing = False
                    print("Awake detected! Alarm stopped.")

            # Draw landmarks on the frame
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # Display the camera feed
        cv2.putText(frame, "Drowsy" if drowsy else "Awake", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up
    video_capture.release()
    cv2.destroyAllWindows()

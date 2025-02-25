import random
import cv2
from deepface import DeepFace
import json
from datetime import datetime, timedelta
import os

def capture_emotion():
    # Initialize the video capture
    video_capture = cv2.VideoCapture(0)  # 0 usually refers to the default webcam

    # Check if the webcam opened successfully
    if not video_capture.isOpened():
        print("Error: Could not open video capture device.")
        return None

    detected_emotion = None
    last_detection_time = datetime.min

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            current_time = datetime.now()
            if current_time - last_detection_time >= timedelta(seconds=30):
                last_detection_time = current_time  # Update the last detection time

                # Detect faces and analyze emotions
                try:
                    analysis = DeepFace.analyze(frame, actions=['emotion'])
                    detected_emotion = analysis[0]['dominant_emotion']  # Access the first element of the list
                    print(f"Detected Emotion: {detected_emotion}")

                    # Display the resulting frame (optional)
                    cv2.putText(frame, detected_emotion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Video', frame)

                    # Write the detected emotion to the JSON file
                    emotion_data = {
                        "id": random.randint(1, 1000000),
                        "date_time": current_time.isoformat(),
                        "detected_emotion": detected_emotion
                    }
                    file_path = 'emotion_result.json'
                    if os.path.exists(file_path):
                        with open(file_path, 'r+') as file:
                            try:
                                data = json.load(file)
                            except json.JSONDecodeError:
                                data = []
                            data.append(emotion_data)
                            file.seek(0)
                            json.dump(data, file, indent=4)
                    else:
                        with open(file_path, 'w') as file:
                            json.dump([emotion_data], file, indent=4)

                except Exception as e:
                    print(f"Error during emotion analysis: {e}")
                    # Handle cases where no face is detected or other errors

            # Exit if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        # Release the video capture and destroy windows
        video_capture.release()
        cv2.destroyAllWindows()

    return detected_emotion

if __name__ == "__main__":
    # Specify the full path, including the directory
    file_path = os.path.join("./", "emotion_result.json")  # Replace with your desired path
    directory = os.path.dirname(file_path) # Extract the directory path

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f"Directory '{directory}' created successfully.")
        except OSError as e:
            print(f"Error creating directory '{directory}': {e}")
            exit()  # Exit the script if directory creation fails

    capture_emotion()

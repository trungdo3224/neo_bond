from fer import FER
import cv2
import asyncio
import time
from utils import draw_rectangle, write_emotion_to_file

async def process_frame(detector, frame):
    result = detector.detect_emotions(frame)
    if result:
        for face in result:
            box = face['box']
            emotions = face['emotions']
            dominant_emotion = max(emotions, key=emotions.get)
            emotion_score = emotions[dominant_emotion]
            draw_rectangle(frame, box)
            write_emotion_to_file(dominant_emotion, emotion_score)
            text = f"{dominant_emotion}: {emotion_score:.2f}"
            cv2.putText(frame, text, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

async def main():
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        await process_frame(detector, frame)
        cv2.imshow('Real-Time Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
def draw_rectangle(frame, box):
    x, y, w, h = box
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

def write_emotion_to_file(dominant_emotion, emotion_score):
    with open('emotion.txt', 'a+') as f:
        f.writelines(f"Detected {dominant_emotion}: {emotion_score:.2f}\nTime: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
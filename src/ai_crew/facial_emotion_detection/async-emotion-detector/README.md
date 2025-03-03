# async-emotion-detector/async-emotion-detector/README.md

# Async Emotion Detector

This project implements a real-time emotion detection system using asynchronous programming in Python. It captures video frames from a webcam, processes them in parallel to detect emotions, and displays the results in real-time.

## Project Structure

```
async-emotion-detector
├── src
│   ├── main.py          # Entry point of the application
│   ├── detector.py      # Contains the EmotionDetector class
│   └── utils.py         # Utility functions for drawing and logging
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd async-emotion-detector
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:

```
python src/main.py
```

This will start the webcam feed and begin detecting emotions in real-time. The detected emotions will be displayed on the video feed and logged to a text file.

## Emotion Detection Functionality

The application uses the `FER` library for emotion detection, which identifies emotions such as happiness, sadness, anger, surprise, and more. The detected emotions are processed asynchronously to ensure smooth performance and responsiveness.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
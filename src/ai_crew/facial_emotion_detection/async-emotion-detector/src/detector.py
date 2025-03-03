class EmotionDetector:
    def __init__(self, detector):
        self.detector = detector

    async def detect_emotions(self, frame):
        return self.detector.detect_emotions(frame)

    async def process_frame(self, frame):
        result = await self.detect_emotions(frame)
        return result
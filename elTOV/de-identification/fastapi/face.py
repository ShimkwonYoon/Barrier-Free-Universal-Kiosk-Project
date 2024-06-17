from ultralytics import YOLO
import cv2
import numpy as np
import mediapipe as mp


# model

class FaceBlur:
    def __init__(self):
        self.model = YOLO("./yolov8n-face.pt")
        # self.model = mp.solutions.face_detection.FaceDetection(
        #     min_detection_confidence=0.2)

    def blur(self, image):

        mat = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.model(mat, verbose=False)
        # coordinates
        for r in results:
            boxes = r.boxes

            for box in boxes:
                # bounding box
                weight = 15
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1) - weight, int(y1) - weight, int(x2) + \
                    weight, int(y2) + weight  # convert to int values
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 0), -1)
            return image

    def pipe_blur(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model.process(rgb_frame)
        frame_height, frame_width, c = frame.shape
        if results.detections:
            for face in results.detections:
                face_react = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height]).astype(int)

                cv2.rectangle(frame, face_react, (0, 0, 0), -1)
        return frame

from ultralytics import YOLO
import cv2

class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        # COCO classes for traffic light (9) and stop sign (11)
        # We can add more if needed.
        self.target_classes = [9, 11] 

    def detect(self, frame):
        """
        Detects objects in the frame.
        Returns a list of detections: [(x1, y1, x2, y2, class_id, conf), ...]
        """
        results = self.model(frame, verbose=False)
        detections = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                if cls_id in self.target_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    detections.append((x1, y1, x2, y2, cls_id, conf))
        
        return detections

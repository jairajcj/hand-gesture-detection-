import cv2
import numpy as np
from detector import ObjectDetector
from correction import ColorCorrector

def main():
    print("Initializing CBSF (Optimized)...")
    
    try:
        # Load detector with nano model for speed/memory
        detector = ObjectDetector()
        corrector = ColorCorrector()
        print("Modules loaded.")
    except Exception as e:
        print(f"Error: {e}")
        return

    cap = cv2.VideoCapture(0)
    # [OPTIMIZATION] Force 640x480 resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("Error: Webcam not found.")
        return

    print("Press 'q' to quit.")

    # [OPTIMIZATION] Frame skipping variables
    frame_count = 0
    SKIP_FRAMES = 5
    current_detections = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # [OPTIMIZATION] Run detection only every N frames
        if frame_count % SKIP_FRAMES == 0:
            current_detections = detector.detect(frame)
        
        frame_count += 1

        # Process detections (reuse same detections for skipped frames)
        for (x1, y1, x2, y2, cls_id, conf) in current_detections:
            # Ensure coordinates are within frame bounds
            h, w = frame.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            roi = frame[y1:y2, x1:x2]
            if roi.size > 0:
                # Apply correction
                corrected_roi = corrector.apply_correction(roi)
                frame[y1:y2, x1:x2] = corrected_roi

                # Draw UI
                label = f"{detector.model.names[cls_id]}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.imshow('CBSF Optimized', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

import os
import cv2
from ultralytics import YOLO

class PPEDetector:
    def __init__(self, model_path="models/ppe_yolov8n.pt"):
        if not os.path.exists(model_path):
            model_path = "yolov8s.pt"
            
        self.model = YOLO(model_path)
        self.target_classes = self.model.names

    def detect_and_annotate(self, image_path, output_path="output.jpg", conf_threshold=0.40):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Cannot load image from {image_path}")

        results = self.model.predict(source=image, conf=conf_threshold)[0]
        
        detected_items = []
        violations = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = self.target_classes[cls_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detected_items.append(label)

            # หากขึ้นต้นด้วย no_ ให้ถือเป็นการละเมิด (สีแดง) นอกนั้นเป็นสีเขียว
            if label.startswith("no_"):
                color = (0, 0, 255) # สีแดง (BGR)
                violations.append(label)
            else:
                color = (0, 255, 0) # สีเขียว (BGR)

            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            cv2.putText(image, f"{label} {conf:.2f}", (x1, max(y1 - 10, 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.imwrite(output_path, image)
        
        status = "NON-COMPLIANT" if len(violations) > 0 else "COMPLIANT"

        return {
            "status": status,
            "detected_items": detected_items,
            "violations": violations,
            "output_saved_at": output_path
        }

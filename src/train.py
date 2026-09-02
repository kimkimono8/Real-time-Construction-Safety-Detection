from ultralytics import YOLO

def train_local_model():
    print("Loading YOLOv8 Nano model...")
    # โหลดโมเดลขนาดเล็กที่สุดเพื่อให้รันบนโน้ตบุ๊กไหว
    model = YOLO('yolov8n.pt')[cite: 1]

    print("Starting training process on CPU...")
    # ทดสอบเทรนแค่ 10 Epochs ก่อนเพื่อดูว่าเครื่องไหวและใช้เวลาเท่าไหร่
    results = model.train(
        data='data/ppe_dataset/data.yaml', 
        epochs=10, 
        imgsz=640, 
        device='cpu'
    )[cite: 1]

    print("Training completed!")

if __name__ == "__main__":
    train_local_model()

import os
from dotenv import load_dotenv
from roboflow import Roboflow

# โหลดตัวแปรสภาพแวดล้อมจากไฟล์ .env (เพื่อซ่อน API Key)
load_dotenv()

def download_ppe_dataset():
    api_key = os.getenv("ROBOFLOW_API_KEY")
    if not api_key:
        raise ValueError("Please set ROBOFLOW_API_KEY in your .env file")
    
    print("Downloading Construction Safety PPE Dataset...")
    
    # เชื่อมต่อผ่าน API
    rf = Roboflow(api_key=api_key)
    # สมมติอ้างอิงโปรเจกต์ PPE Detection พื้นฐานจาก Roboflow Universe 
    project = rf.workspace("ross-currie").project("assignment_2_q3_robotics")
    
    # ดาวน์โหลดชุดข้อมูลในรูปแบบ YOLOv8 ไปเก็บไว้ในโฟลเดอร์ data/
    dataset = project.version(2).download("yolov8", location="./data/ppe_dataset")
    print(f"Dataset successfully downloaded to: {dataset.location}")

if __name__ == "__main__":
    download_ppe_dataset()

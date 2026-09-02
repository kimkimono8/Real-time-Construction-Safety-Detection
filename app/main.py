import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.schemas import ComplianceResponse
from src.detector import PPEDetector

app = FastAPI(
    title="Construction Safety PPE Compliance API",
    description="REST API สำหรับตรวจจับการสวมใส่อุปกรณ์ PPE (หมวกนิรภัย, เสื้อกั๊ก) แบบ Real-time",
    version="1.0.0"
)

# โหลด Detector Model ขึ้น Memory ครั้งเดียวตอนรัน Server
detector = PPEDetector(model_path="models/ppe_yolov8n.pt")

@app.get("/health")
def health_check():
    """ตรวจสอบสถานะความพร้อมของ API Server"""
    return {"status": "healthy", "service": "PPE Detection API"}

@app.post("/predict", response_model=ComplianceResponse)
async def predict_compliance(file: UploadFile = File(...), conf_threshold: float = 0.25):
    """
    รับไฟล์ภาพและคืนค่าสถานะการสวมใส่อุปกรณ์ความปลอดภัย (COMPLIANT / NON-COMPLIANT)
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="ไฟล์ที่อัปโหลดต้องเป็นรูปภาพเท่านั้น (.jpg, .png)")

    temp_input = f"temp_api_{file.filename}"
    temp_output = f"output_api_{file.filename}"

    try:
        # บันทึกไฟล์ภาพชั่วคราว
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # ส่งภาพเข้า Inference Pipeline
        result = detector.detect_and_annotate(
            image_path=temp_input,
            output_path=temp_output,
            conf_threshold=conf_threshold
        )

        detected_items = result["detected_items"]
        status = result["status"]
        message = (
            "สวมใส่อุปกรณ์ความปลอดภัยถูกต้อง"
            if status == "COMPLIANT"
            else "ตรวจพบการละเมิดกฎความปลอดภัย (ไม่พบหมวกนิรภัย)"
        )

        return ComplianceResponse(
            status=status,
            total_detected=len(detected_items),
            detected_items=detected_items,
            message=message
        )

    finally:
        # ลบไฟล์ภาพชั่วคราว
        if os.path.exists(temp_input):
            os.remove(temp_input)
        if os.path.exists(temp_output):
            os.remove(temp_output)

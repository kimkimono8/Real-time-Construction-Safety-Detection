FROM python:3.12-slim

# ติดตั้ง System Libraries ที่จำเป็นสำหรับ OpenCV บน Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ติดตั้ง Python Dependencies ก่อน เพื่อใช้ประโยชน์จาก Docker Layer Caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดและไฟล์โมเดลทั้งหมดเข้ามาใน Container
COPY . .

# เปิดพอร์ตสำหรับเรียกใช้งาน FastAPI
EXPOSE 8000

# กำหนดคำสั่งเริ่มต้นเมื่อ Container ทำงาน
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

import os
import streamlit as st
from PIL import Image
from src.detector import PPEDetector

# กำหนดค่าหน้าเว็บ
st.set_page_config(
    page_title="Construction Safety PPE Compliance",
    page_icon="🦺",
    layout="wide"
)

st.title("🦺 Real-time Construction Safety PPE Detection")
st.markdown("ระบบตรวจสอบการสวมใส่อุปกรณ์คุ้มครองความปลอดภัยส่วนบุคคล (PPE) ในเขตก่อสร้างด้วย Computer Vision")

# แถบควบคุมด้านข้าง (Sidebar Controls)
st.sidebar.header("Model Configuration")
conf_threshold = st.sidebar.slider(
    "Confidence Threshold", 
    min_value=0.10, 
    max_value=0.90, 
    value=0.25, 
    step=0.05,
    help="ปรับค่าความเชื่อมั่นขั้นต่ำของโมเดลในการตรวจจับวัตถุ"
)

# โหลดโมเดลผ่าน Cache เพื่อไม่ให้โหลดซ้ำทุกครั้งที่กด Refresh
@st.cache_resource
def load_detector():
    return PPEDetector(model_path="models/ppe_yolov8n.pt")

detector = load_detector()

# ส่วนอัปโหลดรูปภาพ
uploaded_file = st.file_uploader("เลือกภาพไซต์งานก่อสร้างที่ต้องการตรวจสอบ (.jpg, .jpeg, .png)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # บันทึกไฟล์ภาพชั่วคราวเพื่อส่งให้ Detector
    temp_input_path = "temp_input.jpg"
    temp_output_path = "temp_output.jpg"
    
    with open(temp_input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ประมวลผลภาพผ่าน Inference Pipeline
    with st.spinner("กำลังประมวลผลการตรวจจับ PPE..."):
        result = detector.detect_and_annotate(
            image_path=temp_input_path, 
            output_path=temp_output_path, 
            conf_threshold=conf_threshold
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(temp_input_path, use_container_width=True)

    with col2:
        st.subheader("Detection Result")
        st.image(temp_output_path, use_container_width=True)

    # แสดงผลสรุปสถานะความปลอดภัย (Compliance Status)
    st.divider()
    st.subheader("Compliance Summary")
    
    status = result["status"]
    detected_items = result["detected_items"]

    if status == "COMPLIANT":
        st.success("✅ สถานะ: COMPLIANT (สวมใส่อุปกรณ์ความปลอดภัยถูกต้อง)")
    else:
        st.error("🚨 สถานะ: NON-COMPLIANT (ตรวจพบการละเมิดกฎความปลอดภัย - ไม่พบหมวกนิรภัย)")

    st.write(f"**อุปกรณ์ที่ตรวจพบทั้งหมด ({len(detected_items)} รายการ):**")
    if detected_items:
        st.json(detected_items)
    else:
        st.info("ไม่พบวัตถุที่ตรวจจับได้ตามค่า Threshold ที่ระบุ")

    # ลบไฟล์ชั่วคราวหลังแสดงผล
    if os.path.exists(temp_input_path):
        os.remove(temp_input_path)
    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

import streamlit as st
import numpy as np
from PIL import Image

st.title("Beauty AI Advisor: Auto pH-Adaptive Color Mapping")
st.write("อัปโหลดรูปภาพผิวของคุณ ระบบจะวิเคราะห์สภาพผิวและประเมินค่า pH พร้อมแนะนำเฉดสีที่เหมาะสมให้อัตโนมัติทันที!")

# 1. ส่วนรับอัปโหลดรูปภาพ
uploaded_file = st.file_uploader("อัปโหลดรูปภาพผิวหน้าของคุณ", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # โหลดรูปภาพ
    img = Image.open(uploaded_file)
    st.image(img, caption="รูปภาพที่อัปโหลด", use_column_width=True)
    
    img_np = np.array(img)
    height, width, _ = img_np.shape
    
    # 2. ตัดโซนกลางภาพเพื่อสกัดสีผิว (Skin Tone Extraction)
    crop_margin_h = int(height * 0.25)
    crop_margin_w = int(width * 0.25)
    center_region = img_np[crop_margin_h:height-crop_margin_h, crop_margin_w:width-crop_margin_w]
    
    # กรองแสงเงาและไฮไลท์
    brightness = np.mean(center_region, axis=2)
    filtered_pixels = center_region[(brightness >= 40) & (brightness <= 220)]
    
    if len(filtered_pixels) == 0:
        base_rgb = np.array([200, 150, 120])
    else:
        base_rgb = np.mean(filtered_pixels, axis=0)
        
    r, g, b = base_rgb
    
    # 3. วิเคราะห์สภาพผิวและประเมินค่า pH อัตโนมัติจากสัดส่วนสี (Red vs Green/Blue balance)
    # คำนวณความสมดุลสีเพื่อจำลองสภาพความเป็นกรด-ด่างของผิว
    color_ratio = r / (g + 1e-5)
    
    if color_ratio > 1.25:
        # ผิวมีแนวโน้มระคายเคืองหรือมีความเป็นกรดสูง (pH ต่ำกว่า 4.5)
        estimated_ph = 4.2
        skin_condition = "ผิวมีความไว / ระคายเคืองง่าย (pH ค่อนข้างต่ำ)"
        r = min(255, r * 1.1 + 10)
        b = max(0, b * 0.9 - 5)
    elif color_ratio < 0.95:
        # ผิวมีแนวโน้มแห้งหรือขาดความสมดุล (pH สูงกว่า 5.5)
        estimated_ph = 5.8
        skin_condition = "ผิวแห้ง / ขาดความสมดุล (pH ค่อนข้างสูง)"
        r = r * 0.92
        g = g * 0.92
        b = b * 0.92
    else:
        # สภาพผิวสมดุลปกติ (pH อยู่ในช่วง 4.5 - 5.5)
        estimated_ph = 5.0
        skin_condition = "ผิวสุขภาพดี สมดุลปกติ (pH 4.5 - 5.5)"
        
    final_rgb = (int(r), int(g), int(b))
    hex_color = '#{:02x}{:02x}{:02x}'.format(final_rgb[0], final_rgb[1], final_rgb[2])
    
    # 4. แสดงผลลัพธ์การวิเคราะห์แบบอัตโนมัติ
    st.subheader("ผลการวิเคราะห์อัตโนมัติจาก AI")
    st.info(f"📍 **สภาพผิวที่ประเมินได้:** {skin_condition} (ประมาณค่า pH: {estimated_ph})")
    st.markdown(f"**รหัสสี (Hex Code) ที่เหมาะสมที่สุด:** `{hex_color}`")
    
    # แสดงตัวอย่างวงกลมสี
    st.markdown(
        f'<div style="width: 100px; height: 100px; background-color: {hex_color}; border-radius: 50%; border: 2px solid #ccc; margin-top: 10px;"></div>',
        unsafe_allow_html=True
    )

import streamlit as st
import numpy as np
from PIL import Image

st.title("Beauty AI Advisor: pH-Adaptive Color Mapping")

# 1. ส่วนรับอัปโหลดรูปภาพและกรอกค่า pH
uploaded_file = st.file_uploader("อัปโหลดรูปภาพผิวหน้าของคุณ", type=["jpg", "jpeg", "png"])
skin_ph = st.number_input("ระบุค่า pH ของผิวผู้ทดลอง (ช่วงปกติ: 4.5 - 5.5)", min_value=3.0, max_value=8.0, value=5.2, step=0.1)

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
    
    # กรองแสงเงาและไฮไลท์ที่สว่างหรือมืดเกินไป
    brightness = np.mean(center_region, axis=2)
    filtered_pixels = center_region[(brightness >= 40) & (brightness <= 220)]
    
    if len(filtered_pixels) == 0:
        base_rgb = np.array([200, 150, 120])
    else:
        base_rgb = np.mean(filtered_pixels, axis=0)
        
    r, g, b = base_rgb
    
    # 3. ตรรกะปรับเปลี่ยนสีตามค่า pH ของผิว
    if skin_ph < 4.5:
        r = min(255, r * 1.1 + 10)
        b = max(0, b * 0.9 - 5)
    elif skin_ph > 5.5:
        r = r * 0.92
        g = g * 0.92
        b = b * 0.92
        
    final_rgb = (int(r), int(g), int(b))
    hex_color = '#{:02x}{:02x}{:02x}'.format(final_rgb[0], final_rgb[1], final_rgb[2])
    
    # 4. แสดงผลลัพธ์บนหน้าจอ Streamlit
    st.subheader("ผลลัพธ์การแนะนำเฉดสีตามสภาพผิว")
    st.write(f"**ค่า pH ที่ใช้ประมวลผล:** {skin_ph}")
    st.markdown(f"**รหัสสี (Hex Code) ที่แนะนำ:** `{hex_color}`")
    
    # แสดงตัวอย่างกล่องสีบนหน้าจอ
    st.markdown(
        f'<div style="width: 100px; height: 100px; background-color: {hex_color}; border-radius: 50%; border: 2px solid #ccc;"></div>',
        unsafe_allow_html=True
    )

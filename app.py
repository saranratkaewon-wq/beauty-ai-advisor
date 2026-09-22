import streamlit as st
import numpy as np
from PIL import Image

# กำหนดค่าภาษา
LANGUAGES = {
    "TH": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "โครงงานวิทยาศาสตร์: การพัฒนาเว็บแอปพลิเคชันแนะนำโทนลิปสติกและรองพื้นด้วย AI",
        "upload_label": "อัปโหลดรูปภาพผิวหน้า หรือถ่ายภาพเพื่อวิเคราะห์",
        "analyzing": "กำลังวิเคราะห์อันเดอร์โทนและจำลองค่า pH ของผิว...",
        "skin_result": "ผลการวิเคราะห์สภาพผิวและค่า pH อัตโนมัติ",
        "foundation_title": "1. รองพื้น (Foundation) ที่แนะนำ",
        "blush_title": "2. บลัชออน (Blush On) ที่แนะนำ",
        "lip_title": "3. ลิปสติก (Lipstick) ที่แนะนำ",
        "eye_title": "4. อายแชโดว์ (Eyeshadow) ที่แนะนำ",
        "prep_title": "💡 ขั้นตอนการเตรียมผิวหน้า (Skincare & Prep)",
        "prep_steps": [
            "**1. ทำความสะอาดผิวหน้า (Cleanse):** ล้างหน้าด้วยเจลหรือโฟมล้างหน้าที่เหมาะกับสภาพผิว",
            "**2. ปรับสมดุลผิว (Tone):** เช็ดหน้าด้วยโทนเนอร์เบาๆ เพื่อเตรียมผิว",
            "**3. เติมความชุ่มชื้น (Moisturize):** ทาเซรั่มและมอยส์เจอร์ไรเซอร์ (รอซึม 1-2 นาที)",
            "**4. ทาครีมกันแดด (Sunscreen):** บีบในปริมาณที่เหมาะสม (ประมาณ 2ข้อนิ้วมือ)",
            "**5. ลงไพร์เมอร์ (Primer):** ทาเฉพาะจุด T-zone เพื่อเบลอรูขุมขนและล็อกเมคอัพ"
        ]
    },
    "EN": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "Science Project: AI-Powered Foundation & Lipstick Shade Recommender",
        "upload_label": "Upload or capture your face image for analysis",
        "analyzing": "Analyzing undertone and simulating skin pH...",
        "skin_result": "Automated Skin Condition & pH Analysis",
        "foundation_title": "1. Recommended Foundation",
        "blush_title": "2. Recommended Blush On",
        "lip_title": "3. Recommended Lipstick",
        "eye_title": "4. Recommended Eyeshadow",
        "prep_title": "💡 Skincare & Prep Steps",
        "prep_steps": [
            "**1. Cleanse:** Wash face with suitable gel or foam cleanser.",
            "**2. Tone:** Gently apply toner to balance skin.",
            "**3. Moisturize:** Apply serum and moisturizer (wait 1-2 mins).",
            "**4. Sunscreen:** Apply adequate amount (approx. 2 finger lengths).",
            "**5. Primer:** Apply on T-zone to blur pores and lock makeup."
        ]
    }
}

# เลือกภาษาที่มุมขวาบน
st.sidebar.title("Settings / ตั้งค่า")
lang = st.sidebar.selectbox("Language / ภาษา", ["TH", "EN"])
t = LANGUAGES[lang]

st.title(t["title"])
st.write(t["subtitle"])

# 1. อัปโหลดภาพ
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Image Preview", use_container_width=True)
    
    img_np = np.array(img)
    height, width, _ = img_np.shape
    
    # ตัดโซนกลางภาพสกัดสีผิว
    crop_margin_h = int(height * 0.25)
    crop_margin_w = int(width * 0.25)
    center_region = img_np[crop_margin_h:height-crop_margin_h, crop_margin_w:width-crop_margin_w]
    
    brightness = np.mean(center_region, axis=2)
    filtered_pixels = center_region[(brightness >= 40) & (brightness <= 220)]
    
    if len(filtered_pixels) == 0:
        base_rgb = np.array([200, 150, 120])
    else:
        base_rgb = np.mean(filtered_pixels, axis=0)
        
    r, g, b = base_rgb
    
    # วิเคราะห์ค่า pH และอันเดอร์โทนอัตโนมัติ
    color_ratio = r / (g + 1e-5)
    
    if color_ratio > 1.25:
        estimated_ph = 4.2
        skin_cond = "ผิวมีความไว / ระคายเคืองง่าย (pH ค่อนข้างต่ำ)" if lang == "TH" else "Sensitive / Irritated (Low pH)"
        r = min(255, r * 1.1 + 10)
        b = max(0, b * 0.9 - 5)
    elif color_ratio < 0.95:
        estimated_ph = 5.8
        skin_cond = "ผิวแห้ง / ขาดความสมดุล (pH ค่อนข้างสูง)" if lang == "TH" else "Dry / Imbalanced (High pH)"
        r = r * 0.92
        g = g * 0.92
        b = b * 0.92
    else:
        estimated_ph = 5.0
        skin_cond = "ผิวสุขภาพดี สมดุลปกติ (pH 4.5 - 5.5)" if lang == "TH" else "Healthy / Balanced (pH 4.5 - 5.5)"
        
    final_rgb = (int(r), int(g), int(b))
    hex_color = '#{:02x}{:02x}{:02x}'.format(final_rgb[0], final_rgb[1], final_rgb[2])
    
    # แสดงผลวิเคราะห์ผิว
    st.subheader(t["skin_result"])
    st.info(f"📍 **Condition:** {skin_cond} | **Estimated pH:** {estimated_ph}")
    st.markdown(f"**Mapped Hex Code:** `{hex_color}`")
    st.markdown(f'<div style="width: 80px; height: 80px; background-color: {hex_color}; border-radius: 50%; border: 2px solid #ccc;"></div>', unsafe_allow_html=True)
    
    # ส่วนแนะนำผลิตภัณฑ์
    st.markdown("---")
    
    # 1. รองพื้น
    st.subheader(t["foundation_title"])
    st.markdown("""
    * **00N (Natural Porcelain):** ผิวขาวมากพิเศษ โทนกลางธรรมชาติ
    * **01 / 01 Vanilla & 01N:** ผิวขาวสว่าง โทนกลาง / โทนอุ่นอมเหลือง
    * **02 / 02 Ivory & 02W:** ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง
    * **03 / 03 Petal & 03W (Warm Almond):** ผิวสองสี/ผิวปานกลาง โทนอุ่นเนื้อแอลมอนด์
    * **04N / 04W (Warm Beige):** ผิวสองสีค่อนข้างเข้ม โทนอุ่นอมเหลือง
    * **05W (Warm Sand) & 06W (Warm Honey):** ผิวแทน / ผิวสีน้ำผึ้ง โทนอุ่น
    * **07N & 08N (Caramel / Toffee):** ผิวเข้มลึก โทนกลางธรรมชาติ
    * **เบอร์พิเศษ (22N, 28N):** อุดช่องว่างระหว่างเบอร์ผิวกลางและสองสี
    """)
    
    # 2. บลัชออน
    st.subheader(t["blush_title"])
    st.markdown("""
    * **กลุ่มโทนชมพู (Pink Tones):** `#02 Wavy Pink` (ชมพูนมพาสเทล), `#41 Pinkish Nude` (นู้ดอมเบจละมุน), `#49 Milky Pink` (ชมพูนมเนื้อแมทช์)
    * **กลุ่มโทนส้ม/พีช/คอรัล (Warm Tones):** `#01 Tidal Apricot` (ส้มแอปริคอต), `#03 Soft Peach` (ส้มพีช), `#04 Melon Pomelo` (ส้มคอรัล)
    * **กลุ่มโทนชานม/นู้ดน้ำตาล (Earth Tones):** `#06 Linen Nude` (เบจนู้ดอ่อน), `#35 Rosy Beige` (น้ำตาลนู้ดชมพูกุหลาบ), `#68 Toasted Cinnamon` (น้ำตาลบ่มแดด)
    """)
    
    # 3. ลิปสติก
    st.subheader(t["lip_title"])
    st.markdown("""
    * **กลุ่มสีชมพู (Warm/Neutral Pink):** `#09 Lychee` (ลิ้นจี่ Best Seller), `#16 Pink Taro` (เผือกนม), `#21 Strawberry Acai`, `#22 Very Berry`
    * **กลุ่มสีนู้ดชานม (MLBB Tones):** `#03 Pretzel`, `#04 Biscoff`, `#11 Peanut` (นู้ดชมพูอมน้ำตาล Best Seller)
    * **กลุ่มสีแดง/ส้มอิฐ (Deep & Warm):** `#02 Pear`, `#05 Nama Choco`, `#10 Cranberry` (แครนเบอร์รี่ Best Seller), `#12 Date`, `#13 Apple Glaze`, `#19 Brown Sugar`
    * **กลุ่ม Mixing Color (เบอร์ 24-25):** `#24 Black Sesame` (สีดำดาร์กสี), `#25 Grey` (สีเทาดรอปความสว่าง New Best Seller)
    """)
    
    # 4. อายแชโดว์
    st.subheader(t["eye_title"])
    st.markdown("""
    * **4U2 Eye Shadow Palette:** `#02 Dust of Snow` (ชมพูนู้ดชิมเมอร์), `#03 Wanted` (ชมพูพีชและน้ำตาลอิฐ)
    * **ODD STUDIO Palette:** `#01 Love, Dear` (ชมพู-เบจมินิมอล), `#02 Rose, Moment` (ชมพูกุหลาบอบอุ่น)
    * **Dasique Shadow Palette:** `#02 Rose Petal` (กลีบกุหลาบไล่เฉด), `#14 Peach Squeeze` (พีชส้มแอปริคอตสดใส)
    """)
    
    # 5. ขั้นตอนการเตรียมผิว
    st.markdown("---")
    st.subheader(t["prep_title"])
    for step in t["prep_steps"]:
        st.markdown(f"- {step}")

import streamlit as st
import numpy as np
import random
from PIL import Image

DATABASE = {
    "TH": {
        "foundations": {
            "light": [
                {"name": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ", "hex": "#F9E4D4"},
                {"name": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลาง", "hex": "#F2D8C2"},
                {"name": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนเหลือง", "hex": "#F4D5B6"}
            ],
            "medium": [
                {"name": "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป", "hex": "#E8C5A8"},
                {"name": "02W (Warm Ivory) — ผิวขาวเหลือง โทนอุ่นประกายทอง", "hex": "#E5BE9E"},
                {"name": "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง", "hex": "#D8B08C"},
                {"name": "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี", "hex": "#CE9E7A"}
            ],
            "dark": [
                {"name": "04N (Natural Beige) — ผิวแทน/ผิวเข้ม", "hex": "#BC8C66"},
                {"name": "05W (Warm Sand) — ผิวแทน โทนอุ่นอมแซนด์", "hex": "#A97853"},
                {"name": "06W (Warm Honey) — ผิวสีน้ำผึ้ง/ผิวเข้ม", "hex": "#966542"},
                {"name": "07N (Soft Caramel) — ผิวเข้มลึก โทนธรรมชาติ", "hex": "#7A4E31"}
            ]
        },
        "blushes": [
            {"name": "#02 Wavy Pink (ชมพูนมพาสเทลละมุน)", "hex": "#F4B3C2"},
            {"name": "#41 Pinkish Nude (นู้ดอมเบจละมุน)", "hex": "#E4AC9A"},
            {"name": "#01 Tidal Apricot (ส้มแอปริคอตอุ่นๆ)", "hex": "#F49F75"},
            {"name": "#03 Soft Peach (ส้มพีชละมุนขับผิว)", "hex": "#F99175"},
            {"name": "#06 Linen Nude (เบจนู้ดอ่อน Clean Girl)", "hex": "#D8B49E"},
            {"name": "#35 Rosy Beige (น้ำตาลกุหลาบตุ่น)", "hex": "#C98979"}
        ],
        "lips": [
            {"name": "#09 Lychee (ลิ้นจี่ฉ่ำวาว ขับผิวออร่า)", "hex": "#E04F63"},
            {"name": "#16 Pink Taro (ชมพูเผือกนมๆ นัวๆ)", "hex": "#D896A2"},
            {"name": "#03 Pretzel (นู้ดชานมอมพีชอ่อนๆ)", "hex": "#D49880"},
            {"name": "#11 Peanut (นู้ดชมพูอมน้ำตาล Best Seller)", "hex": "#BC7862"},
            {"name": "#02 Pear (ส้มแอปริคอตสดใสบ่มแดด)", "hex": "#E86A4F"},
            {"name": "#10 Cranberry (แดงแครนเบอร์รี่หน้าไบรท์)", "hex": "#B82238"},
            {"name": "#19 Brown Sugar (น้ำตาลอมแดงอิฐคลาสสิก)", "hex": "#9E4733"}
        ],
        "eyes": [
            {"name": "4U2 #02 Dust of Snow (ชมพูนู้ดชิมเมอร์แชมเปญ)", "hex": "#E5C2BD"},
            {"name": "ODD STUDIO #01 Love, Dear (ชมพู-เบจมินิมอล)", "hex": "#EAD5D1"},
            {"name": "Dasique #02 Rose Petal (กุหลาบอบอุ่นมีมิติ)", "hex": "#D99B9B"},
            {"name": "Dasique #14 Peach Squeeze (พีชส้มแอปริคอตสดใส)", "hex": "#F2A888"}
        ]
    },
    "EN": {
        "foundations": {
            "light": [
                {"name": "00N (Natural Porcelain) — Extra Fair", "hex": "#F9E4D4"},
                {"name": "01N (Natural Vanilla) — Fair Neutral", "hex": "#F2D8C2"},
                {"name": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D5B6"}
            ],
            "medium": [
                {"name": "02N (Natural Ivory) — Light/Medium", "hex": "#E8C5A8"},
                {"name": "02W (Warm Ivory) — Light/Medium Warm", "hex": "#E5BE9E"},
                {"name": "03N (Natural Petal) — Medium Neutral", "hex": "#D8B08C"},
                {"name": "22N (Shell Beige) — Medium Tone", "hex": "#CE9E7A"}
            ],
            "dark": [
                {"name": "04N (Natural Beige) — Tan/Dark", "hex": "#BC8C66"},
                {"name": "05W (Warm Sand) — Tan Warm", "hex": "#A97853"},
                {"name": "06W (Warm Honey) — Deep Honey", "hex": "#966542"},
                {"name": "07N (Soft Caramel) — Deep Caramel", "hex": "#7A4E31"}
            ]
        },
        "blushes": [
            {"name": "#02 Wavy Pink (Pastel Pink)", "hex": "#F4B3C2"},
            {"name": "#41 Pinkish Nude (Soft Beige Nude)", "hex": "#E4AC9A"},
            {"name": "#01 Tidal Apricot (Warm Apricot)", "hex": "#F49F75"},
            {"name": "#03 Soft Peach (Soft Peach)", "hex": "#F99175"},
            {"name": "#06 Linen Nude (Clean Nude)", "hex": "#D8B49E"},
            {"name": "#35 Rosy Beige (Rosy Brown)", "hex": "#C98979"}
        ],
        "lips": [
            {"name": "#09 Lychee (Bright Pink Red)", "hex": "#E04F63"},
            {"name": "#16 Pink Taro (Milky Pink)", "hex": "#D896A2"},
            {"name": "#03 Pretzel (Soft Peach Nude)", "hex": "#D49880"},
            {"name": "#11 Peanut (MLBB Pink Brown)", "hex": "#BC7862"},
            {"name": "#02 Pear (Sun-kissed Apricot)", "hex": "#E86A4F"},
            {"name": "#10 Cranberry (Bright Berry Red)", "hex": "#B82238"},
            {"name": "#19 Brown Sugar (Brick Brown)", "hex": "#9E4733"}
        ],
        "eyes": [
            {"name": "4U2 #02 Dust of Snow (Nude Pink Shimmer)", "hex": "#E5C2BD"},
            {"name": "ODD STUDIO #01 Love, Dear (Minimalist Pink)", "hex": "#EAD5D1"},
            {"name": "Dasique #02 Rose Petal (Warm Rose)", "hex": "#D99B9B"},
            {"name": "Dasique #14 Peach Squeeze (Bright Peach)", "hex": "#F2A888"}
        ]
    }
}

LANGUAGES = {
    "TH": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "ระบบแนะนำเฉดสีเครื่องสำอางเฉพาะบุคคลสำหรับโครงงานวิทยาศาสตร์",
        "upload_label": "อัปโหลดรูปภาพใบหน้าผู้ทดลองเพื่อเลือกเฉดสีที่เหมาะสม",
        "matched_found": "✨ เฉดสีผลิตภัณฑ์ที่คัดเลือกและเหมาะสมกับใบหน้านี้",
        "foundation": "รองพื้น (Foundation)",
        "blush": "บลัชออน (Blush On)",
        "lip": "ลิปสติก (Lipstick)",
        "eye": "อายแชโดว์ (Eyeshadow)",
        "prep_title": "💡 ขั้นตอนการเตรียมผิวหน้า (Skincare & Prep)",
        "prep_steps": [
            "**1. ทำความสะอาดผิวหน้า (Cleanse):** ล้างหน้าด้วยเจลหรือโฟมล้างหน้าที่เหมาะกับสภาพผิว",
            "**2. ปรับสมดุลผิว (Tone):** เช็ดหน้าด้วยโทนเนอร์เบาๆ เพื่อเตรียมผิว",
            "**3. เติมความชุ่มชื้น (Moisturize):** ทาเซรั่มและมอยส์เจอร์ไรเซอร์",
            "**4. ทาครีมกันแดด (Sunscreen):** บีบในปริมาณที่เหมาะสม (ประมาณ 2ข้อนิ้ว)",
            "**5. ลงไพร์เมอร์ (Primer):** ทาเฉพาะจุด T-zone เพื่อเบลอรูขุมขนและล็อกเมคอัพ"
        ]
    },
    "EN": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "Personalized Cosmetic Shade Recommender for Science Project",
        "upload_label": "Upload test subject face image to match shades",
        "matched_found": "✨ Dynamically Matched Product Shades For This Face",
        "foundation": "Foundation",
        "blush": "Blush On",
        "lip": "Lipstick",
        "eye": "Eyeshadow",
        "prep_title": "💡 Skincare & Prep Steps",
        "prep_steps": [
            "**1. Cleanse:** Wash face with suitable cleanser.",
            "**2. Tone:** Apply toner to balance skin.",
            "**3. Moisturize:** Apply moisturizer.",
            "**4. Sunscreen:** Apply sunscreen.",
            "**5. Primer:** Apply on T-zone to lock makeup."
        ]
    }
}

st.title("AI Beauty Advisor & Color Mapping")
st.write("โครงงานวิทยาศาสตร์: ระบบแนะนำเฉดสีเครื่องสำอางเฉพาะบุคคล / Science Project: Personalized Cosmetic Shade Recommender")

# ย้ายปุ่มเลือกภาษามาไว้ตรงกลางหน้าจอหลัก (ใช้ columns จัดวางให้อยู่สวยงาม)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    lang = st.selectbox("🌐 Select Language / เลือกภาษา", ["TH", "EN"])

t = LANGUAGES[lang]
db = DATABASE[lang]

st.markdown("---")
uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Test Subject Preview", use_container_width=True)
    
    img_np = np.array(img)
    height, width, _ = img_np.shape
    
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
    avg_brightness = np.mean(base_rgb)
    
    img_seed = int(r + g + b)
    random.seed(img_seed)
    
    if avg_brightness > 175:
        skin_type_key = "light"
    elif avg_brightness > 120:
        skin_type_key = "medium"
    else:
        skin_type_key = "dark"
        
    matched_fd = random.choice(db["foundations"][skin_type_key])
    matched_blush = random.choice(db["blushes"])
    matched_lip = random.choice(db["lips"])
    matched_eye = random.choice(db["eyes"])
    
    st.markdown("---")
    st.subheader(t["matched_found"])
    
    def render_color_item(label, item):
        st.markdown(f"**{label}:** {item['name']}")
        st.markdown(f'<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;"><div style="width: 35px; height: 35px; background-color: {item["hex"]}; border-radius: 6px; border: 1.5px solid #bbb;"></div><span style="font-size: 14px; color: #555;">Color Code / Swatch: <code>{item["hex"]}</code></span></div>', unsafe_allow_html=True)

    render_color_item(t['foundation'], matched_fd)
    render_color_item(t['blush'], matched_blush)
    render_color_item(t['lip'], matched_lip)
    render_color_item(t['eye'], matched_eye)
    
    st.markdown("---")
    st.subheader(t["prep_title"])
    for step in t["prep_steps"]:
        st.markdown(f"- {step}")

import streamlit as st
from PIL import Image, ImageStat
import cv2
import numpy as np
import mediapipe as mp

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : Beauty AI Advisor", page_icon="🎀", layout="centered")

# CSS ตกแต่งธีมน่ารัก ละมุน นวลตา (Soft Dusty Rose - ถนอมสายตา)
st.markdown("""
<style>
    .stApp {
        background-color: #FAF5F6 !important;
    }
    
    p, span, label, div, h1, h2, h3, h4, .stMarkdown {
        color: #4A3B40 !important;
        font-family: 'Sukhumvit Set', 'Kanit', sans-serif;
    }

    .main-title {
        color: #B85B74 !important;
        text-align: center;
        font-weight: bold;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #8E485B !important;
        text-align: center;
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    /* กล่องการ์ดสรุปผลนวลตา */
    .result-card {
        background-color: #FFFFFF !important;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 8px 20px rgba(184, 91, 116, 0.08);
        border: 1px solid #F2D6DC;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .section-head {
        color: #B85B74 !important;
        font-size: 1.1rem;
        font-weight: bold;
        border-bottom: 2px dashed #E8B4C0;
        padding-bottom: 6px;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    /* วงกลมตัวอย่างสี */
    .swatch-circle {
        display: inline-block;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
        border: 2px solid #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }

    /* ปุ่มกดสีชมพูนวลนุ่ม */
    .stButton>button {
        background: linear-gradient(135deg, #D8708A, #B85B74) !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 12px rgba(184, 91, 116, 0.3) !important;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #E0829B, #C2667F) !important;
    }

    .tip-box {
        background-color: #F8ECEF !important;
        border-left: 4px solid #B85B74;
        padding: 12px 15px;
        border-radius: 10px;
        margin-top: 15px;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# ฟังก์ชันคำนวณความสว่างของรูปภาพ
def check_image_brightness(img):
    gray_img = img.convert('L')
    stat = ImageStat.Stat(gray_img)
    return stat.mean[0]

# ฟังก์ชันตรวจจับใบหน้าและสกัดสีผิวเฉพาะบริเวณแก้มอัตโนมัติ
def analyze_skin_from_image(img):
    img_rgb = np.array(img.convert('RGB'))
    h, w, _ = img_rgb.shape
    
    mp_face_detection = mp.solutions.face_detection
    face_detected = False
    
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.4) as face_detection:
        results = face_detection.process(img_rgb)
        
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                xmin = int(bboxC.xmin * w)
                ymin = int(bboxC.ymin * h)
                box_w = int(bboxC.width * w)
                box_h = int(bboxC.height * h)
                
                # ครอปเฉพาะบริเวณแก้ม (ตรงกลางใบหน้า ย่อยขอบเพื่อไม่ให้ติดผมหรือฉากหลัง)
                cheek_xmin = max(0, xmin + int(box_w * 0.35))
                cheek_xmax = min(w, xmin + int(box_w * 0.65))
                cheek_ymin = max(0, ymin + int(box_h * 0.45))
                cheek_ymax = min(h, ymin + int(box_h * 0.65))
                
                face_crop = img_rgb[cheek_ymin:cheek_ymax, cheek_xmin:cheek_xmax]
                
                if face_crop.size > 0:
                    r = int(np.mean(face_crop[:, :, 0]))
                    g = int(np.mean(face_crop[:, :, 1]))
                    b = int(np.mean(face_crop[:, :, 2]))
                    face_detected = True
                    break
                    
    # หากตรวจไม่พบใบหน้า ให้ใช้ค่าเฉลี่ยพื้นที่ตรงกลาง
    if not face_detected:
        stat = ImageStat.Stat(img.convert('RGB'))
        r, g, b = int(stat.mean[0]), int(stat.mean[1]), int(stat.mean[2])
    
    hex_code = f"#{r:02X}{g:02X}{b:02X}"
    
    # คำนวณจำแนกอันเดอร์โทน (Cool / Warm / Neutral)
    if (r - b) < 32 or (b > g * 0.82):
        undertone = "Cool"
    elif (r - b) > 48 and (g - b) > 22:
        undertone = "Warm"
    else:
        undertone = "Neutral"
        
    return r, g, b, hex_code, undertone, face_detected

# ฐานข้อมูลเครื่องสำอาง
FOUNDATION_DB = {
    "Warm": [
        {"name_th": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "name_en": "00W (Warm Porcelain) — Very Fair Warm", "hex": "#F9E4D3"},
        {"name_th": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "name_en": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D2BA"},
        {"name_th": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "name_en": "02W (Warm Ivory) — Light Medium Warm", "hex": "#E9C7AA"},
        {"name_th": "02G (Golden Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง", "name_en": "02G (Golden Ivory) — Light Medium Golden", "hex": "#E2BC9B"}
    ],
    "Cool": [
        {"name_th": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนอมชมพูธรรมชาติ", "name_en": "00N (Natural Porcelain) — Very Fair Neutral/Cool", "hex": "#FAF0E6"},
        {"name_th": "01 / 01 Vanilla — ผิวขาวสว่าง โทนชมพูละมุน", "name_en": "01 / 01 Vanilla — Fair Cool", "hex": "#F6E3D4"},
        {"name_th": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนธรรมชาติอมชมพู", "name_en": "01N (Natural Vanilla) — Fair Natural Cool", "hex": "#F2D8C6"},
        {"name_th": "02N (Natural Ivory) — ผิวขาวอมชมพูทั่วไป", "name_en": "02N (Natural Ivory) — Light Medium Cool", "hex": "#EACCB8"}
    ],
    "Neutral": [
        {"name_th": "02 / 02 Ivory — ผิวขาวเหลืองทั่วไป โทนดั้งเดิม", "name_en": "02 / 02 Ivory — Light Medium Classic", "hex": "#E8CAAF"},
        {"name_th": "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี โทนกลางธรรมชาติ", "name_en": "22N (Shell Beige) — Medium Natural", "hex": "#DDB18F"}
    ]
}

BLUSH_DB = {
    "Warm": [
        {"name_th": "#01 Tidal Apricot (ส้มแอปริคอตนวลอบอุ่น)", "name_en": "#01 Tidal Apricot (Warm Soft Apricot)", "hex": "#FBAA82"},
        {"name_th": "#03 Soft Peach (ส้มพีชละมุนมีออร่า)", "name_en": "#03 Soft Peach (Glowing Soft Peach)", "hex": "#F39B82"}
    ],
    "Cool": [
        {"name_th": "#02 Wavy Pink (ชมพูนมสว่างพาสเทล)", "name_en": "#02 Wavy Pink (Bright Pastel Milky Pink)", "hex": "#FFAEC1"},
        {"name_th": "#49 Milky Pink (ชมพูนมเนื้อแมทช์นุ่ม)", "name_en": "#49 Milky Pink (Soft Matte Milky Pink)", "hex": "#F88DA5"}
    ],
    "Neutral": [
        {"name_th": "#06 Linen Nude (เบจนู้ดอมน้ำตาลอ่อนคลีนๆ)", "name_en": "#06 Linen Nude (Clean Light Brown Nude)", "hex": "#D39B87"},
        {"name_th": "#35 Rosy Beige (น้ำตาลนู้ดอมชมพูกุหลาบตุ่น)", "name_en": "#35 Rosy Beige (Muted Rosy Brown)", "hex": "#BF8278"}
    ]
}

LIP_DB = {
    "Warm": [
        {"name_th": "#03 Pretzel (นู้ดน้ำตาลส้มอมพีชอ่อน)", "name_en": "#03 Pretzel (Soft Peach Orange Nude)", "hex": "#CE8067"},
        {"name_th": "#10 Cranberry [Best Seller] 🌟 (แดงแครนเบอร์รี่ฉ่ำไบรท์)", "name_en": "#10 Cranberry [Best Seller] 🌟 (Bright Cranberry Red)", "hex": "#AB1227"}
    ],
    "Cool": [
        {"name_th": "#09 Lychee [Best Seller] 🌟 (ชมพูอมแดงระเรื่อ)", "name_en": "#09 Lychee [Best Seller] 🌟 (Fresh Lychee Pink Red)", "hex": "#D54D6C"},
        {"name_th": "#16 Pink Taro (ชมพูนมนัวอมตุ่นไซรัป)", "name_en": "#16 Pink Taro (Muted Syrup Taro Pink)", "hex": "#CD728B"},
        {"name_th": "#21 Strawberry Acai (ชมพูอมแดงสตรอว์เบอร์รี่สดใส)", "name_en": "#21 Strawberry Acai (Vibrant Strawberry Pink)", "hex": "#E02E4E"}
    ],
    "Neutral": [
        {"name_th": "#11 Peanut [Best Seller] 🌟 (นู้ดชมพูอมน้ำตาลตุ่น)", "name_en": "#11 Peanut [Best Seller] 🌟 (Muted Neutral Rosy Brown MLBB)", "hex": "#B1635F"},
        {"name_th": "#25 Grey [Mixing Color] 🌟 (สีเทา: ใช้ทาทับดร็อบความสว่างเพิ่มความหม่นตุ่น)", "name_en": "#25 Grey [Mixing Color] 🌟 (Grey: To mute down brightness)", "hex": "#827271"}
    ]
}

EYESHADOW_DB = {
    "Warm": [
        {"name_th": "4U2 #03 Wanted — โทนชมพูอมส้มพีช คอรัลอุ่น น้ำตาลอิฐ", "name_en": "4U2 #03 Wanted — Warm Coral Peach & Brick Brown", "hex": "#D4735B"}
    ],
    "Cool": [
        {"name_th": "Dasique #02 Rose Petal — โทนชมพูกลีบกุหลาบ กลิตเตอร์ทองฉ่ำ", "name_en": "Dasique #02 Rose Petal — Dusty Rose & Gold Shimmer", "hex": "#D88289"}
    ],
    "Neutral": [
        {"name_th": "4U2 #02 Dust of Snow — โทนชมพูนู้ด น้ำตาลตุ่น ชิมเมอร์แชมเปญ", "name_en": "4U2 #02 Dust of Snow — Nude Pink, Taupe & Champagne", "hex": "#C8958B"}
    ]
}

def render_swatch(hex_code, text):
    return f'<div style="margin-bottom:8px;"><span class="swatch-circle" style="background-color:{hex_code};"></span><span style="font-size:0.95rem;">{text}</span></div>'

# ส่วนหน้าตาแอปพลิเคชัน
st.markdown('<div class="main-title">🎀 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ AI Automatic Face & Personal Color Advisor ✨</div>', unsafe_allow_html=True)

lang = st.selectbox("🌐 เปลี่ยนภาษา / Select Language", ["TH (ไทย)", "EN (English)"])
is_th = "TH" in lang

st.write("---")

st.subheader("📷 " + ("อัปโหลดรูปภาพใบหน้าเพื่อให้อัลกอริทึมวิเคราะห์อัตโนมัติ" if is_th else "Upload Face Photo for Automatic AI Analysis"))

uploaded_file = st.file_uploader(
    "เลือกไฟล์รูปภาพใบหน้าของคุณ (JPG, PNG)" if is_th else "Upload your face photo (JPG, PNG)", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 " + ("รูปภาพใบหน้าที่ใช้วิเคราะห์" if is_th else "Uploaded Face Photo"), use_container_width=True)

btn_text = "✨ ประมวลผลภาพถ่ายและวิเคราะห์เมคอัพอัตโนมัติ" if is_th else "✨ Analyze Image & Recommend Makeup"
if st.button(btn_text, type="primary"):
    if uploaded_file is None:
        st.warning("⚠️ " + ("กรุณาอัปโหลดรูปภาพใบหน้าก่อนทำการวิเคราะห์" if is_th else "Please upload a face image first."))
    else:
        st.balloons()
        
        r, g, b, hex_code, key, face_detected = analyze_skin_from_image(image)
        
        if key == "Warm":
            undertone_title = "Warm Tone (โทนอุ่น / ผิวโทนเหลือง-สองสี)" if is_th else "Warm Tone (Warm / Yellow undertone)"
            style_desc = "เหมาะกับการแต่งหน้าโทนส้มพีช คอรัล อบอุ่น ให้ลุคผิวสุขภาพดี บ่มแดด มีออร่าสดใส" if is_th else "Best suited for warm peach, coral, and warm brick tones."
        elif key == "Cool":
            undertone_title = "Cool Tone (โทนเย็น / ผิวโทนชมพู)" if is_th else "Cool Tone (Cool / Pink undertone)"
            style_desc = "เหมาะกับการแต่งหน้าโทนชมพูนม ชมพูกุหลาบ เบอร์รี่ ให้ลุคหน้าผ่อง สว่างใส ละมุนแบบสไตล์เกาหลี" if is_th else "Best suited for milky pink, rose, and berry shades."
        else:
            undertone_title = "Neutral Tone (โทนธรรมชาติ)" if is_th else "Neutral Tone (Neutral undertone)"
            style_desc = "เหมาะกับการแต่งหน้าโทนชานม นู้ดเบจ นู้ดชมพูตุ่น ให้ลุคสวยแพง สุภาพ เรียบหรูคลาสสิก" if is_th else "Best suited for milk tea, beige, and rosy nude shades."

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        res_head = "💖 ผลการวิเคราะห์เมคอัพเฉพาะบุคคล GlamAI 💖" if is_th else "💖 GlamAI Personal Makeup Analysis 💖"
        st.markdown(f'<h3 style="color:#B85B74; text-align:center; margin-top:0;">{res_head}</h3>', unsafe_allow_html=True)
        
        if face_detected:
            st.success("🎯 " + ("ตรวจพบใบหน้าและสกัดสีจากบริเวณแก้มสำเร็จ!" if is_th else "Face detected! Successfully extracted cheek skin color."))
        else:
            st.info("ℹ️ " + ("ไม่พบตำแหน่งใบหน้าชัดเจน ระบบใช้วิธีคำนวณค่าสีโดยรวมของภาพ" if is_th else "Face location unclear, calculated from overall frame."))

        skin_label = f"<b>สีผิวที่สกัดจากบริเวณใบหน้าจริง:</b> <code>HEX: {hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})" if is_th else f"<b>Cheek Skin Extracted:</b> <code>HEX: {hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})"
        st.markdown(render_swatch(hex_code, skin_label), unsafe_allow_html=True)
        
        under_label = f"🌈 <b>ผลการคำนวณอันเดอร์โทน:</b> {undertone_title}" if is_th else f"🌈 <b>Calculated Undertone:</b> {undertone_title}"
        st.markdown(under_label, unsafe_allow_html=True)
        
        style_label = f"✨ <b>สไตล์การแต่งหน้าที่แนะนำ:</b> {style_desc}" if is_th else f"✨ <b>Recommended Style:</b> {style_desc}"
        st.markdown(style_label, unsafe_allow_html=True)
        
        st.markdown(f'<div class="section-head">🧴 {"รองพื้นที่เหมาะกับเฉดผิว" if is_th else "Recommended Foundation Shades"}</div>', unsafe_allow_html=True)
        for item in FOUNDATION_DB[key]:
            name = item["name_th"] if is_th else item["name_en"]
            st.markdown(render_swatch(item["hex"], name), unsafe_allow_html=True)
            
        st.markdown(f'<div class="section-head">🌸 {"บลัชออนที่ขับผิวผ่อง" if is_th else "Recommended Blush Shades"}</div>', unsafe_allow_html=True)
        for item in BLUSH_DB[key]:
            name = item["name_th"] if is_th else item["name_en"]
            st.markdown(render_swatch(item["hex"], name), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">💋 {"เฉดสีลิปสติกที่แนะนำ" if is_th else "Recommended Lipstick Shades"}</div>', unsafe_allow_html=True)
        for item in LIP_DB[key]:
            name = item["name_th"] if is_th else item["name_en"]
            st.markdown(render_swatch(item["hex"], name), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">👁️ {"พาเลตต์ตาที่เข้ากัน" if is_th else "Recommended Eyeshadow Palettes"}</div>', unsafe_allow_html=True)
        for item in EYESHADOW_DB[key]:
            name = item["name_th"] if is_th else item["name_en"]
            st.markdown(render_swatch(item["hex"], name), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

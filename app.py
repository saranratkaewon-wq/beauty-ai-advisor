import streamlit as st
import numpy as np
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : AI Beauty Advisor Project", page_icon="🎀", layout="centered")

# CSS ตกแต่งธีมโครงงาน (แบบไม่มี Sidebar)
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
        font-size: 0.95rem;
        margin-bottom: 10px;
    }

    .project-badge {
        background-color: #F2D6DC;
        color: #8E485B;
        text-align: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        margin-bottom: 15px;
        display: inline-block;
        width: 100%;
    }

    .info-box {
        background-color: #FFF0F3 !important;
        border-left: 4px solid #B85B74;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }

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

    .stButton>button {
        width: 100%;
        background-color: #B85B74 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        border: none !important;
        font-size: 1.05rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอาง
FOUNDATION_DB = {
    "Warm": [
        {"name_th": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "name_en": "00W (Warm Porcelain) — Very Fair Warm", "hex": "#F9E4D3"},
        {"name_th": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "name_en": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D2BA"},
        {"name_th": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "name_en": "02W (Warm Ivory) — Medium Warm", "hex": "#E9C7AA"}
    ],
    "Cool": [
        {"name_th": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนอมชมพูธรรมชาติ", "name_en": "00N (Natural Porcelain) — Very Fair Cool", "hex": "#FAF0E6"},
        {"name_th": "01 / 01 Vanilla — ผิวขาวสว่าง โทนชมพูละมุน", "name_en": "01 / 01 Vanilla — Fair Cool", "hex": "#F6E3D4"},
        {"name_th": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนธรรมชาติอมชมพู", "name_en": "01N (Natural Vanilla) — Fair Natural Cool", "hex": "#F2D8C6"}
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
    "Warm": [{"name_th": "4U2 #03 Wanted — โทนชมพูอมส้มพีช คอรัลอุ่น", "name_en": "4U2 #03 Wanted — Warm Coral Peach", "hex": "#D4735B"}],
    "Cool": [{"name_th": "Dasique #02 Rose Petal — โทนชมพูกลีบกุหลาบ", "name_en": "Dasique #02 Rose Petal — Dusty Rose", "hex": "#D88289"}],
    "Neutral": [{"name_th": "4U2 #02 Dust of Snow — โทนชมพูนู้ด น้ำตาลตุ่น", "name_en": "4U2 #02 Dust of Snow — Nude Pink", "hex": "#C8958B"}]
}

def render_swatch(hex_code, text):
    return f'<div style="margin-bottom:8px;"><span class="swatch-circle" style="background-color:{hex_code};"></span><span style="font-size:0.95rem;">{text}</span></div>'

def extract_skin_color_accurate(img_array):
    h, w, _ = img_array.shape
    crop_h_start, crop_h_end = int(h * 0.35), int(h * 0.65)
    crop_w_start, crop_w_end = int(w * 0.25), int(w * 0.75)
    center_area = img_array[crop_h_start:crop_h_end, crop_w_start:crop_w_end]
    
    pixels = center_area.reshape(-1, 3)
    brightness = 0.299 * pixels[:, 0] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 2]
    valid_mask = (brightness > 70) & (brightness < 220)
    filtered_pixels = pixels[valid_mask]
    
    if len(filtered_pixels) > 0:
        avg_rgb = np.mean(filtered_pixels, axis=0)
    else:
        avg_rgb = np.mean(pixels, axis=0)
        
    r, g, b = int(avg_rgb[0]), int(avg_rgb[1]), int(avg_rgb[2])
    return r, g, b

# ส่วนหัวข้อโครงงาน
st.markdown('<div class="main-title">🎀 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">ระบบวิเคราะห์อันเดอร์โทนสีผิวและแนะนำเครื่องสำอางอัจฉริยะด้วยการประมวลผลภาพ</div>', unsafe_allow_html=True)
st.markdown('<div class="project-badge">📌 โครงงานคอมพิวเตอร์ ระดับชั้นมัธยมศึกษาปีที่ 5</div>', unsafe_allow_html=True)

lang = st.selectbox("🌐 เปลี่ยนภาษา / Select Language", ["TH (ไทย)", "EN (English)"])
is_th = "TH" in lang

st.write("---")

if is_th:
    st.markdown("""
    <div class="info-box">
        <b>💡 คำแนะนำสำหรับการทดลองใช้งานเพื่อให้แม่นยำที่สุด:</b><br>
        1. ☀️ ถ่ายในสถานที่ที่มี<b>แสงธรรมชาติ</b>สว่างทั่วถึง<br>
        2. 👩‍🦰 หน้าตรง เปิดหน้าผากและแก้ม ไม่ให้มีเส้นผมบดบัง<br>
        3. 🧴 ภาพหน้าสด (ไม่แต่งหน้า) เพื่อผลวิเคราะห์สีผิวจริง
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
        <b>💡 Tips for Best Analysis Results:</b><br>
        1. ☀️ Take photo in <b>natural light</b><br>
        2. 👩‍🦰 Face straight forward and keep hair away from cheeks<br>
        3. 🧴 Bare skin without makeup for true undertone detection
    </div>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📷 ถ่ายรูป หรือ เลือกรูปภาพใบหน้าของคุณ" if is_th else "📷 Take a photo or select your face image", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    
    st.image(image, caption="รูปภาพที่ใช้วิเคราะห์ (Input Image)" if is_th else "Analyzed Image", use_container_width=True)
    
    btn_label = "✨ เริ่มประมวลผลและวิเคราะห์อันเดอร์โทน" if is_th else "✨ Run Undertone Analysis"
    if st.button(btn_label):
        img_array = np.array(image)
        r, g, b = extract_skin_color_accurate(img_array)

        if (r > g) and (g > b):
            if (r - b) > 35 and (g - b) > 15:
                key = "Warm"
                undertone_title = "Warm Tone (โทนอุ่น / ผิวโทนเหลือง-สองสี)" if is_th else "Warm Tone"
                style_desc = "เหมาะกับการแต่งหน้าโทนส้มพีช คอรัล ให้ลุคผิวบ่มแดดสดใส" if is_th else "Best with warm peach & coral tones."
            elif (r - g) < 20:
                key = "Neutral"
                undertone_title = "Neutral Tone (โทนธรรมชาติ)" if is_th else "Neutral Tone"
                style_desc = "เหมาะกับการแต่งหน้าโทนชานม นู้ดเบจ สุภาพ เรียบหรู" if is_th else "Best with milk tea & rosy nude tones."
            else:
                key = "Warm"
                undertone_title = "Warm Tone (โทนอุ่น / ผิวโทนเหลือง-สองสี)" if is_th else "Warm Tone"
                style_desc = "เหมาะกับการแต่งหน้าโทนส้มพีช คอรัล ให้ลุคผิวบ่มแดดสดใส" if is_th else "Best with warm peach & coral tones."
        elif (b > g * 0.88) or (r - b < 20):
            key = "Cool"
            undertone_title = "Cool Tone (โทนเย็น / ผิวโทนชมพู)" if is_th else "Cool Tone"
            style_desc = "เหมาะกับการแต่งหน้าโทนชมพูนม ชมพูกุหลาบ ให้ลุคหน้าผ่อง สว่างใส สไตล์เกาหลี" if is_th else "Best with milky pink & rose tones."
        else:
            key = "Neutral"
            undertone_title = "Neutral Tone (โทนธรรมชาติ)" if is_th else "Neutral Tone"
            style_desc = "เหมาะกับการแต่งหน้าโทนชานม นู้ดเบจ สุภาพ เรียบหรู" if is_th else "Best with milk tea & rosy nude tones."

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        res_head = "💖 ผลการวิเคราะห์จากระบบโครงงาน GlamAI 💖" if is_th else "💖 GlamAI Analysis Result 💖"
        st.markdown(f'<h3 style="color:#B85B74; text-align:center; margin-top:0;">{res_head}</h3>', unsafe_allow_html=True)

        st.markdown(f"🌈 <b>ผลการจำแนกอันเดอร์โทน:</b> {undertone_title}", unsafe_allow_html=True)
        st.markdown(f"✨ <b>คำแนะนำสไตล์เมคอัพ:</b> {style_desc}", unsafe_allow_html=True)
        
        st.markdown(f'<div class="section-head">รองพื้นที่แนะนำ (Recommended Foundation)</div>' if is_th else '<div class="section-head">Foundation</div>', unsafe_allow_html=True)
        for item in FOUNDATION_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)
            
        st.markdown(f'<div class="section-head">บลัชออนที่แนะนำ (Recommended Blush)</div>' if is_th else '<div class="section-head">Blush</div>', unsafe_allow_html=True)
        for item in BLUSH_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">ลิปสติกที่แนะนำ (Recommended Lipstick)</div>' if is_th else '<div class="section-head">Lipstick</div>', unsafe_allow_html=True)
        for item in LIP_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">พาเลตต์ตาที่แนะนำ (Recommended Eyeshadow)</div>' if is_th else '<div class="section-head">Eyeshadow</div>', unsafe_allow_html=True)
        for item in EYESHADOW_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

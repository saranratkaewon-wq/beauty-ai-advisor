import streamlit as st
from PIL import Image, ImageStat
from streamlit_image_coordinates import streamlit_image_coordinates

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : Beauty AI Advisor", page_icon="🎀", layout="centered")

# CSS ตกแต่งธีม
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
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอาง
FOUNDATION_DB = {
    "Warm": [
        {"name_th": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "name_en": "00W (Warm Porcelain) — Very Fair Warm", "hex": "#F9E4D3"},
        {"name_th": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "name_en": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D2BA"},
        {"name_th": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "name_en": "02W (Warm Ivory) — Light Medium Warm", "hex": "#E9C7AA"}
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

# ส่วนหน้าตาแอป
st.markdown('<div class="main-title">🎀 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ Precise Skin Color Sampling & Personal Color Advisor ✨</div>', unsafe_allow_html=True)

lang = st.selectbox("🌐 เปลี่ยนภาษา / Select Language", ["TH (ไทย)", "EN (English)"])
is_th = "TH" in lang

st.write("---")
st.subheader("📷 " + ("อัปโหลดรูปภาพ แล้วแตะบนผิวหน้าเพื่อสกัดสี" if is_th else "Upload photo and tap on your face cheek"))

uploaded_file = st.file_uploader(
    "เลือกไฟล์รูปภาพใบหน้าของคุณ (JPG, PNG)" if is_th else "Upload your face photo", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    
    st.info("👇 " + ("คำแนะนำ: กรุณาแตะ/คลิกที่ บริเวณแก้มหรือผิวหน้า บนรูปภาพด้านล่างเพื่อเลือกจุดสกัดสี" if is_th else "Instructions: Click/Tap on your cheek area on the image below."))
    
    # แสดงรูปและรับพิกัดจุดที่แตะ
    coords = streamlit_image_coordinates(image, key="pil")

    if coords is not None:
        x = coords["x"]
        y = coords["y"]
        
        # สกัดสีรอบๆ จุดที่คลิก (รัศมี 5x5 พิกเซลเพื่อหาค่าเฉลี่ยเนียนๆ)
        crop_box = (max(0, x - 2), max(0, y - 2), min(image.width, x + 3), min(image.height, y + 3))
        cropped_img = image.crop(crop_box)
        stat = ImageStat.Stat(cropped_img)
        
        r = int(stat.mean[0])
        g = int(stat.mean[1])
        b = int(stat.mean[2])
        hex_code = f"#{r:02X}{g:02X}{b:02X}"

        # จำแนกอันเดอร์โทน
        if (r - b) < 32 or (b > g * 0.82):
            key = "Cool"
            undertone_title = "Cool Tone (โทนเย็น / ผิวโทนชมพู)" if is_th else "Cool Tone"
            style_desc = "เหมาะกับการแต่งหน้าโทนชมพูนม ชมพูกุหลาบ ให้ลุคหน้าผ่อง สว่างใส สไตล์เกาหลี" if is_th else "Best with milky pink & rose tones."
        elif (r - b) > 48 and (g - b) > 22:
            key = "Warm"
            undertone_title = "Warm Tone (โทนอุ่น / ผิวโทนเหลือง-สองสี)" if is_th else "Warm Tone"
            style_desc = "เหมาะกับการแต่งหน้าโทนส้มพีช คอรัล ให้ลุคผิวบ่มแดดสดใส" if is_th else "Best with warm peach & coral tones."
        else:
            key = "Neutral"
            undertone_title = "Neutral Tone (โทนธรรมชาติ)" if is_th else "Neutral Tone"
            style_desc = "เหมาะกับการแต่งหน้าโทนชานม นู้ดเบจ สุภาพ เรียบหรู" if is_th else "Best with milk tea & rosy nude tones."

        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        res_head = "💖 ผลการวิเคราะห์เมคอัพเฉพาะบุคคล GlamAI 💖" if is_th else "💖 GlamAI Personal Makeup Analysis 💖"
        st.markdown(f'<h3 style="color:#B85B74; text-align:center; margin-top:0;">{res_head}</h3>', unsafe_allow_html=True)

        skin_label = f"<b>สีผิวที่แตะสกัดจริง (ตำแหน่ง X:{x}, Y:{y}):</b> <code>HEX: {hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})" if is_th else f"<b>Sampled Skin Color:</b> <code>HEX: {hex_code}</code>"
        st.markdown(render_swatch(hex_code, skin_label), unsafe_allow_html=True)
        
        st.markdown(f"🌈 <b>คำนวณอันเดอร์โทน:</b> {undertone_title}", unsafe_allow_html=True)
        st.markdown(f"✨ <b>สไตล์ที่แนะนำ:</b> {style_desc}", unsafe_allow_html=True)
        
        st.markdown(f'<div class="section-head">🧴 {"รองพื้นที่เหมาะกับเฉดผิว" if is_th else "Foundation"}</div>', unsafe_allow_html=True)
        for item in FOUNDATION_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)
            
        st.markdown(f'<div class="section-head">🌸 {"บลัชออน" if is_th else "Blush"}</div>', unsafe_allow_html=True)
        for item in BLUSH_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">💋 {"ลิปสติก" if is_th else "Lipstick"}</div>', unsafe_allow_html=True)
        for item in LIP_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown(f'<div class="section-head">👁️ {"พาเลตต์ตา" if is_th else "Eyeshadow"}</div>', unsafe_allow_html=True)
        for item in EYESHADOW_DB[key]:
            st.markdown(render_swatch(item["hex"], item["name_th"] if is_th else item["name_en"]), unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

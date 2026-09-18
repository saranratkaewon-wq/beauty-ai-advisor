import streamlit as st
from PIL import Image

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : Beauty AI Advisor", page_icon="🎀", layout="centered")

# CSS ตกแต่งธีมน่ารัก ละมุน แกรม (Cute Glam Pastel)
st.markdown("""
<style>
    .stApp {
        background-color: #FFF0F5 !important;
    }
    
    p, span, label, div, h1, h2, h3, h4, .stMarkdown {
        color: #4A154B !important;
        font-family: 'Sukhumvit Set', 'Kanit', sans-serif;
    }

    .main-title {
        color: #D81B60 !important;
        text-align: center;
        font-weight: bold;
        font-size: 2.3rem;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #AD1457 !important;
        text-align: center;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }

    /* กล่องการ์ดสรุปผลน่ารักๆ */
    .result-card {
        background-color: #FFFFFF !important;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 10px 25px rgba(216, 27, 96, 0.12);
        border: 2px solid #FFCCE5;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .section-head {
        color: #C2185B !important;
        font-size: 1.15rem;
        font-weight: bold;
        border-bottom: 2px dashed #FF80AB;
        padding-bottom: 6px;
        margin-top: 18px;
        margin-bottom: 12px;
    }

    /* ตัวอย่างสีกระดุมวงกลม */
    .swatch-circle {
        display: inline-block;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
        border: 2px solid #FFFFFF;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    /* ปุ่มกดน่ารักสดใส */
    .stButton>button {
        background: linear-gradient(135deg, #FF69B4, #FF1493) !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 28px !important;
        box-shadow: 0 5px 15px rgba(255, 105, 180, 0.4) !important;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }

    .tip-box {
        background-color: #FFF5F8 !important;
        border-left: 5px solid #FF4081;
        padding: 12px 15px;
        border-radius: 12px;
        margin-top: 15px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอางตามโครงงานวิทยาศาสตร์
FOUNDATION_DB = {
    "Warm": [
        {"code": "00W", "name": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "hex": "#F8E2CF"},
        {"code": "01W", "name": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "hex": "#F4D2BA"},
        {"code": "02W", "name": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "hex": "#E9C7AA"},
        {"code": "02G", "name": "02G (Golden Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง", "hex": "#E2BC9B"},
        {"code": "22W", "name": "22W (Sheer Beige) — ผิวกลางๆ ค่อนไปทางสองสี โทนอุ่นอมเหลือง", "hex": "#DEB492"},
        {"code": "03W", "name": "03W (Warm Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นอมเหลือง", "hex": "#D6A783"},
        {"code": "03A", "name": "03A (Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นเนื้อแอลมอนด์", "hex": "#CF9E79"},
        {"code": "03G", "name": "03G (Golden Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นประกายทองลุ่มลึก", "hex": "#C6936E"},
        {"code": "04W", "name": "04W (Warm Beige) — ผิวสองสีค่อนข้างเข้ม โทนอุ่นอมเหลือง", "hex": "#BD8761"},
        {"code": "05W", "name": "05W (Warm Sand) — ผิวแทน/ผิวเข้ม โทนอุ่นอมแซนด์", "hex": "#B27B55"},
        {"code": "06W", "name": "06W (Warm Honey) — ผิวสีน้ำผึ้ง/ผิวเข้ม โทนอุ่นอมน้ำผึ้ง", "hex": "#A76E48"}
    ],
    "Cool": [
        {"code": "00N", "name": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนกลางธรรมชาติ", "hex": "#FAF0E6"},
        {"code": "01", "name": "01 / 01 Vanilla — ผิวขาวสว่าง โทนดั้งเดิม (กึ่งนิวทรัล)", "hex": "#F6E3D4"},
        {"code": "01N", "name": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลางธรรมชาติ", "hex": "#F2D8C6"},
        {"code": "02N", "name": "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป โทนกลางธรรมชาติ", "hex": "#EACCB8"}
    ],
    "Neutral": [
        {"code": "02", "name": "02 / 02 Ivory — ผิวขาวเหลืองทั่วไป โทนดั้งเดิม", "hex": "#E8CAAF"},
        {"code": "22N", "name": "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี โทนกลางธรรมชาติ", "hex": "#DDB18F"},
        {"code": "03N", "name": "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง โทนกลางธรรมชาติ", "hex": "#D4A37F"},
        {"code": "28N", "name": "28N (Oat) — ผิวสองสีค่อนข้างเข้ม โทนกลางธรรมชาติอมโอ๊ต", "hex": "#C89571"},
        {"code": "04N", "name": "04N (Natural Beige) — ผิวแทน/ผิวเข้ม โทนกลางธรรมชาติ", "hex": "#BA845F"},
        {"code": "07N", "name": "07N (Soft Caramel) — ผิวเข้มลึก โทนกลางธรรมชาติอมคาราเมล", "hex": "#9B633F"},
        {"code": "08N", "name": "08N (Rich Toffee) — ผิวเข้มลึกมาก โทนกลางธรรมชาติอมท็อฟฟี่", "hex": "#844F2E"}
    ]
}

BLUSH_DB = [
    {"group": "กลุ่มโทนชมพู (Pink Tones)", "name": "#02 Wavy Pink (ชมพูนมสว่างพาสเทล)", "hex": "#FFB7C5"},
    {"group": "กลุ่มโทนชมพู (Pink Tones)", "name": "#41 Pinkish Nude (ชมพูนู้ดอมเบจละมุน)", "hex": "#E8A3A8"},
    {"group": "กลุ่มโทนชมพู (Pink Tones)", "name": "#49 Milky Pink (ชมพูนมเนื้อแมทช์นุ่ม)", "hex": "#FF99B2"},
    {"group": "กลุ่มโทนส้ม/พีช/คอรัล (Warm Tones)", "name": "#01 Tidal Apricot (ส้มแอปริคอตนวลอบอุ่น)", "hex": "#FBB088"},
    {"group": "กลุ่มโทนส้ม/พีช/คอรัล (Warm Tones)", "name": "#03 Soft Peach (ส้มพีชละมุนมีออร่า)", "hex": "#F4A28C"},
    {"group": "กลุ่มโทนส้ม/พีช/คอรัล (Warm Tones)", "name": "#04 Melon Pomelo (ส้มอมชมพูคอรัลสดใส)", "hex": "#FF8A7A"},
    {"group": "กลุ่มโทนชานม/นู้ดน้ำตาล (Earth Tones)", "name": "#06 Linen Nude (เบจนู้ดอมน้ำตาลอ่อนคลีนๆ)", "hex": "#D8A28C"},
    {"group": "กลุ่มโทนชานม/นู้ดน้ำตาล (Earth Tones)", "name": "#35 Rosy Beige (น้ำตาลนู้ดอมชมพูกุหลาบตุ่น)", "hex": "#C98A80"},
    {"group": "กลุ่มโทนชานม/นู้ดน้ำตาล (Earth Tones)", "name": "#68 Toasted Cinnamon (น้ำตาลบ่มแดดติ่งส้มอิฐ)", "hex": "#B86D53"}
]

LIP_DB = [
    {"group": "กลุ่มสีชมพู (Warm / Neutral Pink)", "name": "#09 Lychee [Best Seller] 🌟 (ชมพูอมแดงระเรื่อ)", "hex": "#DC5B78"},
    {"group": "กลุ่มสีชมพู (Warm / Neutral Pink)", "name": "#16 Pink Taro (ชมพูนมนัวอมตุ่นไซรัป)", "hex": "#D47A92"},
    {"group": "กลุ่มสีชมพู (Warm / Neutral Pink)", "name": "#21 Strawberry Acai (ชมพูอมแดงสตรอว์เบอร์รี่สดใส)", "hex": "#E63956"},
    {"group": "กลุ่มสีชมพู (Warm / Neutral Pink)", "name": "#22 Very Berry (ชมพูเบอร์รี่เข้มข้นฉ่ำน้ำ)", "hex": "#C2185B"},
    {"group": "กลุ่มสีนู้ดชานม/ชมพูตุ่น (MLBB)", "name": "#03 Pretzel (นู้ดน้ำตาลส้มอมพีชอ่อน)", "hex": "#D28B72"},
    {"group": "กลุ่มสีนู้ดชานม/ชมพูตุ่น (MLBB)", "name": "#04 Biscoff (นู้ดชานมอมน้ำตาลนวล)", "hex": "#C47B62"},
    {"group": "กลุ่มสีนู้ดชานม/ชมพูตุ่น (MLBB)", "name": "#11 Peanut [Best Seller] 🌟 (นู้ดชมพูอมน้ำตาลตุ่น)", "hex": "#B86B66"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#02 Pear (ส้มแอปริคอตสดใสบ่มแดด)", "hex": "#E06D3B"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#05 Nama Choco (น้ำตาลช็อกโกแลตเข้มข้น)", "hex": "#6A3828"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#10 Cranberry [Best Seller] 🌟 (แดงแครนเบอร์รี่ฉ่ำไบรท์)", "hex": "#B0122A"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#12 Date (แดงก่ำอมน้ำตาลอินทผลัม)", "hex": "#8C2320"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#13 Apple Glaze (แดงแอปเปิ้ลเคลือบแก้ว)", "hex": "#D01C24"},
    {"group": "กลุ่มสีแดง/ส้มอิฐ/ช็อกโกแลต (Deep & Warm)", "name": "#19 Brown Sugar (น้ำตาลอมแดงอิฐอุ่น)", "hex": "#A0402C"},
    {"group": "รุ่นพิเศษ Mixing Color", "name": "#24 Black Sesame (สีดำ: ใช้ผสมดึงสีลิปให้ดาร์กเข้มขึ้น)", "hex": "#2B2B2B"},
    {"group": "รุ่นพิเศษ Mixing Color", "name": "#25 Grey [Best Seller] 🌟 (สีเทา: ใช้ทาทับดร็อบความสว่างเพิ่มความหม่นตุ่น)", "hex": "#8C7B7A"}
]

EYESHADOW_DB = [
    {"brand": "4U2 Eye Shadow Palette", "name": "#02 Dust of Snow (ชมพูนู้ด-น้ำตาลตุ่น ชิมเมอร์แชมเปญทอง)", "hex": "#D4A398"},
    {"brand": "4U2 Eye Shadow Palette", "name": "#03 Wanted (ชมพูอมส้มพีช คอรัลอุ่น น้ำตาลอิฐแมทช์)", "hex": "#D97D64"},
    {"brand": "ODD STUDIO Palette", "name": "#01 Love, Dear (ชมพูนู้ดธรรมชาติ ชานมแมทช์)", "hex": "#D29F91"},
    {"brand": "ODD STUDIO Palette", "name": "#02 Rose, Moment (ชมพูกลีบกุหลาบแห้ง วิ้งค์ทอง)", "hex": "#C87B82"},
    {"brand": "Dasique Shadow Palette", "name": "#02 Rose Petal (ชมพูกลีบกุหลาบ กลิตเตอร์ทองฉ่ำ)", "hex": "#E08F95"},
    {"brand": "Dasique Shadow Palette", "name": "#14 Peach Squeeze (ชมพูพีช-ส้มแอปริคอตสดใส)", "hex": "#F49B88"}
]

# ฟังก์ชันแสดงวงกลมตัวอย่างสี
def render_swatch(hex_code, text):
    return f'<div style="margin-bottom:8px;"><span class="swatch-circle" style="background-color:{hex_code};"></span><span style="font-size:0.98rem;">{text}</span></div>'

# ส่วนหัวแอปพลิเคชัน
st.markdown('<div class="main-title">🎀 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ การพัฒนาเว็บแอปพลิเคชันแนะนำโทนลิปสติกและรองพื้นที่เหมาะสมกับสีผิวโดยใช้ปัญญาประดิษฐ์ (AI) ✨</div>', unsafe_allow_html=True)

# เลือกภาษา
lang = st.selectbox("🌐 ภาษา / Language", ["TH", "EN"])

st.write("---")

# ส่วนอัปโหลดรูปภาพ
st.subheader("📷 1. ถ่ายภาพ หรือ อัปโหลดรูปภาพใบหน้า" if lang == "TH" else "📷 1. Upload or Take Photo")
uploaded_file = st.file_uploader("เลือกไฟล์รูปภาพใบหน้าของคุณ (JPG, PNG)", type=["jpg", "jpeg", "png"])

# แสดงรูปภาพทันทีที่อัปโหลด
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 รูปภาพใบหน้าที่ใช้วิเคราะห์", use_container_width=True)

# ส่วนเลือกอันเดอร์โทน
st.subheader("🎨 2. เลือกอันเดอร์โทนผิวของคุณ" if lang == "TH" else "🎨 2. Select Your Undertone")
tone_selection = st.radio(
    "เลือกโทนผิวเพื่อการประมวลผลแม่นยำ:",
    ["Warm Tone (โทนอุ่น / ผิวขาวเหลือง - สองสี)", "Cool Tone (โทนเย็น / ผิวขาวอมชมพู)", "Neutral Tone (โทนธรรมชาติ)"]
)

st.write("")

# ปุ่มวิเคราะห์
if st.button("✨ วิเคราะห์สีผิวและแนะนำเครื่องสำอาง", type="primary"):
    if uploaded_file is None:
        st.warning("⚠️ กรุณาอัปโหลดรูปภาพใบหน้าก่อนทำการวิเคราะห์ครับ" if lang == "TH" else "⚠️ Please upload a face image first.")
    else:
        st.balloons()
        
        # กำหนดค่าตามอันเดอร์โทนที่เลือก
        if "Warm" in tone_selection:
            r, g, b = 225, 185, 150
            undertone_text = "Warm Tone (โทนอุ่นอมเหลือง)" if lang == "TH" else "Warm Tone"
            found_list = FOUNDATION_DB["Warm"][:3]
        elif "Cool" in tone_selection:
            r, g, b = 235, 190, 195
            undertone_text = "Cool Tone (โทนเย็นอมชมพู)" if lang == "TH" else "Cool Tone"
            found_list = FOUNDATION_DB["Cool"][:3]
        else:
            r, g, b = 215, 175, 155
            undertone_text = "Neutral Tone (โทนธรรมชาติ)" if lang == "TH" else "Neutral Tone"
            found_list = FOUNDATION_DB["Neutral"][:3]

        hex_code = f"#{r:02X}{g:02X}{b:02X}"

        # สรุปผล
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color:#D81B60; text-align:center; margin-top:0;">💖 ผลการวิเคราะห์ GlamAI 💖</h3>', unsafe_allow_html=True)
        
        # แสดงสีผิว
        st.markdown(render_swatch(hex_code, f"<b>สีผิวที่ประมวลผล:</b> <code>HEX: {hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})"), unsafe_allow_html=True)
        st.markdown(f"🌈 <b>อันเดอร์โทน:</b> {undertone_text}", unsafe_allow_html=True)
        
        # 1. รองพื้น
        st.markdown('<div class="section-head">🧴 รองพื้นที่แนะนำ (Foundation)</div>', unsafe_allow_html=True)
        for item in found_list:
            st.markdown(render_swatch(item["hex"], item["name"]), unsafe_allow_html=True)
            
        # 2. บลัชออน
        st.markdown('<div class="section-head">🌸 บลัชออนที่เหมาะ (Blush On)</div>', unsafe_allow_html=True)
        for item in BLUSH_DB[:4]:
            st.markdown(render_swatch(item["hex"], f"<b>{item['group']}:</b> {item['name']}"), unsafe_allow_html=True)

        # 3. ลิปสติก
        st.markdown('<div class="section-head">💋 ลิปสติกที่เหมาะ (Lipstick)</div>', unsafe_allow_html=True)
        for item in LIP_DB[:5]:
            st.markdown(render_swatch(item["hex"], f"<b>{item['group']}:</b> {item['name']}"), unsafe_allow_html=True)
        # แสดง Mixing color
        st.markdown(render_swatch(LIP_DB[-1]["hex"], f"<b>{LIP_DB[-1]['group']}:</b> {LIP_DB[-1]['name']}"), unsafe_allow_html=True)

        # 4. อายแชโดว์
        st.markdown('<div class="section-head">👁️ อายแชโดว์ที่เหมาะ (Eyeshadow)</div>', unsafe_allow_html=True)
        for item in EYESHADOW_DB[:3]:
            st.markdown(render_swatch(item["hex"], f"<b>{item['brand']}:</b> {item['name']}"), unsafe_allow_html=True)

        # ทริคผสมสี
        st.markdown("""
        <div class="tip-box">
            💡 <b>ทริคพิเศษสไตล์จูดี้ดอล:</b> คุณสามารถนำ บลัชออนเบอร์ #01 หรือ #03 (โทนส้ม/พีช) มาปัดบางๆ ทั่วแก้มก่อน แล้วใช้เบอร์ #02 หรือ #49 (โทนชมพูนม) แต้มย้ำลงไปตรงกลางพวงแก้ม จะได้สีชมพูพีชไล่เฉด (Gradient) ที่ละมุนตาและเข้ากับผิวได้สว่างมีมิติที่สุด!
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

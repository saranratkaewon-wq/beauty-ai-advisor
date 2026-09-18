import streamlit as st

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

    .info-box {
        background-color: #FFF0F3 !important;
        border-left: 4px solid #B85B74;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 20px;
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
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอาง
FOUNDATION_DB = {
    "Warm": [
        {"name_th": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "name_en": "00W (Warm Porcelain) — Very Fair Warm", "hex": "#F9E4D3"},
        {"name_th": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "name_en": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D2BA"},
        {"name_th": "02W (Warm Ivory) — ผิวขาวเหลืองถึงผิวสองสี โทนอุ่นอมเหลือง", "name_en": "02W (Warm Ivory) — Medium Warm", "hex": "#E9C7AA"}
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

st.markdown('<div class="main-title">🎀 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ Personal Color & Makeup Advisor ✨</div>', unsafe_allow_html=True)

lang = st.selectbox("🌐 เปลี่ยนภาษา / Select Language", ["TH (ไทย)", "EN (English)"])
is_th = "TH" in lang

st.write("---")

# ส่วนเลือกโทนสีผิว
if is_th:
    st.markdown('<div class="info-box"><b>🎨 ระบุโทนสีผิวของคุณเพื่อรับคำแนะนำ:</b></div>', unsafe_allow_html=True)
    tone_options = {
        "Warm Tone (ผิวสองสี / ผิวขาวเหลือง)": "Warm",
        "Cool Tone (ผิวขาว / ผิวอมชมพู)": "Cool",
        "Neutral Tone (ผิวโทนธรรมชาติ)": "Neutral"
    }
else:
    st.markdown('<div class="info-box"><b>🎨 Select your skin tone for recommendations:</b></div>', unsafe_allow_html=True)
    tone_options = {
        "Warm Tone (Medium / Yellow Skin)": "Warm",
        "Cool Tone (Fair / Pink Skin)": "Cool",
        "Neutral Tone (Natural Balanced Skin)": "Neutral"
    }

selected_label = st.radio(
    "เลือกโทนสีผิว" if is_th else "Select Skin Tone",
    list(tone_options.keys())
)

key = tone_options[selected_label]

# รายละเอียดข้อความสีผิวและสไตล์
if key == "Warm":
    skin_text = "ผิวสองสี / ผิวขาวเหลือง (Warm Tone)" if is_th else "Warm Tone (Medium / Yellow Skin)"
    style_desc = "เหมาะกับการแต่งหน้าโทนส้มพีช คอรัล ให้ลุคผิวบ่มแดดสดใส" if is_th else "Best with warm peach & coral tones."
elif key == "Cool":
    skin_text = "ผิวขาว / ผิวอมชมพู (Cool Tone)" if is_th else "Cool Tone (Fair / Pink Skin)"
    style_desc = "เหมาะกับการแต่งหน้าโทนชมพูนม ชมพูกุหลาบ ให้ลุคหน้าผ่อง สว่างใส สไตล์เกาหลี" if is_th else "Best with milky pink & rose tones."
else:
    skin_text = "ผิวโทนธรรมชาติ (Neutral Tone)" if is_th else "Neutral Tone (Natural Balanced Skin)"
    style_desc = "เหมาะกับการแต่งหน้าโทนชานม นู้ดเบจ สุภาพ เรียบหรู" if is_th else "Best with milk tea & rosy nude tones."

# แสดงผลการวิเคราะห์เฉพาะข้อความ (ไม่มีรูปตัวอย่างสีผิว)
st.markdown('<div class="result-card">', unsafe_allow_html=True)
res_head = "💖 รายการเครื่องสำอางแนะนำสำหรับคุณ 💖" if is_th else "💖 Recommended Makeup List 💖"
st.markdown(f'<h3 style="color:#B85B74; text-align:center; margin-top:0;">{res_head}</h3>', unsafe_allow_html=True)

st.markdown(f"🎨 <b>ระดับเฉดและอันเดอร์โทนสีผิว:</b> {skin_text}", unsafe_allow_html=True)
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

st.write("---")
if is_th:
    st.caption("⚠️ **ข้อแนะนำเพิ่มเติม:** แนะนำให้ทดลองปาดเนื้อผลิตภัณฑ์ (Swatch) บริเวณกรอบหน้า/สันกราม ก่อนตัดสินใจเลือกซื้อจริง")
else:
    st.caption("⚠️ **Note:** We recommend swatching shades along your jawline before purchasing.")

st.markdown('</div>', unsafe_allow_html=True)

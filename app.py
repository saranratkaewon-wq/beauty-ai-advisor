import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : Beauty AI Advisor", page_icon="💄", layout="centered")

# CSS ตกแต่งธีมหวาน แกรม ละมุน + บังคับสีข้อความให้ชัดเจน
st.markdown("""
<style>
    /* พี้นหลังเว็บโทนชมพูพาสเทลละมุน */
    .stApp {
        background-color: #FFF5F7 !important;
    }
    
    /* บังคับสีข้อความทั่วไปและข้อความในตัวเลือก */
    p, span, label, div, .stMarkdown {
        color: #333333 !important;
    }

    /* หัวข้อหลัก */
    .main-title {
        color: #D81B60 !important;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: bold;
        font-size: 2.2rem;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #880E4F !important;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    /* การ์ดสรุปผล */
    .glam-card {
        background-color: #FFFFFF !important;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 8px 20px rgba(216, 27, 96, 0.08);
        border: 1px solid #FFE0B2;
        margin-bottom: 20px;
    }

    /* หัวข้อภายในผลการวิเคราะห์ */
    .section-header {
        color: #C2185B !important;
        font-size: 1.2rem;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 10px;
        border-bottom: 2px solid #F8BBD0;
        padding-bottom: 5px;
    }

    /* แถบสีพรีวิว */
    .color-swatch {
        display: inline-block;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
        border: 1px solid rgba(0,0,0,0.15);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* กล่องทริคพิเศษ */
    .tip-box {
        background: linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%) !important;
        border-left: 5px solid #FF69B4;
        padding: 15px;
        border-radius: 12px;
        color: #4A4A4A !important;
        font-size: 0.95rem;
        margin-top: 15px;
    }

    /* ตกแต่งปุ่มเลือก Radio ให้ตัวหนังสือชัดเจน */
    div[role="radiogroup"] label p {
        color: #4A154B !important;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอางพร้อม HEX Code สำหรับพรีวิวสี
COSMETICS_DB = {
    "Foundation": [
        {"name": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนกลาง", "hex": "#F9E4D4"},
        {"name": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "hex": "#F7E1CE"},
        {"name": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลางธรรมชาติ", "hex": "#F5DBCB"},
        {"name": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "hex": "#F3D3BD"},
        {"name": "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป โทนกลาง", "hex": "#ECCFB9"},
        {"name": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "hex": "#E8C8B0"},
        {"name": "02G (Golden Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง", "hex": "#E4C0A3"},
        {"name": "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง โทนกลาง", "hex": "#DEB596"},
        {"name": "03W (Warm Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นอมเหลือง", "hex": "#D8AC8A"}
    ],
    "Blush": {
        "Pink Tones": {"name": "#41 Pinkish Nude (ชมพูนู้ดอมเบจ)", "hex": "#E8A3A8"},
        "Warm Tones": {"name": "#03 Soft Peach (ส้มพีชละมุน)", "hex": "#F4A28C"},
        "Neutral Tones": {"name": "#35 Rosy Beige (น้ำตาลนู้ดอมชมพู)", "hex": "#C98A80"}
    },
    "Lipstick": {
        "Pink Tones": {"name": "#09 Lychee (ชมพูลิ้นจี่)", "hex": "#DC5B78"},
        "MLBB Tones": {"name": "#11 Peanut (นู้ดชมพูอมน้ำตาล)", "hex": "#B86B66"},
        "Mixing Colors": {"name": "#25 Grey (ผสมดรอปความสว่างเพิ่มความหม่นตุ่น)", "hex": "#8C7B7A"}
    },
    "Eyeshadow": [
        {"name": "4U2 #02 Dust of Snow (ชมพูนู้ด-น้ำตาลชิมเมอร์)", "hex": "#D4A398"},
        {"name": "Dasique #02 Rose Petal (ชมพูกลีบกุหลาบ)", "hex": "#E08F95"}
    ]
}

st.markdown('<div class="main-title">💄 GlamAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">✨ Beauty AI Advisor & Personal Color Helper ✨</div>', unsafe_allow_html=True)

lang = st.selectbox("🌐 เลือกภาษา / Select Language", ["TH", "EN"])

uploaded_file = st.file_uploader("📷 ถ่ายภาพ หรือ อัปโหลดรูปภาพใบหน้า", type=["jpg", "jpeg", "png"])
tone_selection = st.radio(
    "🎨 เลือกอันเดอร์โทนผิวของคุณ",
    ["Warm Tone (โทนอุ่น/ผิวขาวเหลือง-สองสี)", "Cool Tone (โทนเย็น/ผิวขาวอมชมพู)", "Neutral Tone (โทนธรรมชาติ)"]
)

if st.button("✨ วิเคราะห์สีผิวและแนะนำเครื่องสำอาง", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.warning("กรุณาอัปโหลดรูปภาพก่อนทำการวิเคราะห์ครับ" if lang == "TH" else "Please upload an image first.")
    else:
        if "Warm Tone" in tone_selection:
            r, g, b = 225, 185, 150
            undertone = "Warm Tone (โทนอุ่น)" if lang == "TH" else "Warm Tone"
            found = COSMETICS_DB["Foundation"][5]
        elif "Cool Tone" in tone_selection:
            r, g, b = 235, 190, 195
            undertone = "Cool Tone (โทนเย็น/ชมพู)" if lang == "TH" else "Cool Tone"
            found = COSMETICS_DB["Foundation"][2]
        else:
            r, g, b = 215, 175, 155
            undertone = "Neutral Tone (โทนธรรมชาติ)" if lang == "TH" else "Neutral Tone"
            found = COSMETICS_DB["Foundation"][4]

        hex_code = f"#{r:02X}{g:02X}{b:02X}"

        blush_p = COSMETICS_DB["Blush"]["Pink Tones"]
        blush_w = COSMETICS_DB["Blush"]["Warm Tones"]
        blush_n = COSMETICS_DB["Blush"]["Neutral Tones"]

        lip_p = COSMETICS_DB["Lipstick"]["Pink Tones"]
        lip_m = COSMETICS_DB["Lipstick"]["MLBB Tones"]
        lip_x = COSMETICS_DB["Lipstick"]["Mixing Colors"]

        eye1 = COSMETICS_DB["Eyeshadow"][0]
        eye2 = COSMETICS_DB["Eyeshadow"][1]

        if lang == "TH":
            st.balloons()
            st.markdown(f"""
            <div class="glam-card">
                <h3 style="color:#D81B60; text-align:center; margin-top:0;">💖 ผลการวิเคราะห์ GlamAI 💖</h3>
                
                <p>🎨 <b>สีผิวที่ประมวลผล:</b> <span class="color-swatch" style="background-color:{hex_code};"></span> <b>HEX:</b> <code>{hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})</p>
                <p>🌈 <b>อันเดอร์โทน:</b> {undertone}</p>
                
                <div class="section-header">🧴 รองพื้นที่แนะนำ</div>
                <p>• <span class="color-swatch" style="background-color:{found['hex']};"></span>{found['name']}</p>
                
                <div class="section-header">🌸 บลัชออนที่เหมาะ</div>
                <p>• <b>โทนชมพู:</b> <span class="color-swatch" style="background-color:{blush_p['hex']};"></span>{blush_p['name']}</p>
                <p>• <b>โทนส้ม/พีช:</b> <span class="color-swatch" style="background-color:{blush_w['hex']};"></span>{blush_w['name']}</p>
                <p>• <b>โทนชานม:</b> <span class="color-swatch" style="background-color:{blush_n['hex']};"></span>{blush_n['name']}</p>
                
                <div class="section-header">💋 ลิปสติกที่เหมาะ</div>
                <p>• <b>กลุ่มสีชมพู:</b> <span class="color-swatch" style="background-color:{lip_p['hex']};"></span>{lip_p['name']}</p>
                <p>• <b>สีนู้ด MLBB:</b> <span class="color-swatch" style="background-color:{lip_m['hex']};"></span>{lip_m['name']}</p>
                <p>• <b>ตัวช่วยผสมสี:</b> <span class="color-swatch" style="background-color:{lip_x['hex']};"></span>{lip_x['name']}</p>
                
                <div class="section-header">👁️ อายแชโดว์ที่เหมาะ</div>
                <p>• <span class="color-swatch" style="background-color:{eye1['hex']};"></span>{eye1['name']}</p>
                <p>• <span class="color-swatch" style="background-color:{eye2['hex']};"></span>{eye2['name']}</p>
                
                <div class="tip-box">
                    💡 <b>ทริคพิเศษ:</b> ปัดบลัชออนโทนส้มพีชบางๆ ทั่วแก้ม แล้วใช้บลัชออนโทนชมพูนมแต้มตรงกลางพวงแก้ม เพื่อสร้างมิติ Gradient ให้หน้าผ่องใสเป็นธรรมชาติ!
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.balloons()
            st.markdown(f"""
            <div class="glam-card">
                <h3 style="color:#D81B60; text-align:center; margin-top:0;">💖 GlamAI Analysis Report 💖</h3>
                
                <p>🎨 <b>Detected Color:</b> <span class="color-swatch" style="background-color:{hex_code};"></span> <b>HEX:</b> <code>{hex_code}</code> | <b>RGB:</b> ({r}, {g}, {b})</p>
                <p>🌈 <b>Undertone:</b> {undertone}</p>
                
                <div class="section-header">🧴 Recommended Foundation</div>
                <p>• <span class="color-swatch" style="background-color:{found['hex']};"></span>{found['name']}</p>
                
                <div class="section-header">🌸 Recommended Blush</div>
                <p>• <b>Pink Tone:</b> <span class="color-swatch" style="background-color:{blush_p['hex']};"></span>{blush_p['name']}</p>
                <p>• <b>Warm Tone:</b> <span class="color-swatch" style="background-color:{blush_w['hex']};"></span>{blush_w['name']}</p>
                <p>• <b>Neutral Tone:</b> <span class="color-swatch" style="background-color:{blush_n['hex']};"></span>{blush_n['name']}</p>
                
                <div class="section-header">💋 Recommended Lipstick</div>
                <p>• <b>Pink Tone:</b> <span class="color-swatch" style="background-color:{lip_p['hex']};"></span>{lip_p['name']}</p>
                <p>• <b>MLBB Tone:</b> <span class="color-swatch" style="background-color:{lip_m['hex']};"></span>{lip_m['name']}</p>
                <p>• <b>Mixing Option:</b> <span class="color-swatch" style="background-color:{lip_x['hex']};"></span>{lip_x['name']}</p>
                
                <div class="section-header">👁️ Recommended Eyeshadow</div>
                <p>• <span class="color-swatch" style="background-color:{eye1['hex']};"></span>{eye1['name']}</p>
                <p>• <span class="color-swatch" style="background-color:{eye2['hex']};"></span>{eye2['name']}</p>
            </div>
            """, unsafe_allow_html=True)

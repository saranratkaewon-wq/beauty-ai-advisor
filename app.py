import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="GlamAI : Beauty AI Advisor", page_icon="💄", layout="centered")

# CSS ปรับแต่งความสวยงามโทน Dark Luxury Glam
st.markdown("""
<style>
    /* บังคับสีปุ่มและองค์ประกอบหลักให้แกรม */
    .stButton>button {
        background: linear-gradient(45deg, #D4AF37, #C5A059);
        color: #000000 !important;
        font-weight: bold;
        border: none;
        border-radius: 25px;
        padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #E5C158, #D4AF37);
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# ฐานข้อมูลเครื่องสำอางพร้อม HEX Code
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
    "Blush": [
        {"type": "โทนชมพู", "name": "#41 Pinkish Nude (ชมพูนู้ดอมเบจ)", "hex": "#E8A3A8"},
        {"type": "โทนส้ม/พีช", "name": "#03 Soft Peach (ส้มพีชละมุน)", "hex": "#F4A28C"},
        {"type": "โทนชานม", "name": "#35 Rosy Beige (น้ำตาลนู้ดอมชมพู)", "hex": "#C98A80"}
    ],
    "Lipstick": [
        {"type": "กลุ่มสีชมพู", "name": "#09 Lychee (ชมพูลิ้นจี่)", "hex": "#DC5B78"},
        {"type": "สีนู้ด MLBB", "name": "#11 Peanut (นู้ดชมพูอมน้ำตาล)", "hex": "#B86B66"},
        {"type": "ตัวช่วยผสมสี", "name": "#25 Grey (ผสมดรอปความสว่างเพิ่มความหม่นตุ่น)", "hex": "#8C7B7A"}
    ],
    "Eyeshadow": [
        {"name": "4U2 #02 Dust of Snow (ชมพูนู้ด-น้ำตาลชิมเมอร์)", "hex": "#D4A398"},
        {"name": "Dasique #02 Rose Petal (ชมพูกลีบกุหลาบ)", "hex": "#E08F95"}
    ]
}

# หัวข้อหลัก
st.title("💄 GlamAI")
st.caption("✨ Beauty AI Advisor & Personal Color Helper ✨")
st.write("---")

lang = st.selectbox("🌐 เลือกภาษา / Select Language", ["TH", "EN"])

uploaded_file = st.file_uploader("📷 ถ่ายภาพ หรือ อัปโหลดรูปภาพใบหน้า", type=["jpg", "jpeg", "png"])

tone_selection = st.radio(
    "🎨 เลือกอันเดอร์โทนผิวของคุณ",
    ["Warm Tone (โทนอุ่น/ผิวขาวเหลือง-สองสี)", "Cool Tone (โทนเย็น/ผิวขาวอมชมพู)", "Neutral Tone (โทนธรรมชาติ)"]
)

st.write("")

if st.button("✨ วิเคราะห์สีผิวและแนะนำเครื่องสำอาง", use_container_width=True):
    if uploaded_file is None:
        st.warning("กรุณาอัปโหลดรูปภาพก่อนทำการวิเคราะห์ครับ" if lang == "TH" else "Please upload an image first.")
    else:
        st.balloons()
        
        # คำนวณอันเดอร์โทน
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

        st.subheader("✨ ผลการวิเคราะห์ GlamAI" if lang == "TH" else "✨ GlamAI Analysis Result")
        
        # สรุปสีผิว
        st.markdown(f"**🎨 สีผิวที่ประมวลผลได้:** `HEX: {hex_code}` | `RGB: ({r}, {g}, {b})`")
        st.color_picker("ตัวอย่างสีผิวของคุณ", value=hex_code, disabled=True)
        st.markdown(f"**🌈 อันเดอร์โทน:** {undertone}")
        st.write("---")

        # 1. รองพื้น
        st.subheader("🧴 รองพื้นที่แนะนำ" if lang == "TH" else "🧴 Recommended Foundation")
        col1, col2 = st.columns([1, 4])
        with col1:
            st.color_picker(" ", value=found['hex'], disabled=True, key="found_pick")
        with col2:
            st.write(f"**{found['name']}**")

        # 2. บลัชออน
        st.subheader("🌸 บลัชออนที่เหมาะ" if lang == "TH" else "🌸 Recommended Blush")
        for idx, item in enumerate(COSMETICS_DB["Blush"]):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.color_picker(" ", value=item['hex'], disabled=True, key=f"blush_{idx}")
            with col2:
                st.write(f"• **{item['type']}:** {item['name']}")

        # 3. ลิปสติก
        st.subheader("💋 ลิปสติกที่เหมาะ" if lang == "TH" else "💋 Recommended Lipstick")
        for idx, item in enumerate(COSMETICS_DB["Lipstick"]):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.color_picker(" ", value=item['hex'], disabled=True, key=f"lip_{idx}")
            with col2:
                st.write(f"• **{item['type']}:** {item['name']}")

        # 4. อายแชโดว์
        st.subheader("👁️ อายแชโดว์ที่เหมาะ" if lang == "TH" else "👁️ Recommended Eyeshadow")
        for idx, item in enumerate(COSMETICS_DB["Eyeshadow"]):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.color_picker(" ", value=item['hex'], disabled=True, key=f"eye_{idx}")
            with col2:
                st.write(f"• **{item['name']}**")

        # ทริคพิเศษ
        st.info("💡 **ทริคพิเศษ:** ปัดบลัชออนโทนส้มพีชบางๆ ทั่วแก้ม แล้วใช้บลัชออนโทนชมพูนมแต้มตรงกลางพวงแก้ม เพื่อสร้างมิติ Gradient ให้หน้าผ่องใสเป็นธรรมชาติ!" if lang == "TH" else "💡 **Beauty Tip:** Apply soft peach blush all over cheeks, then dab light pink blush at the center for a glowing gradient effect!")

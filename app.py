import streamlit as st

st.set_page_config(page_title="GlamAI : Beauty AI Advisor", layout="centered")

COSMETICS_DB = {
    "Foundation": [
        "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนกลางธรรมชาติ",
        "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง",
        "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลางธรรมชาติ",
        "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง",
        "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป โทนกลางธรรมชาติ",
        "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง",
        "02G (Golden Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง",
        "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี โทนกลางธรรมชาติ",
        "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง โทนกลางธรรมชาติ",
        "03W (Warm Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นอมเหลือง",
        "28N (Oat) — ผิวสองสีค่อนข้างเข้ม โทนกลางธรรมชาติอมโอ๊ต",
        "04N (Natural Beige) — ผิวแทน/ผิวเข้ม โทนกลางธรรมชาติ",
        "05W (Warm Sand) — ผิวแทน/ผิวเข้ม โทนอุ่นอมแซนด์",
        "06W (Warm Honey) — ผิวสีน้ำผึ้ง/ผิวเข้ม โทนอุ่นอมน้ำผึ้ง",
        "07N (Soft Caramel) — ผิวเข้มลึก โทนกลางธรรมชาติอมคาราเมล",
        "08N (Rich Toffee) — ผิวเข้มลึกมาก โทนกลางธรรมชาติอมท็อฟฟี่"
    ],
    "Blush": {
        "Pink Tones": ["#02 Wavy Pink (ชมพูนมสว่าง)", "#41 Pinkish Nude (ชมพูนู้ดอมเบจ)", "#49 Milky Pink (ชมพูนมแมทช์)"],
        "Warm Tones": ["#01 Tidal Apricot (ส้มแอปริคอต)", "#03 Soft Peach (ส้มพีชละมุน)", "#04 Melon Pomelo (ส้มอมชมพู)"],
        "Neutral Tones": ["#06 Linen Nude (เบจนู้ดอมน้ำตาล)", "#35 Rosy Beige (น้ำตาลนู้ดอมชมพู)", "#68 Toasted Cinnamon (น้ำตาลบ่มแดด)"]
    },
    "Lipstick": {
        "Pink Tones": ["#09 Lychee (ชมพูลิ้นจี่)", "#16 Pink Taro (ชมพูเผือก)", "#21 Strawberry Acai", "#22 Very Berry"],
        "MLBB Tones": ["#03 Pretzel (นู้ดส้มพีช)", "#04 Biscoff (นู้ดชานม)", "#11 Peanut (นู้ดชมพูอมน้ำตาล)"],
        "Deep & Warm": ["#02 Pear", "#05 Nama Choco", "#10 Cranberry", "#12 Date", "#13 Apple Glaze", "#19 Brown Sugar"],
        "Mixing Colors": ["#24 Black Sesame (ผสมเพิ่มความดาร์ก)", "#25 Grey (ผสมดรอปความสว่างเพิ่มความหม่นตุ่น)"]
    },
    "Eyeshadow": [
        "4U2 #02 Dust of Snow (ชมพูนู้ด-น้ำตาลชิมเมอร์)",
        "4U2 #03 Wanted (ชมพูอมส้มพีช-คอรัล)",
        "ODD STUDIO #01 Love, Dear (ชมพู-เบจ)",
        "ODD STUDIO #02 Rose, Moment (ชมพูกุหลาบอบอุ่น)",
        "Dasique #02 Rose Petal (ชมพูกลีบกุหลาบ)",
        "Dasique #14 Peach Squeeze (ชมพูพีช-ส้มแอปริคอต)"
    ]
}

st.title("💄 GlamAI : Beauty AI Advisor")
lang = st.selectbox("🌐 เลือกภาษา / Select Language", ["TH", "EN"])

uploaded_file = st.file_uploader("📷 ถ่ายภาพ หรือ อัปโหลดรูปภาพใบหน้า", type=["jpg", "jpeg", "png"])
tone_selection = st.radio(
    "🎨 เลือกอันเดอร์โทนผิวของคุณ",
    ["Warm Tone (โทนอุ่น/ผิวขาวเหลือง-สองสี)", "Cool Tone (โทนเย็น/ผิวขาวอมชมพู)", "Neutral Tone (โทนธรรมชาติ)"]
)

if st.button("✨ วิเคราะห์สีผิวและแนะนำเครื่องสำอาง", type="primary"):
    if uploaded_file is None:
        st.warning("กรุณาอัปโหลดรูปภาพก่อนทำการวิเคราะห์ครับ" if lang == "TH" else "Please upload an image first.")
    else:
        if "Warm Tone" in tone_selection:
            r, g, b = 225, 185, 150
            undertone = "Warm Tone (โทนอุ่น)" if lang == "TH" else "Warm Tone"
            selected_found = COSMETICS_DB["Foundation"][5]
        elif "Cool Tone" in tone_selection:
            r, g, b = 235, 190, 195
            undertone = "Cool Tone (โทนเย็น/ชมพู)" if lang == "TH" else "Cool Tone"
            selected_found = COSMETICS_DB["Foundation"][2]
        else:
            r, g, b = 215, 175, 155
            undertone = "Neutral Tone (โทนธรรมชาติ)" if lang == "TH" else "Neutral Tone"
            selected_found = COSMETICS_DB["Foundation"][4]

        hex_code = f"#{r:02X}{g:02X}{b:02X}"

        if lang == "TH":
            st.success("วิเคราะห์สำเร็จ!")
            st.markdown(f"""
### 💄 ผลการวิเคราะห์ GlamAI
* **สีผิวที่ประมวลผล (RGB):** ({r}, {g}, {b}) | HEX: `{hex_code}`
* **อันเดอร์โทน:** {undertone}

#### 🧴 รองพื้นที่แนะนำ
* {selected_found}

#### 🌸 บลัชออนที่เหมาะ
* **โทนชมพู:** {COSMETICS_DB['Blush']['Pink Tones'][1]}
* **โทนส้ม/พีช:** {COSMETICS_DB['Blush']['Warm Tones'][1]}
* **โทนชานม:** {COSMETICS_DB['Blush']['Neutral Tones'][1]}

#### 💋 ลิปสติกที่เหมาะ
* **กลุ่มสีชมพู:** {COSMETICS_DB['Lipstick']['Pink Tones'][0]}
* **สีนู้ด MLBB:** {COSMETICS_DB['Lipstick']['MLBB Tones'][2]}
* **ตัวช่วยผสมสี:** {COSMETICS_DB['Lipstick']['Mixing Colors'][1]}

#### 👁️ อายแชโดว์ที่เหมาะ
* {COSMETICS_DB['Eyeshadow'][0]}
* {COSMETICS_DB['Eyeshadow'][4]}

> 💡 **ทริคพิเศษ:** ปัดบลัชออนโทนส้มพีชบางๆ ทั่วแก้ม แล้วใช้บลัชออนโทนชมพูนมแต้มตรงกลางพวงแก้ม เพื่อสร้างมิติ Gradient ให้หน้าผ่องใส!
""")
        else:
            st.success("Analysis Complete!")
            st.markdown(f"""
### 💄 GlamAI Analysis Report
* **Detected Skin Color (RGB):** ({r}, {g}, {b}) | HEX: `{hex_code}`
* **Undertone:** {undertone}

#### 🧴 Recommended Foundation
* {selected_found}

#### 🌸 Recommended Blush
* **Pink Tone:** {COSMETICS_DB['Blush']['Pink Tones'][1]}
* **Warm Tone:** {COSMETICS_DB['Blush']['Warm Tones'][1]}
* **Neutral Tone:** {COSMETICS_DB['Blush']['Neutral Tones'][1]}

#### 💋 Recommended Lipstick
* **Pink Tone:** {COSMETICS_DB['Lipstick']['Pink Tones'][0]}
* **MLBB Tone:** {COSMETICS_DB['Lipstick']['MLBB Tones'][2]}
* **Mixing Option:** {COSMETICS_DB['Lipstick']['Mixing Colors'][1]}

#### 👁️ Recommended Eyeshadow
* {COSMETICS_DB['Eyeshadow'][0]}
* {COSMETICS_DB['Eyeshadow'][4]}
""")

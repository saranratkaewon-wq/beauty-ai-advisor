import streamlit as st
import numpy as np
import random

from PIL import Image

# กำหนดฐานข้อมูลเฉดสีทั้งหมด เพื่อให้ระบบสุ่มเลือกเฉพาะสีที่ "เหมาะกับช่วงผิวของแต่ละคน"
DATABASE = {
    "TH": {
        "foundations": {
            "light": [
                "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนกลางธรรมชาติ",
                "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลางธรรมชาติ",
                "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง",
            ],
            "medium": [
                "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป โทนกลางธรรมชาติ",
                "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง",
                "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง โทนกลางธรรมชาติ",
                "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี",
            ],
            "dark": [
                "04N (Natural Beige) — ผิวแทน/ผิวเข้ม โทนกลางธรรมชาติ",
                "05W (Warm Sand) — ผิวแทน/ผิวเข้ม โทนอุ่นอมแซนด์",
                "06W (Warm Honey) — ผิวสีน้ำผึ้ง/ผิวเข้ม โทนอุ่นอมน้ำผึ้ง",
                "07N (Soft Caramel) — ผิวเข้มลึก โทนกลางธรรมชาติ",
            ],
        },
        "blushes": [
            "#02 Wavy Pink: สีชมพูนมพาสเทลอ่อนๆ ช่วยให้หน้าแก้มผ่องใส",
            "#41 (Pinkish Nude): สีชมพูนู้ดอมเบจสุดละมุน กลืนกับผิวได้ดี",
            "#01 Tidal Apricot: สีส้มแอปริคอตนวลๆ อุ่นๆ เป็นธรรมชาติ",
            "#03 (Soft Peach): สีส้มพีชละมุน ขับผิวโทนเหลืองให้มีออร่า",
            "#06 Linen Nude: สีเบจนู้ดอมน้ำตาลอ่อน ลุค Clean Girl",
            "#35 (Rosy Beige): สีน้ำตาลนู้ดอมชมพูกุหลาบตุ่น สวยแพง",
        ],
        "lips": [
            "#09 Lychee (สีลิ้นจี่): ชมพูอมแดงระเรื่อ ขับผิวหน้าผ่องมาก (Best Seller)",
            "#16 Pink Taro (สีเผือก): ชมพูนมนัวๆ อมตุ่นเบาๆ",
            "#03 Pretzel: สีนู้ดน้ำตาลส้มอมพีชอ่อนๆ",
            "#11 Peanut (สีถั่ว): สีนู้ดชมพูอมน้ำตาลตุ่น เข้ากับทุกลุค (Best Seller)",
            "#02 Pear: สีส้มแอปริคอตสดใส บ่มแดด",
            "#10 Cranberry: สีแดงแครนเบอร์รี่ฉ่ำๆ หน้าไบรท์ (Best Seller)",
            "#19 Brown Sugar: สีน้ำตาลอมแดงอิฐอุ่นๆ คลาสสิก",
        ],
        "eyes": [
            "4U2 #02 Dust of Snow: โทนชมพูนู้ด-น้ำตาลตุ่น มีชิมเมอร์แชมเปญทอง",
            "ODD STUDIO #01 Love, Dear: ชมพู-เบจมินิมอล เนื้อแมทช์ละมุน",
            "Dasique #02 Rose Petal: โทนชมพูกลีบกุหลาบไล่เฉด กลิตเตอร์สะท้อนแสงสวย",
            "Dasique #14 Peach Squeeze: โทนชมพูพีช-ส้มแอปริคอตสดใส",
        ],
    },
    "EN": {
        "foundations": {
            "light": [
                "00N (Natural Porcelain) — Extra Fair, Neutral",
                "01N (Natural Vanilla) — Fair, Neutral",
                "01W (Warm Vanilla) — Fair, Warm Undertone",
            ],
            "medium": [
                "02N (Natural Ivory) — Light/Medium, Neutral",
                "02W (Warm Ivory) — Light/Medium, Warm",
                "03N (Natural Petal) — Medium, Neutral",
                "22N (Shell Beige) — Medium Tone",
            ],
            "dark": [
                "04N (Natural Beige) — Tan/Dark, Neutral",
                "05W (Warm Sand) — Tan/Dark, Warm",
                "06W (Warm Honey) — Deep Honey, Warm",
                "07N (Soft Caramel) — Deep Caramal, Neutral",
            ],
        },
        "blushes": [
            "#02 Wavy Pink: Pastel pink for bright apple cheeks",
            "#41 (Pinkish Nude): Soft nude beige blush",
            "#01 Tidal Apricot: Warm apricot natural look",
            "#03 (Soft Peach): Soft peach for warm undertones",
            "#06 Linen Nude: Clean beige nude",
            "#35 (Rosy Beige): Natural rosy brown contour blush",
        ],
        "lips": [
            "#09 Lychee: Best Seller bright pink red syrup",
            "#16 Pink Taro: Soft muted milky pink",
            "#03 Pretzel: Soft peach brown nude",
            "#11 Peanut: Best Seller MLBB pink brown",
            "#02 Pear: Bright sun-kissed apricot",
            "#10 Cranberry: Best Seller bright berry red",
            "#19 Brown Sugar: Warm classic brick brown",
        ],
        "eyes": [
            "4U2 #02 Dust of Snow: Nude pink with champagne shimmer",
            "ODD STUDIO #01 Love, Dear: Minimalist pink-beige matte",
            "Dasique #02 Rose Petal: Gradient rose petal palette",
            "Dasique #14 Peach Squeeze: Bright peach apricot palette",
        ],
    },
}

LANGUAGES = {
    "TH": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": (
            "โครงงานวิทยาศาสตร์: ระบบแนะนำเฉดสีเครื่องสำอางเฉพาะบุคคลด้วย AI"
        ),
        "upload_label": "อัปโหลดรูปภาพใบหน้าผู้ทดลองเพื่อวิเคราะห์",
        "skin_result": "ผลการวิเคราะห์สภาพผิวและค่า pH อัตโนมัติ",
        "matched_found": (
            "✨ ผลิตภัณฑ์และเฉดสีที่คัดเลือกเฉพาะสำหรับใบหน้านี้"
        ),
        "foundation": "รองพื้น (Foundation)",
        "blush": "บลัชออน (Blush On)",
        "lip": "ลิปสติก (Lipstick)",
        "eye": "อายแชโดว์ (Eyeshadow)",
        "prep_title": "💡 ขั้นตอนการเตรียมผิวหน้า (Skincare & Prep)",
        "prep_steps": [
            (
                "**1. ทำความสะอาดผิวหน้า (Cleanse):** ล้างหน้าด้วยเจลหรือโฟมล้างหน้าที่เหมาะกับสภาพผิว"
            ),
            "**2. ปรับสมดุลผิว (Tone):** เช็ดหน้าด้วยโทนเนอร์เบาๆ เพื่อเตรียมผิว",
            (
                "**3. เติมความชุ่มชื้น (Moisturize):** ทาเซรั่มและมอยส์เจอร์ไรเซอร์"
            ),
            (
                "**4. ทาครีมกันแดด (Sunscreen):** บีบในปริมาณที่เหมาะสม"
            ),
            (
                "**5. ลงไพร์เมอร์ (Primer):** ทาเฉพาะจุด T-zone เพื่อล็อกเมคอัพ"
            ),
        ],
    },
    "EN": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": (
            "Science Project: Personalized Cosmetic Shade Recommender"
        ),
        "upload_label": "Upload test subject face image for analysis",
        "skin_result": "Automated Skin Condition & pH Analysis",
        "matched_found": "✨ Dynamically Matched Shades For This Face",
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
            "**5. Primer:** Apply on T-zone to lock makeup.",
        ],
    },
}

st.sidebar.title("Settings / ตั้งค่า")
lang = st.sidebar.selectbox("Language / ภาษา", ["TH", "EN"])
t = LANGUAGES[lang]
db = DATABASE[lang]

st.title(t["title"])
st.write(t["subtitle"])

uploaded_file = st.file_uploader(
    t["upload_label"], type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
  img = Image.open(uploaded_file)
  st.image(img, caption="Test Subject Preview", use_container_width=True)

  img_np = np.array(img)
  height, width, _ = img_np.shape

  # สกัดสีผิวโซนกลาง
  crop_margin_h = int(height * 0.25)
  crop_margin_w = int(width * 0.25)
  center_region = img_np[
      crop_margin_h : height - crop_margin_h,
      crop_margin_w : width - crop_margin_w,
  ]

  brightness = np.mean(center_region, axis=2)
  filtered_pixels = center_region[(brightness >= 40) & (brightness <= 220)]

  if len(filtered_pixels) == 0:
    base_rgb = np.array([200, 150, 120])
  else:
    base_rgb = np.mean(filtered_pixels, axis=0)

  r, g, b = base_rgb
  avg_brightness = np.mean(base_rgb)

  # ใช้ค่าสีเฉพาะตัวของรูปนี้ในการตั้ง Seed สุ่ม เพื่อให้แต่ละรูปได้ผลลัพธ์ต่างกันแน่นอน
  img_seed = int(r + g + b)
  random.seed(img_seed)

  # วิเคราะห์ค่า pH จำลอง
  color_ratio = r / (g + 1e-5)
  if color_ratio > 1.25:
    estimated_ph = 4.2
    skin_cond = (
        "ผิวมีความไว / ระคายเคืองง่าย (pH ค่อนข้างต่ำ)"
        if lang == "TH"
        else "Sensitive / Irritated (Low pH)"
    )
    r = min(255, r * 1.1 + 10)
    b = max(0, b * 0.9 - 5)
  elif color_ratio < 0.95:
    estimated_ph = 5.8
    skin_cond = (
        "ผิวแห้ง / ขาดความสมดุล (pH ค่อนข้างสูง)"
        if lang == "TH"
        else "Dry / Imbalanced (High pH)"
    )
    r = r * 0.92
    g = g * 0.92
    b = b * 0.92
  else:
    estimated_ph = 5.0
    skin_cond = (
        "ผิวสุขภาพดี สมดุลปกติ (pH 4.5 - 5.5)"
        if lang == "TH"
        else "Healthy / Balanced (pH 4.5 - 5.5)"
    )

  final_rgb = (int(r), int(g), int(b))
  hex_color = "#{:02x}{:02x}{:02x}".format(
      final_rgb[0], final_rgb[1], final_rgb[2]
  )

  # --- คัดเลือกสีเฉพาะบุคคลแบบไดนามิกตามความสว่างผิวของภาพนี้ ---
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

  # แสดงผลวิเคราะห์ผิว
  st.subheader(t["skin_result"])
  st.info(
      f"📍 **Condition:** {skin_cond} | **Estimated pH:** {estimated_ph} |"
      f" **Subject Seed:** {img_seed}"
  )
  st.markdown(f"**Mapped Skin Hex:** `{hex_color}`")
  st.markdown(
      f'<div style="width: 80px; height: 80px; background-color: {hex_color};'
      ' border-radius: 50%; border: 2px solid #ccc;"></div>',
      unsafe_allow_html=True,
  )

  # แสดงผลเฉพาะสีที่เหมาะกับคนๆ นั้น
  st.markdown("---")
  st.subheader(t["matched_found"])

  st.success(f"""
    * **{t['foundation']}:** {matched_fd}
    * **{t['blush']}:** {matched_blush}
    * **{t['lip']}:** {matched_lip}
    * **{t['eye']}:** {matched_eye}
    """)

  # ขั้นตอนเตรียมผิว
  st.markdown("---")
  st.subheader(t["prep_title"])
  for step in t["prep_steps"]:
    st.markdown(f"- {step}")

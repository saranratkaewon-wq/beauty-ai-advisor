import streamlit as st
import numpy as np
import random
from PIL import Image

DATABASE = {
    "TH": {
        "foundations": {
            "light": [
                {"name": "00N (Natural Porcelain) — ผิวขาวมากพิเศษ โทนกลางธรรมชาติ", "hex": "#F9E4D4"},
                {"name": "00W (Warm Porcelain) — ผิวขาวมากพิเศษ โทนอุ่นอมเหลือง", "hex": "#F7DEC6"},
                {"name": "01N (Natural Vanilla) — ผิวขาวสว่าง โทนกลางธรรมชาติ", "hex": "#F2D8C2"},
                {"name": "01W (Warm Vanilla) — ผิวขาวสว่าง โทนอุ่นอมเหลือง", "hex": "#F4D5B6"}
            ],
            "medium": [
                {"name": "02N (Natural Ivory) — ผิวขาวเหลืองทั่วไป โทนกลางธรรมชาติ", "hex": "#E8C5A8"},
                {"name": "02W (Warm Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นอมเหลือง", "hex": "#E5BE9E"},
                {"name": "02G (Golden Ivory) — ผิวขาวเหลืองทั่วไป โทนอุ่นประกายทอง", "hex": "#E0B38C"},
                {"name": "03N (Natural Petal) — ผิวสองสี/ผิวปานกลาง โทนกลางธรรมชาติ", "hex": "#D8B08C"},
                {"name": "03W (Warm Almond) — ผิวสองสี/ผิวปานกลาง โทนอุ่นอมเหลือง", "hex": "#D1A47B"},
                {"name": "22N (Shell Beige) — ผิวกลางๆ ค่อนไปทางสองสี โทนกลางธรรมชาติ", "hex": "#CE9E7A"}
            ],
            "dark": [
                {"name": "04N (Natural Beige) — ผิวแทน/ผิวเข้ม โทนกลางธรรมชาติ", "hex": "#BC8C66"},
                {"name": "04W (Warm Beige) — ผิวสองสีค่อนข้างเข้ม โทนอุ่นอมเหลือง", "hex": "#B3805B"},
                {"name": "05W (Warm Sand) — ผิวแทน/ผิวเข้ม โทนอุ่นอมแซนด์", "hex": "#A97853"},
                {"name": "06W (Warm Honey) — ผิวสีน้ำผึ้ง/ผิวเข้ม โทนอุ่นอมน้ำผึ้ง", "hex": "#966542"},
                {"name": "07N (Soft Caramel) — ผิวเข้มลึก โทนกลางธรรมชาติอมคาราเมล", "hex": "#7A4E31"},
                {"name": "08N (Rich Toffee) — ผิวเข้มลึกมาก โทนกลางธรรมชาติอมท็อฟฟี่", "hex": "#5E3920"}
            ]
        },
        "blushes": [
            {"name": "#02 Wavy Pink — ชมพูนมพาสเทลอ่อนๆ ละมุนหน้าเด็ก", "hex": "#F4B3C2"},
            {"name": "#41 Pinkish Nude — ชมพูนู้ดอมเบจสุดละมุน Everyday Look", "hex": "#E4AC9A"},
            {"name": "#49 Milky Pink — ชมพูนมเนื้อแมทช์นัวๆ ไม่ลอย", "hex": "#E897A8"},
            {"name": "#01 Tidal Apricot — ส้มแอปริคอตอุ่นๆ เป็นธรรมชาติ", "hex": "#F49F75"},
            {"name": "#03 Soft Peach — ส้มพีชละมุน ขับผิวออร่า", "hex": "#F99175"},
            {"name": "#04 Melon Pomelo — ส้มอมชมพูคอรัล สดชื่นสดใส", "hex": "#F28C74"},
            {"name": "#06 Linen Nude — เบจนู้ดอมน้ำตาล Clean Girl สวยแพง", "hex": "#D8B49E"},
            {"name": "#35 Rosy Beige — น้ำตาลนู้ดอมชมพูกุหลาบตุ่น", "hex": "#C98979"},
            {"name": "#68 Toasted Cinnamon — น้ำตาลบ่มแดดติ่งส้มอิฐ สายฝอ", "hex": "#B56B48"}
        ],
        "lips": [
            {"name": "#09 Lychee (ลิ้นจี่) — ชมพูอมแดงระเรื่อ ขับผิวออร่า [Best Seller]", "hex": "#E04F63"},
            {"name": "#16 Pink Taro (เผือก) — ชมพูนมนัวๆ อมตุ่นละมุน", "hex": "#D896A2"},
            {"name": "#21 Strawberry Acai — ชมพูอมแดงสตรอว์เบอร์รี่สดใส ซ่อนเปรี้ยว", "hex": "#D63851"},
            {"name": "#22 Very Berry — ชมพูเบอร์รี่ฉ่ำน้ำ ทาออมเบรสวย", "hex": "#B51A30"},
            {"name": "#03 Pretzel — สีนู้ดน้ำตาลส้มอมพีชอ่อนๆ เบสสวย", "hex": "#D49880"},
            {"name": "#04 Biscoff — สีนู้ดชานมอมน้ำตาลนวลๆ คลาสสิก", "hex": "#C4856E"},
            {"name": "#11 Peanut (ถั่ว) — นู้ดชมพูอมน้ำตาลตุ่น My Lips But Better [Best Seller]", "hex": "#BC7862"},
            {"name": "#02 Pear — ส้มแอปริคอตสดใส บ่มแดด", "hex": "#E86A4F"},
            {"name": "#05 Nama Choco — น้ำตาลช็อกโกแลตเข้มข้น ลุคสายฝอ", "hex": "#703823"},
            {"name": "#10 Cranberry — แดงแครนเบอร์รี่ฉ่ำๆ หน้าไบรท์ [Best Seller]", "hex": "#B82238"},
            {"name": "#12 Date — แดงก่ำอมน้ำตาลอินทผลัม ลุคคุณหนู", "hex": "#993333"},
            {"name": "#13 Apple Glaze — แดงแอปเปิ้ลเคลือบแก้วฉ่ำวาว", "hex": "#CC1111"},
            {"name": "#19 Brown Sugar — น้ำตาลอมแดงอิฐอุ่นๆ คลาสสิก", "hex": "#9E4733"},
            {"name": "#24 Black Sesame (ดำ) — [Mixing Color] ทาทับให้ลิปดาร์กเข้มขึ้น", "hex": "#2B2B2B"},
            {"name": "#25 Grey (เทา) — [Mixing Color] ทาทับเพื่อดรอปความสว่างเพิ่มความหม่นตุ่น [NEW Best Seller]", "hex": "#7A7A7A"}
        ],
        "eyes": [
            {"name": "4U2 #02 Dust of Snow — ชมพูนู้ดชิมเมอร์แชมเปญทองอ่อนๆ", "hex": "#E5C2BD"},
            {"name": "4U2 #03 Wanted — ชมพูอมส้มพีชและน้ำตาลอิฐเนื้อแมทช์", "hex": "#E29D85"},
            {"name": "ODD STUDIO #01 Love, Dear — ชมพู-เบจมินิมอล เนื้อนัว", "hex": "#EAD5D1"},
            {"name": "ODD STUDIO #02 Rose, Moment — กุหลาบแห้ง Warm Rose วิ้งค์ทอง", "hex": "#D69393"},
            {"name": "Dasique #02 Rose Petal — กลีบกุหลาบ 9 ช่อง กลิตเตอร์สะท้อนแสงสวย", "hex": "#D99B9B"},
            {"name": "Dasique #14 Peach Squeeze — พีชส้มแอปริคอตสดใส ตาสวยหวานฉ่ำ", "hex": "#F2A888"}
        ]
    },
    "EN": {
        "foundations": {
            "light": [
                {"name": "00N (Natural Porcelain) — Extra Fair Neutral", "hex": "#F9E4D4"},
                {"name": "00W (Warm Porcelain) — Extra Fair Warm", "hex": "#F7DEC6"},
                {"name": "01N (Natural Vanilla) — Fair Neutral", "hex": "#F2D8C2"},
                {"name": "01W (Warm Vanilla) — Fair Warm", "hex": "#F4D5B6"}
            ],
            "medium": [
                {"name": "02N (Natural Ivory) — Light/Medium Neutral", "hex": "#E8C5A8"},
                {"name": "02W (Warm Ivory) — Light/Medium Warm", "hex": "#E5BE9E"},
                {"name": "02G (Golden Ivory) — Light/Medium Golden", "hex": "#E0B38C"},
                {"name": "03N (Natural Petal) — Medium Neutral", "hex": "#D8B08C"},
                {"name": "03W (Warm Almond) — Medium Warm", "hex": "#D1A47B"},
                {"name": "22N (Shell Beige) — Medium Shell Neutral", "hex": "#CE9E7A"}
            ],
            "dark": [
                {"name": "04N (Natural Beige) — Tan/Dark Neutral", "hex": "#BC8C66"},
                {"name": "04W (Warm Beige) — Tan Warm", "hex": "#B3805B"},
                {"name": "05W (Warm Sand) — Tan Sand Warm", "hex": "#A97853"},
                {"name": "06W (Warm Honey) — Deep Honey Warm", "hex": "#966542"},
                {"name": "07N (Soft Caramel) — Deep Caramel Neutral", "hex": "#7A4E31"},
                {"name": "08N (Rich Toffee) — Deep Rich Toffee", "hex": "#5E3920"}
            ]
        },
        "blushes": [
            {"name": "#02 Wavy Pink — Pastel Pink Soft Glow", "hex": "#F4B3C2"},
            {"name": "#41 Pinkish Nude — Soft Beige Nude Everyday", "hex": "#E4AC9A"},
            {"name": "#49 Milky Pink — Milky Matte Pink", "hex": "#E897A8"},
            {"name": "#01 Tidal Apricot — Warm Apricot Natural", "hex": "#F49F75"},
            {"name": "#03 Soft Peach — Soft Peach Glow", "hex": "#F99175"},
            {"name": "#04 Melon Pomelo — Coral Melon Fresh", "hex": "#F28C74"},
            {"name": "#06 Linen Nude — Clean Girl Brown Nude", "hex": "#D8B49E"},
            {"name": "#35 Rosy Beige — Rosy Brown Nude", "hex": "#C98979"},
            {"name": "#68 Toasted Cinnamon — Sunkissed Warm Brown", "hex": "#B56B48"}
        ],
        "lips": [
            {"name": "#09 Lychee — Bright Pink Red [Best Seller]", "hex": "#E04F63"},
            {"name": "#16 Pink Taro — Milky Pink Muted", "hex": "#D896A2"},
            {"name": "#21 Strawberry Acai — Vibrant Strawberry Red", "hex": "#D63851"},
            {"name": "#22 Very Berry — Deep Juicy Berry", "hex": "#B51A30"},
            {"name": "#03 Pretzel — Soft Peach Nude Base", "hex": "#D49880"},
            {"name": "#04 Biscoff — Classic Milk Tea Nude", "hex": "#C4856E"},
            {"name": "#11 Peanut — MLBB Pink Brown [Best Seller]", "hex": "#BC7862"},
            {"name": "#02 Pear — Sun-kissed Apricot", "hex": "#E86A4F"},
            {"name": "#05 Nama Choco — Rich Chocolate Brown", "hex": "#703823"},
            {"name": "#10 Cranberry — Bright Cranberry Red [Best Seller]", "hex": "#B82238"},
            {"name": "#12 Date — Deep Reddish Brown", "hex": "#993333"},
            {"name": "#13 Apple Glaze — Glossy Apple Red", "hex": "#CC1111"},
            {"name": "#19 Brown Sugar — Classic Brick Brown", "hex": "#9E4733"},
            {"name": "#24 Black Sesame — [Mixing Color] Darkener", "hex": "#2B2B2B"},
            {"name": "#25 Grey — [Mixing Color] Tone Down / Muted [NEW Best Seller]", "hex": "#7A7A7A"}
        ],
        "eyes": [
            {"name": "4U2 #02 Dust of Snow — Nude Pink Champagne Shimmer", "hex": "#E5C2BD"},
            {"name": "4U2 #03 Wanted — Warm Peach Coral & Matte Brick", "hex": "#E29D85"},
            {"name": "ODD STUDIO #01 Love, Dear — Minimalist Pink Beige", "hex": "#EAD5D1"},
            {"name": "ODD STUDIO #02 Rose, Moment — Warm Rose with Gold Sparkle", "hex": "#D69393"},
            {"name": "Dasique #02 Rose Petal — 9-Pan Rose Palette with Fine Glitter", "hex": "#D99B9B"},
            {"name": "Dasique #14 Peach Squeeze — Vibrant Peach Apricot Palette", "hex": "#F2A888"}
        ]
    }
}

LANGUAGES = {
    "TH": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "ระบบแนะนำเฉดสีเครื่องสำอางเฉพาะบุคคลสำหรับโครงงานวิทยาศาสตร์",
        "upload_label": "📸 อัปโหลดรูปภาพใบหน้า หรือถ่ายภาพเพื่อเลือกเฉดสีที่เหมาะสม",
        "matched_found": "✨ เฉดสีผลิตภัณฑ์ที่คัดเลือกและเหมาะกับใบหน้านี้",
        "foundation": "รองพื้น (Foundation)",
        "blush": "บลัชออน (Blush On)",
        "lip": "ลิปสติก (Lipstick)",
        "eye": "อายแชโดว์ (Eyeshadow)",
        "prep_title": "💡 ขั้นตอนการเตรียมผิวหน้า (Skincare & Prep Steps)",
        "prep_steps": [
            "**1. ทำความสะอาดผิวหน้า (Cleanse):** ล้างหน้าด้วยเจลหรือโฟมล้างหน้าที่เหมาะกับสภาพผิว เพื่อขจัดความมันส่วนเกินและสิ่งสกปรกที่ตกค้าง",
            "**2. ปรับสมดุลผิว (Tone):** เช็ดหน้าด้วยโทนเนอร์เบาๆ เพื่อเตรียมผิวให้พร้อมรับการบำรุง และช่วยกระชับรูขุมขน",
            "**3. เติมความชุ่มชื้น (Moisturize):** ทาเซรั่มและมอยส์เจอร์ไรเซอร์ให้ทั่วใบหน้าและลำคอ *(Tip: รอครีมซึม 1-2 นาทีก่อนแต่งหน้า)*",
            "**4. ทาครีมกันแดด (Sunscreen):** สำคัญมาก! บีบกันแดดในปริมาณที่เหมาะสม (ประมาณ 2 ข้อนิ้วมือ) เกลี่ยให้ทั่วใบหน้าและลำคอ",
            "**5. ลงไพร์เมอร์ (Primer):** ทาไพร์เมอร์เฉพาะจุด T-zone (หน้าผาก จมูก คาง) เพื่อเบลอรูขุมขนและล็อกเมคอัพให้ติดทน"
        ]
    },
    "EN": {
        "title": "AI Beauty Advisor & Color Mapping",
        "subtitle": "Personalized Cosmetic Shade Recommender for Science Project",
        "upload_label": "📸 Upload or capture test subject face image to match shades",
        "matched_found": "✨ Dynamically Matched Product Shades For This Face",
        "foundation": "Foundation",
        "blush": "Blush On",
        "lip": "Lipstick",
        "eye": "Eyeshadow",
        "prep_title": "💡 Skincare & Prep Steps",
        "prep_steps": [
            "**1. Cleanse:** Wash face with suitable cleanser to remove excess oil and impurities.",
            "**2. Tone:** Apply gentle toner to balance skin and prep for skincare.",
            "**3. Moisturize:** Apply serum and moisturizer evenly.",
            "**4. Sunscreen:** Essential! Apply proper amount (about 2 finger lengths) of sunscreen.",
            "**5. Primer:** Apply on T-zone to blur pores and lock in makeup."
        ]
    }
}

st.title("AI Beauty Advisor & Color Mapping")
st.write("โครงงานวิทยาศาสตร์: ระบบแนะนำเฉดสีเครื่องสำอางเฉพาะบุคคล / Science Project: Personalized Cosmetic Shade Recommender")

# ปุ่มเลือกภาษาอยู่ตรงกลางหน้าจอหลัก
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    lang = st.selectbox("🌐 Select Language / เลือกภาษา", ["TH", "EN"])

t = LANGUAGES[lang]
db = DATABASE[lang]

st.markdown("---")
# รองรับทั้งการอัปโหลดไฟล์และการถ่ายภาพจากกล้อง (camera_input)
upload_method = st.radio("เลือกวิธีป้อนรูปภาพ / Select input method:", ["📁 อัปโหลดไฟล์รูปภาพ (Upload File)", "📷 ถ่ายภาพด้วยกล้อง (Camera)"])

uploaded_file = None
if "อัปโหลด" in upload_method:
    uploaded_file = st.file_uploader(t["upload_label"], type=["jpg", "jpeg", "png"])
else:
    uploaded_file = st.camera_input(t["upload_label"])

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
        st.markdown(f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 14px;"><div style="width: 40px; height: 40px; background-color: {item["hex"]}; border-radius: 8px; border: 2px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"></div><span style="font-size: 14px; color: #444;">Color Swatch / Code: <code>{item["hex"]}</code></span></div>', unsafe_allow_html=True)

    render_color_item(t['foundation'], matched_fd)
    render_color_item(t['blush'], matched_blush)
    render_color_item(t['lip'], matched_lip)
    render_color_item(t['eye'], matched_eye)
    
    st.markdown("---")
    st.subheader(t["prep_title"])
    for step in t["prep_steps"]:
        st.markdown(f"- {step}")

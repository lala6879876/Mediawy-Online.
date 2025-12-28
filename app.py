import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق اللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stTextInput, .stTextArea { direction: rtl; text-align: right; }
    div.stRadio > div { flex-direction: row; }
    </style>
    """, unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الكاملة 🎬")

# إعداد المفتاح
API_KEY = "AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE"
genai.configure(api_key=API_KEY)

# --- قسم الإعدادات ---
st.subheader("🛠️ إعدادات الفيديو والصوت")
col1, col2 = st.columns(2)

with col1:
    audio_mode = st.radio("نوع التعليق الصوتي:", ["ذكاء اصطناعي (AI)", "صوت بشري (ملف)"])

with col2:
    logo_file = st.file_uploader("ارفع اللوجو", type=['png', 'jpg', 'jpeg'])

if audio_mode == "صوت بشري (ملف)":
    user_audio = st.file_uploader("ارفع ملف الـ MP3", type=['mp3'])

# --- زر الإنتاج ---
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
            res_text = None
            # محاولة تجربة الموديلات المتاحة لحل مشكلة 404
            models_to_try = ['gemini-1.5-flash', 'gemini-pro', 'gemini-1.5-pro']
            
            for m_name in models_to_try:
                try:
                    model = genai.GenerativeModel(m_name)
                    prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                    response = model.generate_content(prompt)
                    if response.text:
                        res_text = response.text
                        break
                except:
                    continue
            
            if res_text:
                st.success("✅ تم استلام البيانات بنجاح!")
                lines = res_text.split('\n')
                
                # --- الـ 5 مستطيلات المطلوبة ---
                st.divider()
                st.subheader("📋 خطة النشر المقترحة (SEO)")
                
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ وصف الفيديو (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، تحفيز، ميدياوي، تطوير الذات")
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #تطوير_ذات #ميدياوي #shorts")
                st.info("5️⃣ موعد النشر المثالي: اليوم الساعة 8 مساءً")
                
                st.balloons()
            else:
                st.error("خطأ: تعذر الوصول لموديلات جوجل حالياً، برجاء المحاولة مرة أخرى.")
    else:
        st.warning("برجاء رفع اللوجو أولاً")

st.markdown("---")
st.caption("برمجة وتطوير ميدياوي © 2025")

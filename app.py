import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق RTL للعربية
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الكاملة 🎬")

# سحب المفتاح من الخزنة السرية (Secrets)
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("⚠️ خطأ: لم يتم وضع المفتاح في الـ Secrets!")
    st.stop()

# --- واجهة المستخدم ---
st.subheader("🎤 أولاً: نوع التعليق الصوتي")
audio_mode = st.radio("", ["ذكاء اصطناعي (AI)", "صوت بشري (ملف)"], label_visibility="collapsed")
if audio_mode == "صوت بشري (ملف)":
    st.file_uploader("ارفع ملف الـ MP3", type=['mp3'])

st.divider()

st.subheader("🖼️ ثانياً: ارفع اللوجو")
logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

if st.button("توليد الخطة والسكريبت 🚀"):
    if logo_file:
        with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
            try:
                # محاولة استخدام الموديل المتاح
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("اكتب نصيحة عن النجاح بالعامية المصرية واقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر.")
                
                st.success("✅ تم التوليد بنجاح")
                res_text = response.text
                lines = res_text.split('\n')
                
                # عرض الـ 5 مستطيلات
                st.divider()
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف الكامل (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، ميدياوي، تطوير")
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #ميدياوي #shorts")
                st.info("5️⃣ موعد النشر المثالي: اليوم الساعة 8 مساءً")
                st.balloons()
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً")

st.caption("برمجة وتطوير ميدياوي © 2025")

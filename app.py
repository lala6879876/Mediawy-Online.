import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق RTL
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الكاملة 🎬")

# إعداد المفتاح
genai.configure(api_key="AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE")

# 1. اختيار الصوت (فوق خالص)
st.subheader("🎤 أولاً: اختر نوع الصوت")
audio_mode = st.radio("", ["ذكاء اصطناعي (AI)", "صوت بشري (ملف)"], label_visibility="collapsed")

if audio_mode == "صوت بشري (ملف)":
    user_audio = st.file_uploader("ارفع ملف الـ MP3", type=['mp3'])

st.divider()

# 2. اللوجو
st.subheader("🖼️ ثانياً: ارفع الشعار (Logo)")
logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# زر الإنتاج
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري الاتصال بجوجل..."):
            try:
                # محاولة استخدام الموديل بالاسم الأكثر شمولاً
                model = genai.GenerativeModel('models/gemini-1.5-flash')
                prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                response = model.generate_content(prompt)
                res_text = response.text
                
                st.success("✅ تم التوليد بنجاح")
                lines = res_text.split('\n')
                
                # الـ 5 مستطيلات
                st.divider()
                st.text_input("1️⃣ العنوان:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية:", value="نجاح، ميدياوي، تطوير الذات")
                st.text_input("4️⃣ الهاشتاجات:", value="#نجاح #ميدياوي #shorts")
                st.info("5️⃣ موعد النشر: اليوم الساعة 8 مساءً")
                st.balloons()
                
            except Exception as e:
                # لو فشل، جرب الموديل البديل فوراً
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    res_text = response.text
                    st.success("✅ تم التوليد (نسخة احتياطية)")
                    st.text_area("البيانات:", value=res_text, height=200)
                except:
                    st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً")

st.caption("Mediawy Pro © 2025")

import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق RTL للعربية
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الاحترافية 🎬")

# سحب المفتاح من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ خطأ: المفتاح غير موجود في Secrets!")
    st.stop()

# --- 1. اختيار الصوت (فوق) ---
st.subheader("🎤 أولاً: نوع التعليق الصوتي")
audio_mode = st.radio("", ["ذكاء اصطناعي (AI)", "صوت بشري (ملف)"], label_visibility="collapsed")
if audio_mode == "صوت بشري (ملف)":
    st.file_uploader("ارفع ملف الـ MP3", type=['mp3'])

st.divider()

# --- 2. رفع اللوجو ---
st.subheader("🖼️ ثانياً: ارفع اللوجو")
logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# --- زر الإنتاج ---
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري فحص الموديلات وتوليد المحتوى..."):
            try:
                # الحركة السحرية: بنسأل جوجل إيه الموديل اللي شغال عندك يا ست الكل؟
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # بننقي أحسن واحد (1.5 flash) لو موجود، لو مش موجود بياخد أول واحد
                target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])

                model = genai.GenerativeModel(target_model)
                prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح في أسطر منفصلة: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                response = model.generate_content(prompt)
                
                st.success(f"✅ تم الاتصال بنجاح!")
                res_text = response.text
                lines = res_text.split('\n')
                
                # الـ 5 مستطيلات
                st.divider()
                st.subheader("📋 خطة النشر والـ SEO")
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف الكامل (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، ميدياوي، تطوير")
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #ميدياوي #shorts")
                st.info(f"5️⃣ موعد النشر: اليوم الساعة 8 مساءً")
                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("برجاء رفع اللوجو أولاً")

st.caption("برمجة وتطوير ميدياوي © 2025")

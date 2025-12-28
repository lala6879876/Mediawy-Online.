import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق اللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stTextInput, .stTextArea { direction: rtl; text-align: right; }
    div.stRadio > div { flex-direction: row; gap: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الكاملة 🎬")

# إعداد المفتاح
API_KEY = "AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE"
genai.configure(api_key=API_KEY)

# --- 1. قسم اختيار الصوت (بقى فوق خالص) ---
st.subheader("🎤 أولاً: اختر نوع الصوت")
audio_mode = st.radio("", ["ذكاء اصطناعي (AI)", "صوت بشري (ملف)"], label_visibility="collapsed")

if audio_mode == "صوت بشري (ملف)":
    user_audio = st.file_uploader("ارفع ملف الـ MP3 الخاص بك", type=['mp3'])

st.divider()

# --- 2. قسم رفع اللوجو ---
st.subheader("🖼️ ثانياً: ارفع الشعار (Logo)")
logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# --- زر الإنتاج ---
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري فحص الموديلات وتوليد المحتوى..."):
            res_text = None
            try:
                # محاولة الحصول على الموديلات المتاحة تلقائياً
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # اختيار أفضل موديل متاح
                target_model = ""
                if any("gemini-1.5-flash" in m for m in available_models):
                    target_model = [m for m in available_models if "gemini-1.5-flash" in m][0]
                elif any("gemini-pro" in m for m in available_models):
                    target_model = [m for m in available_models if "gemini-pro" in m][0]
                else:
                    target_model = available_models[0]

                model = genai.GenerativeModel(target_model)
                prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                response = model.generate_content(prompt)
                res_text = response.text
                
            except Exception as e:
                st.error(f"عذراً، حدث خطأ: {str(e)}")
            
            if res_text:
                st.success(f"✅ تم التوليد بنجاح")
                lines = res_text.split('\n')
                
                # --- المستطيلات الـ 5 ---
                st.divider()
                st.subheader("📋 خطة النشر المقترحة")
                
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف الكامل (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، ميدياوي، تطوير الذات")
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #ميدياوي #shorts")
                st.info("5️⃣ موعد النشر: اليوم الساعة 8 مساءً")
                
                st.balloons()
    else:
        st.warning("برجاء رفع اللوجو أولاً")

st.markdown("---")
st.caption("برمجة وتطوير ميدياوي © 2025")

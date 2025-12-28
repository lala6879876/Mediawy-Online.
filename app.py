import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online Pro", layout="centered")

# تنسيق RTL
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Pro - النسخة الكاملة 🎬")

# إعداد المفتاح
API_KEY = "AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE"
genai.configure(api_key=API_KEY)

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
        with st.spinner("جاري الاتصال بأقوى موديل متاح..."):
            try:
                # الكود السحري: بيشوف الموديلات اللي حسابك بيدعمها فعلاً
                models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                # ترتيب الموديلات حسب الأفضلية (الأحدث للأقدم)
                if any("gemini-1.5-flash" in m for m in models):
                    final_model = [m for m in models if "gemini-1.5-flash" in m][0]
                elif any("gemini-1.5-pro" in m for m in models):
                    final_model = [m for m in models if "gemini-1.5-pro" in m][0]
                else:
                    final_model = models[0] # بياخد أول موديل متاح في حسابك أياً كان اسمه

                model = genai.GenerativeModel(final_model)
                prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                response = model.generate_content(prompt)
                res_text = response.text
                
                st.success(f"✅ تم التشغيل بنجاح")
                lines = res_text.split('\n')
                
                # الـ 5 مستطيلات
                st.divider()
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف الاحترافي:", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية:", value="نجاح، ميدياوي، تطوير الذات")
                st.text_input("4️⃣ الهاشتاجات:", value="#نجاح #ميدياوي #shorts")
                st.info(f"5️⃣ موعد النشر المثالي: اليوم - باستخدام {final_model}")
                st.balloons()
                
            except Exception as e:
                st.error(f"عذراً يا محمد، لسه فيه مشكلة في الاتصال: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً")

st.markdown("---")
st.caption("برمجة وتطوير ميدياوي © 2025")

import streamlit as st
import google.generativeai as genai
import os

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online 🎬", layout="centered")

# --- تنسيق التصميم (CSS) لجعل الواجهة أجمل ---
st.markdown("""
    <style>
    .main { text-align: right; }
    .stTextInput, .stTextArea { direction: rtl; }
    </style>
    """, unsafe_allow_type=True)

st.title("Mediawy Pro - النسخة الأونلاين 🎬")
st.subheader("منصة صناعة المحتوى الذكي")

# إعداد مفتاح API
API_KEY = "AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE"
genai.configure(api_key=API_KEY)

# --- الواجهة ---
with st.expander("⚙️ إعدادات الفيديو", expanded=True):
    audio_mode = st.radio("اختر مصدر الصوت:", ["ذكاء اصطناعي (AI)", "رفع ملف خارجي"])
    if audio_mode == "رفع ملف خارجي":
        st.file_uploader("ارفع ملف الـ MP3", type=['mp3'])
    
    logo_file = st.file_uploader("ارفع شعارك (Logo)", type=['png', 'jpg', 'jpeg'])

# --- زر البدء ---
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري التواصل مع الذكاء الاصطناعي..."):
            try:
                # محاولة استخدام الموديل المتاح
                model_name = 'gemini-1.5-flash'
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = "اكتب نصيحة عن النجاح بالعامية المصرية ثم اقترح (عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر) في أسطر منفصلة."
                    response = model.generate_content(prompt)
                    res_text = response.text
                except:
                    # إذا فشل الفلاش نستخدم البرو (حل مشكلة 404)
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                    res_text = response.text

                st.success("✅ تم استلام البيانات من الذكاء الاصطناعي")

                # تقسيم النص لمحاكاة المستطيلات الخمسة
                lines = res_text.split('\n')
                
                # --- عرض النتائج في المستطيلات الخمسة ---
                st.markdown("---")
                st.text_input("📌 العنوان المقترح:", value=lines[0] if len(lines)>0 else "عنوان الفيديو")
                st.text_area("📝 الوصف الاحترافي (Description):", value=res_text, height=150)
                st.text_input("🔍 الكلمات المفتاحية (Tags):", value="نجاح، تحفيز، ميدياوي، تطوير الذات")
                st.text_input("🏷️ الهاشتاجات (Hashtags):", value="#نجاح #تطوير_ذات #ميدياوي #shorts")
                st.info(f"⏰ موعد النشر المثالي: {lines[-1] if len(lines)>1 else 'الساعة 8 مساءً'}")

                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ في النظام: {str(e)}")
                st.info("تأكد من صلاحية مفتاح ال

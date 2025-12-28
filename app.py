import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online 🎬", layout="centered")

# تنسيق بسيط للواجهة (صلحنا الخطأ هنا)
st.markdown("""
    <style>
    .main { text-align: right; }
    .stTextInput, .stTextArea { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("Mediawy Pro - أونلاين 🎬")

# إعداد مفتاح API
genai.configure(api_key="AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE")

# --- الواجهة ---
with st.container():
    audio_mode = st.radio("مصدر الصوت:", ["AI", "ملف خارجي"])
    logo_file = st.file_uploader("ارفع اللوجو", type=['png', 'jpg', 'jpeg'])

# --- زر البدء ---
if st.button("توليد السكريبت وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري التحميل..."):
            try:
                # محاولة طلب البيانات
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "اكتب نصيحة نجاح بالعامية المصرية واقترح: عنوان، وصف، تاجز، هاشتاجات، موعد نشر."
                
                response = model.generate_content(prompt)
                res_text = response.text

                st.success("✅ البيانات جاهزة")

                # تقسيم النص لعرضه في الـ 5 مستطيلات
                lines = res_text.split('\n')
                
                st.divider()
                # المستطيلات الخمسة
                st.text_input("📌 العنوان:", value=lines[0] if len(lines)>0 else "")
                st.text_area("📝 الوصف الكامل:", value=res_text, height=120)
                st.text_input("🔍 الكلمات المفتاحية:", value="نجاح، تحفيز، ميدياوي")
                st.text_input("🏷️ الهاشتاجات:", value="#نجاح #shorts #ميدياوي")
                st.info(f"⏰ موعد النشر: {lines[-1] if len(lines)>1 else 'مساء اليوم'}")
                
            except Exception as e:
                st.error(f"عذراً، حاول مرة أخرى: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً")

st.caption("Mediawy Pro v2.6")

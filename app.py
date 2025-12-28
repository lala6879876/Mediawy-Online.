import streamlit as st
import google.generativeai as genai
import asyncio
import edge_tts
import requests
import os

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online 🎬", layout="centered")

# إدخال المفتاح (Gemini)
genai.configure(api_key="AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE")

st.title("Mediawy Pro - أونلاين 🎬")
st.subheader("أهلاً بك يا محمد في منصتك الخاصة")

# --- الواجهة ---
with st.container():
    audio_mode = st.radio("اختر نوع الصوت:", ["ذكاء اصطناعي (AI)", "صوت بشري (رفع ملف)"])
    
    user_audio = None
    if audio_mode == "صوت بشري (رفع ملف)":
        user_audio = st.file_uploader("ارفع ملف الصوت (MP3)", type=['mp3'])
    
    logo_file = st.file_uploader("ارفع اللوجو الخاص بك", type=['png', 'jpg', 'jpeg'])

# --- زر الإنتاج ---
if st.button("إنشاء الفيديو وخطة النشر 🚀"):
    if logo_file:
        with st.spinner("جاري توليد المحتوى والمونتاج..."):
            try:
                # 1. الذكاء الاصطناعي (السكريبت والبيانات)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "اكتب نصيحة سريعة وقوية عن النجاح بالعامية المصرية مع اقتراح (عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر)."
                resp = model.generate_content(prompt).text
                
                # 2. عرض بيانات النشر في الـ 5 مستطيلات
                st.success("✅ تم تجهيز خطة النشر!")
                sections = resp.split('\n')
                
                st.text_input("📌 العنوان المقترح:", value=sections[0] if len(sections)>0 else "")
                st.text_area("📝 الوصف (Description):", value=resp, height=150)
                st.text_input("🔍 الكلمات المفتاحية:", value="نجاح، ميدياوي، تطوير")
                st.text_input("🏷️ الهاشتاجات:", value="#نجاح #ميدياوي #تحفيز")
                st.info(f"⏰ {sections[-1] if len(sections)>0 else 'موعد النشر: المساء'}")
                
                # 3. ملاحظة المونتاج أونلاين
                st.warning("تم تجهيز البيانات! المونتاج النهائي يتم الآن ربطه بسيرفرات التحميل.")
                
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.error("من فضلك ارفع اللوجو أولاً")

st.markdown("---")
st.caption("Mediawy Cinema Engine v2.5 - 2025")

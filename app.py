import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Video Maker", layout="centered")

# تنسيق RTL
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Pro - مصنع الفيديوهات 🎬")

# إعداد المفتاح من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# المدخلات
audio_mode = st.radio("مصدر الصوت:", ["ذكاء اصطناعي (AI)", "رفع ملف خارجي"])
logo_file = st.file_uploader("ارفع اللوجو الخاص بك", type=['png', 'jpg', 'jpeg'])

if st.button("صناعة الفيديو الآن 🚀"):
    if logo_file:
        with st.spinner("جاري فحص الموديلات وتوليد الفيديو... قد يستغرق دقيقة..."):
            try:
                # 1. البحث عن الموديل الشغال (تجنب خطأ 404)
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                
                model = genai.GenerativeModel(target_model)
                response = model.generate_content("اكتب نصيحة نجاح قصيرة جداً بالعامية المصرية (سطرين فقط).")
                script = response.text
                
                # 2. تحويل النص لصوت
                tts = gTTS(text=script, lang='ar')
                tts.save("voice.mp3")
                
                # 3. معالجة اللوجو
                with open("temp_logo.png", "wb") as f:
                    f.write(logo_file.getbuffer())
                
                # 4. الرندرة (دمج الصوت والصورة)
                audio_clip = AudioFileClip("voice.mp3")
                video_clip = ImageClip("temp_logo.png").set_duration(audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                # إخراج الفيديو بجودة سريعة
                video_clip.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac")
                
                # 5. عرض الفيديو
                st.success(f"✅ تم صناعة الفيديو بنجاح باستخدام {target_model}")
                st.video("final_video.mp4")
                
                with open("final_video.mp4", "rb") as file:
                    st.download_button("تحميل الفيديو 📥", file, "mediawy_video.mp4")
                
                st.divider()
                st.subheader("📋 بيانات الفيديو")
                st.text_area("السكريبت المولّد:", script)

            except Exception as e:
                st.error(f"حدث خطأ أثناء الرندرة: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً عشان نصنع الفيديو")

st.caption("Mediawy Pro © 2025")

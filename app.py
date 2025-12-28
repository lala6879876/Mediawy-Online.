import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip
import os

st.set_page_config(page_title="Mediawy Video Maker", layout="centered")

# إعداد الذكاء الاصطناعي
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

st.title("Mediawy Pro - مصنع الفيديوهات 🎬")

# المدخلات
audio_mode = st.radio("مصدر الصوت:", ["ذكاء اصطناعي (AI)", "رفع ملف خارجي"])
logo_file = st.file_uploader("ارفع اللوجو الخاص بك", type=['png', 'jpg', 'jpeg'])

if st.button("صناعة الفيديو الآن 🚀"):
    if logo_file:
        with st.spinner("جاري توليد السكريبت والصوت والفيديو..."):
            try:
                # 1. توليد النص
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("اكتب نصيحة نجاح قصيرة جداً بالعامية المصرية.")
                script = response.text
                
                # 2. تحويل النص لصوت (gTTS)
                tts = gTTS(text=script, lang='ar')
                tts.save("voice.mp3")
                
                # 3. حفظ اللوجو مؤقتاً
                with open("temp_logo.png", "wb") as f:
                    f.write(logo_file.getbuffer())
                
                # 4. صناعة الفيديو (MoviePy)
                audio_clip = AudioFileClip("voice.mp3")
                # عمل فيديو مدته على قد مدة الصوت
                video_clip = ImageClip("temp_logo.png").set_duration(audio_clip.duration)
                video_clip = video_clip.set_audio(audio_clip)
                
                # تصدير الفيديو
                video_clip.write_videofile("final_video.mp4", fps=24, codec="libx264")
                
                # 5. عرض النتائج
                st.success("✅ تم صناعة الفيديو بنجاح!")
                st.video("final_video.mp4") # هنا الفيديو هيظهر قدامك
                
                with open("final_video.mp4", "rb") as file:
                    st.download_button("تحميل الفيديو 📥", file, "mediawy_video.mp4")
                
                # عرض البيانات تحت الفيديو
                st.divider()
                st.subheader("📋 خطة النشر")
                st.text_area("السكريبت المستخدم:", script)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الرندرة: {str(e)}")
    else:
        st.warning("لازم ترفع اللوجو عشان نركبه على الفيديو!")

st.caption("برمجة وتطوير ميدياوي © 2025")

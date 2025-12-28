import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.editor import *
import requests
import os
import random

st.set_page_config(page_title="Mediawy Shorts Pro2026", layout="centered")

# إعدادات API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

st.title("Mediawy Shorts Creator 🎬🔥")

# --- المدخلات ---
audio_mode = st.radio("مصدر الصوت:", ["ذكاء اصطناعي (AI)", "صوت بشرى (WAV/MP3)"])
user_audio_file = None
if audio_mode == "صوت بشرى (WAV/MP3)":
    user_audio_file = st.file_uploader("ارفع تسجيلك الصوتي", type=['wav', 'mp3'])

logo_file = st.file_uploader("ارفع لوجو القناة", type=['png', 'jpg', 'jpeg'])

if st.button("صناعة فيديو احترافي بنقلات 🚀"):
    if logo_file:
        with st.spinner("جاري المعالجة.. لحظات والفيديو يجهز..."):
            try:
                # 1. إعداد الصوت وتجهيزه
                if audio_mode == "ذكاء اصطناعي (AI)":
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                    model = genai.GenerativeModel(target_model)
                    res = model.generate_content("اكتب نصيحة نجاح قصيرة جداً بالعامية المصرية.")
                    tts = gTTS(text=res.text, lang='ar')
                    tts.save("temp_audio.mp3")
                    audio = AudioFileClip("temp_audio.mp3")
                else:
                    ext = user_audio_file.name.split('.')[-1]
                    audio_path = f"user_audio.{ext}"
                    with open(audio_path, "wb") as f: f.write(user_audio_file.getbuffer())
                    audio = AudioFileClip(audio_path)

                duration = audio.duration
                part_duration = duration / 3

                # 2. جلب 3 صور ومعالجتها بـ PIL لضمان الجودة
                clips = []
                for i in range(3):
                    # رابط صور بجودة عالية وأبعاد ثابتة
                    img_url = f"https://picsum.photos/seed/{random.randint(1,1000)}/1080/1920"
                    img_data = requests.get(img_url).content
                    img_path = f"bg_{i}.jpg"
                    with open(img_path, "wb") as f: f.write(img_data)
                    
                    # خطوة الأمان: فتح الصورة بـ PIL وحفظها بصيغة RGB قياسية
                    temp_img = PIL.Image.open(img_path).convert("RGB")
                    temp_img.save(img_path)
                    
                    # صنع الكليب مع تأثير الزوم
                    clip = ImageClip(img_path).set_duration(part_duration).resize(height=1920)
                    # تأثير الزوم الاحترافي
                    clip = clip.fx(vfx.resize, lambda t: 1 + 0.03 * t) 
                    clips.append(clip)

                # 3. دمج الصور مع طريقة "method='subtitles'" لضمان استقرار الفريمات
                bg_video = concatenate_videoclips(clips, method="compose")

                # 4. إضافة اللوجو (أعلى اليمين)
                with open("logo_temp.png", "wb") as f: f.write(logo_file.getbuffer())
                logo = (ImageClip("logo_temp.png")
                        .resize(width=180)
                        .set_duration(duration)
                        .set_position(("right", "top"))
                        .margin(right=30, top=30, opacity=0))

                # 5. الإنتاج النهائي بأكواد أمان متطورة
                final = CompositeVideoClip([bg_video, logo], size=(1080, 1920))
                final = final.set_audio(audio)
                
                output_file = "final_shorts.mp4"
                # الإعدادات دي بتحل مشكلة avcodec_send_packet
                final.write_videofile(
                    output_file, 
                    fps=24, 
                    codec="libx264", 
                    audio_codec="aac",
                    temp_audiofile='temp-audio.m4a', 
                    remove_temp=True
                )

                st.success("✅ تم حل المشكلة وصناعة الفيديو بنجاح!")
                st.video(output_file)
                
                with open(output_file, "rb") as f:
                    st.download_button("تحميل الفيديو 📥", f, "mediawy_shorts.mp4")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الرندرة: {str(e)}")
    else:
        st.warning("ارفع اللوجو الأول!")

st.caption("Mediawy Pro © 2025")

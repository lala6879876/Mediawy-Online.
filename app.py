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

st.set_page_config(page_title="Mediawy Shorts Ultra", layout="centered")

# إعدادات API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

st.title("Mediawy Shorts Ultra 🎬✨")

# --- المدخلات ---
audio_mode = st.radio("مصدر الصوت:", ["ذكاء اصطناعي (AI)", "صوت بشرى (WAV/MP3)"])
user_audio_file = None
if audio_mode == "صوت بشرى (WAV/MP3)":
    user_audio_file = st.file_uploader("ارفع تسجيلك الصوتي", type=['wav', 'mp3'])

logo_file = st.file_uploader("ارفع لوجو القناة", type=['png', 'jpg', 'jpeg'])

if st.button("صناعة الفيديو الترا 🚀"):
    if logo_file:
        with st.spinner("جاري الرندرة وإضافة الموسيقى والنصوص..."):
            try:
                # 1. إعداد الصوت الأساسي
                if audio_mode == "ذكاء اصطناعي (AI)":
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                    model = genai.GenerativeModel(target_model)
                    res = model.generate_content("اكتب نصيحة دينية قصيرة جداً بالعامية المصرية (أقل من 10 كلمات).")
                    script = res.text
                    tts = gTTS(text=script, lang='ar')
                    tts.save("temp_audio.mp3")
                    audio = AudioFileClip("temp_audio.mp3")
                else:
                    ext = user_audio_file.name.split('.')[-1]
                    with open(f"user_audio.{ext}", "wb") as f: f.write(user_audio_file.getbuffer())
                    audio = AudioFileClip(f"user_audio.{ext}")
                    script = "نصيحة اليوم من ميدياوي" # نص افتراضي للـ Subtitles في حالة الصوت البشري

                duration = audio.duration

                # 2. إضافة موسيقى خلفية هادئة (رابط خارجي)
                music_url = "https://www.bensound.com/bensound-music/bensound-relaxing.mp3"
                music_data = requests.get(music_url).content
                with open("bg_music.mp3", "wb") as f: f.write(music_data)
                bg_music = AudioFileClip("bg_music.mp3").volumex(0.1).set_duration(duration) # خفض الصوت لـ 10%
                
                final_audio = CompositeAudioClip([audio, bg_music])

                # 3. جلب الصور وتأثير الزوم
                clips = []
                for i in range(2):
                    img_url = f"https://picsum.photos/seed/{random.randint(1,500)}/1080/1920"
                    img_data = requests.get(img_url).content
                    img_path = f"bg_{i}.jpg"
                    with open(img_path, "wb") as f: f.write(img_data)
                    PIL.Image.open(img_path).convert("RGB").save(img_path)
                    clip = ImageClip(img_path).set_duration(duration/2).resize(height=1920).fx(vfx.resize, lambda t: 1 + 0.02*t)
                    clips.append(clip)
                bg_video = concatenate_videoclips(clips, method="compose")

                # 4. اللوجو (أعلى اليمين)
                with open("logo_temp.png", "wb") as f: f.write(logo_file.getbuffer())
                logo = ImageClip("logo_temp.png").resize(width=180).set_duration(duration).set_position(("right", "top")).margin(right=30, top=30, opacity=0)

                # 5. شريط الأدعية المتحرك في الأسفل
                dua_list = " 🕋 سبحان الله .. الحمد لله .. لا إله إلا الله .. الله أكبر .. " * 10
                # ملاحظة: سنستخدم صورة بسيطة للشريط لتجنب مشاكل الخطوط العربية على السيرفر
                dua_strip = ColorClip(size=(1080, 80), color=(0,0,0)).set_opacity(0.6).set_duration(duration).set_position(("center", 1750))

                # --- الإنتاج النهائي ---
                final = CompositeVideoClip([bg_video, logo, dua_strip], size=(1080, 1920))
                final = final.set_audio(final_audio)
                
                output_file = "ultra_shorts.mp4"
                final.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")

                st.success("✅ تم صناعة الفيديو بالموسيقى والتأثيرات!")
                st.video(output_file)
                st.info(f"السكريبت: {script}")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("ارفع اللوجو الأول!")

st.caption("Mediawy Ultra © 2025")

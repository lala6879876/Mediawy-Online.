import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import *
import requests
from PIL import Image
import os

st.set_page_config(page_title="Mediawy Shorts Maker", layout="centered")

# إعدادات API من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

st.title("Mediawy Shorts Creator 🎬✨")

logo_file = st.file_uploader("ارفع لوجو القناة", type=['png', 'jpg', 'jpeg'])

if st.button("صناعة فيديو شورتس الآن 🚀"):
    if logo_file:
        with st.spinner("جاري تصميم الفيديو (أبعاد الشورتس + لوجو + صوت)..."):
            try:
                # 1. توليد السكريبت
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content("اكتب نصيحة دينية قصيرة جداً بالعامية المصرية (سطرين).")
                script = res.text

                # 2. الصوت
                tts = gTTS(text=script, lang='ar')
                tts.save("voice.mp3")
                audio = AudioFileClip("voice.mp3")
                duration = audio.duration

                # 3. جلب خلفية شورتس (صورة طولي 1080x1920)
                img_url = "https://images.unsplash.com/photo-1509062522246-3755977927d7?q=80&w=1080&h=1920&auto=format&fit=crop"
                img_data = requests.get(img_url).content
                with open("bg.jpg", "wb") as f: f.write(img_data)

                # 4. بناء الفيديو (استخدام ImageClip مباشرة)
                bg = ImageClip("bg.jpg").set_duration(duration)
                
                # جعل الفيديو طولي (شورتس)
                bg = bg.resize(height=1920) # تأكيد الارتفاع

                # 5. معالجة اللوجو (أعلى اليمين)
                with open("logo_temp.png", "wb") as f: f.write(logo_file.getbuffer())
                logo = (ImageClip("logo_temp.png")
                        .resize(width=200) # حجم اللوجو
                        .set_duration(duration)
                        .set_position(("right", "top")))

                # 6. الدمج النهائي (بدون TextClip لتجنب أخطاء السيرفر)
                final = CompositeVideoClip([bg, logo], size=(1080, 1920))
                final = final.set_audio(audio)
                
                # تصدير الفيديو
                output_file = "shorts_mediawy.mp4"
                final.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")

                st.success("✅ مبروك! الفيديو جاهز بالأبعاد المطلوبة واللوجو")
                st.video(output_file)
                
                with open(output_file, "rb") as f:
                    st.download_button("تحميل الفيديو 📥", f, "mediawy_shorts.mp4")

            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("ارفع اللوجو الأول يا بطل!")

st.caption("برمجة وتطوير ميدياوي © 2025")

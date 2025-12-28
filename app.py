import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from moviepy.editor import *
from moviepy.video.fx.all import resize
import requests
import os

st.set_page_config(page_title="Mediawy Shorts Maker", layout="centered")

# إعدادات API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود!")
    st.stop()

st.title("Mediawy Shorts Creator 🎬✨")

logo_file = st.file_uploader("ارفع لوجو القناة", type=['png', 'jpg'])

if st.button("صناعة الفيديو الاحترافي 🚀"):
    if logo_file:
        with st.spinner("جاري تصميم الفيديو... (لوجو، صور، شريط متحرك)"):
            try:
                # 1. توليد السكريبت
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                model = genai.GenerativeModel(target_model)
                res = model.generate_content("اكتب نصيحة دينية قصيرة جداً للشباب بالعامية.")
                script = res.text

                # 2. الصوت
                tts = gTTS(text=script, lang='ar')
                tts.save("voice.mp3")
                audio = AudioFileClip("voice.mp3")
                duration = audio.duration

                # 3. جلب صور تلقائية (Unsplash)
                img_url = "https://source.unsplash.com/1080x1920/?nature,mosque"
                img_data = requests.get(img_url).content
                with open("bg.jpg", "wb") as f: f.write(img_data)

                # 4. بناء الفيديو (أبعاد الشورتس)
                bg = ImageClip("bg.jpg").set_duration(duration).resize(height=1920)
                
                # تأثير الزوم (خفيف)
                bg = bg.add_mask().fx(vfx.zoom_in, 0.05, duration)

                # 5. اللوجو (أعلى اليمين)
                with open("logo.png", "wb") as f: f.write(logo_file.getbuffer())
                logo = ImageClip("logo.png").resize(width=150).set_duration(duration)
                logo = logo.set_position(("right", "top")).margin(right=20, top=20, opacity=0)

                # 6. شريط الأدعية المتحرك (أسفل الفيديو)
                dua_text = "سبحان الله وبحمده .. سبحان الله العظيم .. لا إله إلا الله " * 5
                txt_clip = TextClip(dua_text, fontsize=40, color='white', bg_color='black', size=(2000, 60))
                txt_clip = txt_clip.set_duration(duration).set_position(("center", 1700))
                # تحريك الشريط من اليمين لليسار
                txt_clip = txt_clip.fx(vfx.scroll, w=1080, x_speed=100)

                # 7. الدمج النهائي
                final = CompositeVideoClip([bg, logo, txt_clip], size=(1080, 1920))
                final = final.set_audio(audio)
                
                final.write_videofile("shorts.mp4", fps=24, codec="libx264", audio_codec="aac")

                st.success("✅ الفيديو جاهز يا بطل!")
                st.video("shorts.mp4")
                
            except Exception as e:
                st.error(f"خطأ: {str(e)}")
    else:
        st.warning("ارفع اللوجو الأول يا هندسة!")

st.caption("برمجة وتطوير ميدياوي © 2025")

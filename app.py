import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import PIL.Image
# الحل السحري لمشكلة ANTIALIAS
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
from moviepy.editor import *
import requests
import os

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Shorts Maker", layout="centered")

# تنسيق RTL
st.markdown("""<style>.main {text-align: right; direction: rtl;} .stTextInput, .stTextArea {direction: rtl; text-align: right;}</style>""", unsafe_allow_html=True)

st.title("Mediawy Shorts Creator 🎬✨")

# إعداد المفتاح من Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

# --- 1. قسم الصوت ---
st.subheader("🎤 مصدر الصوت")
audio_mode = st.radio("", ["ذكاء اصطناعي (AI)", "صوت بشرى (WAV/MP3)"], label_visibility="collapsed")

user_audio_file = None
if audio_mode == "صوت بشرى (WAV/MP3)":
    user_audio_file = st.file_uploader("ارفع تسجيلك الصوتي (WAV أو MP3)", type=['wav', 'mp3'])

st.divider()

# --- 2. قسم اللوجو ---
st.subheader("🖼️ ارفع لوجو القناة")
logo_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

# --- زر الإنتاج ---
if st.button("صناعة فيديو شورتس الآن 🚀"):
    if logo_file:
        if audio_mode == "صوت بشرى (WAV/MP3)" and user_audio_file is None:
            st.warning("ارفع ملف الويف (WAV) الأول!")
            st.stop()
            
        with st.spinner("جاري الرندرة... قد يستغرق الأمر دقيقة"):
            try:
                # 1. إعداد الصوت
                if audio_mode == "ذكاء اصطناعي (AI)":
                    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                    target_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                    model = genai.GenerativeModel(target_model)
                    res = model.generate_content("اكتب نصيحة دينية قصيرة جداً بالعامية المصرية.")
                    script = res.text
                    tts = gTTS(text=script, lang='ar')
                    tts.save("temp_audio.mp3")
                    audio = AudioFileClip("temp_audio.mp3")
                else:
                    ext = user_audio_file.name.split('.')[-1]
                    audio_path = f"user_audio.{ext}"
                    with open(audio_path, "wb") as f:
                        f.write(user_audio_file.getbuffer())
                    audio = AudioFileClip(audio_path)

                duration = audio.duration

                # 2. جلب خلفية شورتس
                img_url = "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?q=80&w=1080&h=1920&auto=format&fit=crop"
                img_data = requests.get(img_url).content
                with open("bg.jpg", "wb") as f: f.write(img_data)

                # 3. بناء الفيديو (1080x1920)
                bg = ImageClip("bg.jpg").set_duration(duration).resize(height=1920)

                # 4. اللوجو (أعلى اليمين)
                with open("logo_temp.png", "wb") as f: f.write(logo_file.getbuffer())
                logo = (ImageClip("logo_temp.png")
                        .resize(width=180)
                        .set_duration(duration)
                        .set_position(("right", "top"))
                        .margin(right=30, top=30, opacity=0))

                # 5. الدمج النهائي
                final = CompositeVideoClip([bg, logo], size=(1080, 1920))
                final = final.set_audio(audio)
                
                output_file = "mediawy_shorts.mp4"
                final.write_videofile(output_file, fps=24, codec="libx264", audio_codec="aac")

                st.success("✅ تم حل المشكلة التقنية والفيديو جاهز!")
                st.video(output_file)
                
                with open(output_file, "rb") as f:
                    st.download_button("تحميل الفيديو 📥", f, "mediawy_shorts.mp4")

            except Exception as e:
                st.error(f"حدث خطأ أثناء الرندرة: {str(e)}")
    else:
        st.warning("ارفع اللوجو أولاً!")

st.caption("برمجة وتطوير ميدياوي © 2025")

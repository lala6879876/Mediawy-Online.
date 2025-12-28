import os
import subprocess
import sys

# سطر سحري: بيسطب المكتبة الناقصة أوتوماتيك أول ما الموقع يفتح
try:
    import google.generativeai as genai
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

import streamlit as st
import asyncio
import edge_tts

# باقي الكود بتاعك...
st.title("Mediawy Online 🎬")
st.write("أهلاً بك يا محمد في نسختك الأونلاين")

# ... كمل باقي الكود هنا

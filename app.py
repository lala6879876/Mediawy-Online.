import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online", layout="centered")

# تنسيق اللغة العربية (RTL)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stTextInput, .stTextArea { direction: rtl; text-align: right; }
    div[data-testid="stExpander"] { direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

st.title("Mediawy Pro - أونلاين 🎬")

# إعداد المفتاح
genai.configure(api_key="AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE")

# اختيار اللوجو
logo_file = st.file_uploader("ارفع اللوجو الخاص بك", type=['png', 'jpg', 'jpeg'])

if st.button("توليد خطة النشر والسكريبت 🚀"):
    if logo_file:
        with st.spinner("جاري محاولة الاتصال بالذكاء الاصطناعي..."):
            # قائمة بالموديلات الممكنة (عشان لو واحد فشل التاني يلحقه)
            available_models = ['models/gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
            res_text = None
            
            for model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                    response = model.generate_content(prompt)
                    res_text = response.text
                    if res_text:
                        break # لو اشتغل يخرج من اللفة
                except:
                    continue # لو فشل يجرب اللي بعده
            
            if res_text:
                st.success("✅ تم استلام البيانات بنجاح!")
                lines = res_text.split('\n')
                
                st.subheader("🚀 خطة النشر والـ SEO")
                
                # الـ 5 مستطيلات اللي طلبتهم
                st.text_input("1️⃣ العنوان المقترح:", value=lines[0] if len(lines) > 0 else "")
                st.text_area("2️⃣ الوصف (Description):", value=res_text, height=150)
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، تحفيز، ميدياوي، تطوير الذات")
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #تحفيز #ميدياوي #shorts")
                st.info("5️⃣ موعد النشر المثالي: اليوم الساعة 8 مساءً")
                
                st.balloons()
            else:
                st.error("عذراً، موديلات جوجل مشغولة حالياً، جرب تضغط على الزرار مرة تانية.")
    else:
        st.warning("برجاء رفع اللوجو أولاً")

st.markdown("---")
st.caption("برمجة وتطوير ميدياوي © 2025")

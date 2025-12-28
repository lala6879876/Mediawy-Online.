import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Mediawy Online", layout="centered")

# تنسيق اللغة العربية
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stTextInput, .stTextArea { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title("Mediawy Pro - أونلاين 🎬")

# إعداد المفتاح مباشرة والموديل المستقر
genai.configure(api_key="AIzaSyBjAufXabtLWuvQKkCitigiacpKsYRNNOE")

# اختيار الملفات
logo_file = st.file_uploader("ارفع اللوجو الخاص بك", type=['png', 'jpg', 'jpeg'])

# زر البدء
if st.button("توليد خطة النشر والسكريبت 🚀"):
    if logo_file:
        with st.spinner("جاري التوليد..."):
            try:
                # استخدمنا gemini-pro لأنه الأكثر استقراراً ويمنع خطأ 404
                model = genai.GenerativeModel('gemini-pro')
                prompt = "اكتب نصيحة عن النجاح بالعامية المصرية. ثم اقترح: عنوان، وصف، كلمات مفتاحية، هاشتاجات، موعد نشر."
                
                response = model.generate_content(prompt)
                res_text = response.text

                st.success("✅ تم استلام البيانات")

                # تقسيم النص افتراضياً لعرضه في المستطيلات
                lines = res_text.split('\n')

                # المستطيلات الخمسة المطلوبة
                st.subheader("🚀 خطة النشر المقترحة")
                
                st.text_input("1️⃣ عنوان الفيديو:", value=lines[0] if len(lines) > 0 else "")
                
                st.text_area("2️⃣ وصف الفيديو (Description):", value=res_text, height=150)
                
                st.text_input("3️⃣ الكلمات المفتاحية (Tags):", value="نجاح، تحفيز، ميدياوي، تطوير الذات")
                
                st.text_input("4️⃣ الهاشتاجات (Hashtags):", value="#نجاح #تطوير_ذات #ميدياوي #shorts")
                
                st.info(f"5️⃣ موعد النشر المثالي: مساء اليوم الساعة 8")

                st.balloons()
                
            except Exception as e:
                st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("برجاء رفع اللوجو أولاً")

st.markdown("---")
st.caption("برمجة وتطوير ميدياوي © 2025")

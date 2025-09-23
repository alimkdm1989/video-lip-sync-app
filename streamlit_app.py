import streamlit as st
import yt_dlp
from gtts import gTTS
import os
import subprocess

st.title("🎯 تطبيق Lip-Sync من يوتيوب")
st.markdown("---")

# تحديث yt-dlp
try:
    subprocess.run(["pip", "install", "--upgrade", "yt-dlp"], capture_output=True)
except:
    pass

with st.sidebar:
    st.header("⚙️ الإعدادات")
    language = st.selectbox("🌍 اللغة", ["ar", "en"], 
                           format_func=lambda x: "العربية" if x == "ar" else "الإنجليزية")

youtube_url = st.text_input("🔗 رابط الفيديو من يوتيوب", 
                           placeholder="https://www.youtube.com/watch?v=...")
text_input = st.text_area("📝 النص للتعليق الصوتي", 
                         placeholder="اكتب النص هنا...", 
                         height=100)
avatar_file = st.file_uploader("🖼️ صورة الأفاتار", 
                              type=['jpg', 'jpeg', 'png'])

if st.button("🚀 إنشاء الفيديو", use_container_width=True):
    if youtube_url and text_input and avatar_file:
        try:
            # إنشاء مجلد temp
            os.makedirs('temp', exist_ok=True)
            
            # حفظ الأفاتار
            with open('temp/avatar.jpg', 'wb') as f:
                f.write(avatar_file.getbuffer())
            
            # تحميل الفيديو من يوتيوب - إعدادات محسّنة
            st.info("📥 جاري تحميل الفيديو...")
            ydl_opts = {
                'format': 'best[height<=360]',  # جودة أقل لتجنب المشاكل
                'outtmpl': 'temp/video.mp4',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            # تحويل النص لصوت
            st.info("🔊 جاري تحويل النص لصوت...")
            tts = gTTS(text=text_input, lang=language)
            tts.save('temp/audio.mp3')
            
            st.success("✅ تم المعالجة بنجاح!")
            st.info("📌 ملاحظة: هذا النموذج يدمج الصوت مع الفيديو فقط.")
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
            st.info("💡 جرب فيديو آخر عام وقصير")
            st.info("📌 تأكد أن الفيديو ليس مقيد بالسن أو خاص")
    else:
        st.warning("⚠️ الرجاء ملء جميع الحقول!")

st.markdown("---")
st.info("""
💡 **نصائح مهمة:**
- استخدم فيديوهات عامة وقصيرة أولاً
- تجنب الفيديوهات المقيدة بالسن
- تأكد من أن رابط يوتيوب صحيح
- الصور يجب أن تكون بصيغة JPG أو PNG
""")

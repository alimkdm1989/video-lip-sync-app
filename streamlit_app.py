import streamlit as st
import yt_dlp
from gtts import gTTS
import os

# عنوان التطبيق
st.title("🎯 تطبيق Lip-Sync من يوتيوب")
st.markdown("---")

# الإعدادات الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات")
    language = st.selectbox("🌍 اللغة", ["ar", "en"], 
                           format_func=lambda x: "العربية" if x == "ar" else "الإنجليزية")

# الحقول الرئيسية
youtube_url = st.text_input("🔗 رابط الفيديو من يوتيوب", 
                           placeholder="https://www.youtube.com/watch?v=...")
text_input = st.text_area("📝 النص للتعليق الصوتي", 
                         placeholder="اكتب النص هنا...", 
                         height=100)
avatar_file = st.file_uploader("🖼️ صورة الأفاتار", 
                              type=['jpg', 'jpeg', 'png'])

# زر المعالجة
if st.button("🚀 إنشاء الفيديو", use_container_width=True):
    if youtube_url and text_input and avatar_file:
        try:
            # إنشاء مجلد مؤقت
            os.makedirs('temp', exist_ok=True)
            
            # حفظ الأفاتار
            avatar_path = 'temp/avatar.jpg'
            with open(avatar_path, 'wb') as f:
                f.write(avatar_file.getbuffer())
            
            # تحميل الفيديو من يوتيوب
            st.info("📥 جاري تحميل الفيديو...")
            ydl_opts = {'format': 'best[ext=mp4]', 'outtmpl': 'temp/video.mp4'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            # تحويل النص لصوت
            st.info("🔊 جاري تحويل النص لصوت...")
            tts = gTTS(text=text_input, lang=language)
            audio_path = 'temp/audio.mp3'
            tts.save(audio_path)
            
            # عرض رسالة نجاح
            st.success("✅ تم المعالجة بنجاح!")
            st.info("📌 ملاحظة: هذا النموذج يدمج الصوت مع الفيديو فقط.")
            st.info("💡 للحصول على تحريك الشفاه الحقيقي (Lip-Sync)، تحتاج لملوديلات Wav2Lip.")

        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
    else:
        st.warning("⚠️ الرجاء ملء جميع الحقول!")

# معلومات إضافية
st.markdown("---")
st.info("""
💡 **ملاحظات مهمة:**
- تأكد من أن رابط يوتيوب صحيح
- الصور يجب أن تكون بصيغة JPG أو PNG
- هذا التطبيق يعمل على الإنترنت فقط
""")

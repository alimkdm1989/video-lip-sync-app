import streamlit as st
from gtts import gTTS
import os
import shutil

st.set_page_config(page_title="Lip-Sync from YouTube", layout="centered")
st.title("🎯 تطبيق Lip-Sync")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    language = st.selectbox(
        "🌍 اللغة", ["ar", "en"],
        format_func=lambda x: "العربية" if x == "ar" else "الإنجليزية"
    )

# إدخال النص
text_input = st.text_area(
    "📝 النص للتعليق الصوتي",
    placeholder="اكتب النص هنا...",
    height=120
)

# رفع صورة الأفاتار
avatar_file = st.file_uploader(
    "🖼️ صورة الأفاتار",
    type=['jpg', 'jpeg', 'png']
)

# رفع الفيديو (بدل التحميل من يوتيوب)
video_file = st.file_uploader(
    "📥 ارفع الفيديو من جهازك (mp4/mkv/webm)",
    type=['mp4', 'mkv', 'webm']
)

if st.button("🚀 إنشاء الفيديو", use_container_width=True):
    if text_input and avatar_file and video_file:
        try:
            # تنظيف مجلد temp
            if os.path.exists('temp'):
                shutil.rmtree('temp')
            os.makedirs('temp', exist_ok=True)

            # حفظ الأفاتار
            avatar_path = 'temp/avatar.jpg'
            with open(avatar_path, 'wb') as f:
                f.write(avatar_file.getbuffer())

            # حفظ الفيديو
            video_ext = video_file.name.split('.')[-1]
            video_path = f'temp/video.{video_ext}'
            with open(video_path, 'wb') as f:
                f.write(video_file.getbuffer())
            st.success("✅ تم رفع الفيديو بنجاح!")
            st.video(video_path)

            # تحويل النص لصوت
            st.info("🔊 جاري تحويل النص لصوت...")
            tts = gTTS(text=text_input, lang=language)
            audio_path = 'temp/audio.mp3'
            tts.save(audio_path)
            st.success("✅ تم تحويل النص لصوت.")
            st.audio(audio_path)

            st.success("✅ المعالجة تمت بنجاح! (الفيديو + الصوت + الأفاتار محفوظة في temp/)")

        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
    else:
        st.warning("⚠️ الرجاء ملء جميع الحقول (النص + الأفاتار + الفيديو).")

st.markdown("---")
st.info("""
💡 **ملاحظات مهمة:**
- بدل التحميل من يوتيوب: حمّل الفيديو بجهازك باستخدام yt-dlp أو أي أداة، ثم ارفعه هنا.
- استخدم فيديو قصير للتجربة الأولى.
- الملفات تحفظ داخل مجلد `temp/` مؤقتًا.
""")

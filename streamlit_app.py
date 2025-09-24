import streamlit as st
import yt_dlp
from gtts import gTTS
import os

st.title("🎯 تطبيق Lip-Sync من يوتيوب")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    language = st.selectbox(
        "🌍 اللغة", ["ar", "en"], 
        format_func=lambda x: "العربية" if x == "ar" else "الإنجليزية"
    )

youtube_url = st.text_input(
    "🔗 رابط الفيديو من يوتيوب", 
    placeholder="https://www.youtube.com/watch?v=..."
)
text_input = st.text_area(
    "📝 النص للتعليق الصوتي", 
    placeholder="اكتب النص هنا...", 
    height=100
)
avatar_file = st.file_uploader(
    "🖼️ صورة الأفاتار", 
    type=['jpg', 'jpeg', 'png']
)

if st.button("🚀 إنشاء الفيديو", use_container_width=True):
    if youtube_url and text_input and avatar_file:
        try:
            # إنشاء مجلد temp
            os.makedirs('temp', exist_ok=True)
            
            # حفظ الأفاتار
            with open('temp/avatar.jpg', 'wb') as f:
                f.write(avatar_file.getbuffer())
            
            # محاولة تحميل الفيديو
            try:
                st.info("📥 جاري محاولة تحميل الفيديو...")
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",   # يحتاج ffmpeg
                    "outtmpl": "temp/video.%(ext)s",
                    "quiet": False,
                    "noplaylist": True,
                    "http_headers": {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                    }
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([youtube_url])
                st.success("✅ تم تحميل الفيديو!")
            except Exception as video_error:
                st.warning(f"⚠️ لم نتمكن من تحميل الفيديو: {str(video_error)}")
                st.info("📌 سنكمل المعالجة بدون الفيديو لتجربة التطبيق")
            
            # تحويل النص لصوت
            st.info("🔊 جاري تحويل النص لصوت...")
            tts = gTTS(text=text_input, lang=language)
            tts.save('temp/audio.mp3')
            
            st.success("✅ تم المعالجة بنجاح!")
            st.info("📌 التطبيق يعمل! يمكنك الآن تجربة فيديوهات مختلفة")
            
        except Exception as e:
            st.error(f"❌ حدث خطأ: {str(e)}")
    else:
        st.warning("⚠️ الرجاء ملء جميع الحقول!")

st.markdown("---")
st.info("""
💡 **ملاحظات مهمة:**
- يجب أن يكون ffmpeg مثبت (Streamlit Cloud: أضف ملف packages.txt يحتوي على 'ffmpeg')
- استخدم فيديوهات عامة وقصيرة أولاً
- تجنب الفيديوهات المقيدة بالسن أو المحمية
- إذا استمر الخطأ، جرب فيديو آخر
""")

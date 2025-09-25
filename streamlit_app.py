import streamlit as st
import yt_dlp
from gtts import gTTS
import os
import shutil

st.set_page_config(page_title="Lip-Sync from YouTube", layout="centered")
st.title("🎯 تطبيق Lip-Sync من يوتيوب")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    language = st.selectbox(
        "🌍 اللغة", ["ar", "en"],
        format_func=lambda x: "العربية" if x == "ar" else "الإنجليزية"
    )

youtube_url = st.text_input("🔗 رابط الفيديو من يوتيوب", placeholder="https://www.youtube.com/watch?v=...")
text_input = st.text_area("📝 النص للتعليق الصوتي", placeholder="اكتب النص هنا...", height=120)
avatar_file = st.file_uploader("🖼️ صورة الأفاتار", type=['jpg', 'jpeg', 'png'])

st.markdown("**اختياري**: إذا كان الفيديو مقيدًا (محتوى للبالغين أو خاص) يمكنك رفع `cookies.txt` من متصفحك.")
cookies_file = st.file_uploader("📥 ملف الكوكيز (cookies.txt) - اختياري", type=['txt'])

# helper
def save_uploaded_to(path, uploaded_file):
    with open(path, 'wb') as f:
        f.write(uploaded_file.getbuffer())

def download_video_with_fallback(url, out_dir='temp', cookies_path=None):
    os.makedirs(out_dir, exist_ok=True)
    out_template = os.path.join(out_dir, "video.%(ext)s")
    base_opts = {
        "outtmpl": out_template,
        "noplaylist": True,
        "merge_output_format": "mp4",
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
            "Referer": "https://www.youtube.com/"
        },
        # quiet True would hide errors — keep False for debugging
        "quiet": True,
    }
    if cookies_path:
        base_opts["cookiefile"] = cookies_path

    # 1) Try to extract info first (to show formats / detect restrictions)
    try:
        with yt_dlp.YoutubeDL(base_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception as e:
        raise RuntimeError(f"فشل استخراج معلومات الفيديو (ربما 403 أو محمي): {e}")

    # Provide formats to user (if they need to choose)
    formats = info.get("formats", []) if info else []
    # 2) Try download: bestvideo+bestaudio (merge)
    opts = dict(base_opts)
    opts["format"] = "bestvideo+bestaudio/best"
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        # find produced file
        # yt-dlp will merge to .mp4 when merge_output_format specified
        for fname in os.listdir(out_dir):
            if fname.startswith("video.") and fname.lower().endswith((".mp4", ".mkv", ".webm")):
                return os.path.join(out_dir, fname), formats
        # fallback if not found - return generic path
        return os.path.join(out_dir, "video.mp4"), formats
    except Exception as e1:
        # If 403 or merge error, try fallback single-file 'best'
        err = str(e1)
        # Try fallback format
        opts2 = dict(base_opts)
        opts2["format"] = "best"
        try:
            with yt_dlp.YoutubeDL(opts2) as ydl:
                ydl.download([url])
            for fname in os.listdir(out_dir):
                if fname.startswith("video.") and fname.lower().endswith((".mp4", ".mkv", ".webm")):
                    return os.path.join(out_dir, fname), formats
            return os.path.join(out_dir, "video.mp4"), formats
        except Exception as e2:
            # give both errors up
            raise RuntimeError(f"محاولات التحميل فشلت:\nمحاولة الدمج: {err}\nمحاولة fallback: {e2}")

if st.button("🚀 إنشاء الفيديو", use_container_width=True):
    if youtube_url and text_input and avatar_file:
        # تحضير temp
        if os.path.exists('temp'):
            shutil.rmtree('temp')
        os.makedirs('temp', exist_ok=True)

        # حفظ الافاتار
        save_uploaded_to('temp/avatar.jpg', avatar_file)

        # حفظ كوكيز إن وُجدت
        cookies_path = None
        if cookies_file:
            cookies_path = 'temp/cookies.txt'
            save_uploaded_to(cookies_path, cookies_file)

        # محاولة تحميل الفيديو مع واجهات رسائل مفيدة
        st.info("📥 جارٍ محاولة تحميل الفيديو... (قد يستغرق بعض الوقت)")
        try:
            with st.spinner("Downloading..."):
                video_path, formats = download_video_with_fallback(youtube_url, out_dir='temp', cookies_path=cookies_path)
            st.success("✅ تم تحميل الفيديو! الملف: " + video_path)
            # عرض الفيديو داخل التطبيق (إذا أردت)
            try:
                st.video(video_path)
            except Exception:
                st.info("تم تحميل الملف لكن عرض الفيديو داخل Streamlit قد لا يعمل (حجم/صيغة).")
        except Exception as e:
            st.error(f"⚠️ لم نتمكن من تحميل الفيديو: {e}")
            st.warning("اقتراحات: \n- جرّب رفع ملف cookies.txt من متصفحك (إن كان الفيديو مقيدًا).\n- جرّب فيديو عام وشائع للتأكد.\n- كبديل: يمكنك رفع ملف الفيديو مباشرة لاستخدامه في التطبيق.")
            # عرض صيغ متاحة إذا كانت من info (اختياري)
            # عرض uploader لرفع ملف الفيديو محلياً
            uploaded_local = st.file_uploader("أو ارفع ملف فيديو محلي (mp4,mkv,webm)", type=['mp4','mkv','webm'])
            if uploaded_local:
                local_path = 'temp/uploaded_video.' + uploaded_local.name.split('.')[-1]
                save_uploaded_to(local_path, uploaded_local)
                st.success("✅ تم حفظ الفيديو المرفوع محليًا.")
                try:
                    st.video(local_path)
                    video_path = local_path
                except Exception:
                    st.info("تم حفظ الفيديو المرفوع، قد لا يُعرض داخل Streamlit.")
        # تحويل النص لصوت (إذا أردنا دائماً إنشاء الـ audio)
        try:
            st.info("🔊 جاري تحويل النص لصوت...")
            tts = gTTS(text=text_input, lang=language)
            audio_path = 'temp/audio.mp3'
            tts.save(audio_path)
            st.success("✅ تم تحويل النص لصوت.")
            st.audio(audio_path)
        except Exception as e:
            st.error(f"فشل تحويل النص لصوت: {e}")

    else:
        st.warning("⚠️ الرجاء ملء جميع الحقول (رابط + نص + صورة الأفاتار).")

st.markdown("---")
st.info("""
💡 **ملاحظات مهمة:**
- إذا استمر الخطأ 403: جرب تحميل الفيديو محليًا بواسطة `yt-dlp` على جهازك ثم ارفعه هنا.
- لتصدير cookies من المتصفح: استعمل امتداد chromium مثل "Get cookies.txt" واحفظ بصيغة `cookies.txt` (Netscape format).
- احذر من مشاركة ملفات الكوكيز لأنها تحتوي على بيانات الجلسة.
- تأكد أن لديك ffmpeg مثبت (في Streamlit Cloud: ضع ملف `packages.txt` يحوي السطر `ffmpeg`).
""")

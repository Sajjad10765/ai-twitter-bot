import os
import feedparser
import requests

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

print(f"🔍 فحص المتغيرات:")
print(f"- Chat ID موجود؟ {'نعم' if CHAT_ID else 'لا (فارغ!)'}")
print(f"- Telegram Token موجود؟ {'نعم' if TELEGRAM_BOT_TOKEN else 'لا (فارغ!)'}")
print(f"- Gemini API Key موجود؟ {'نعم' if GEMINI_API_KEY else 'لا (فارغ!)'}")

def generate_with_gemini(prompt: str) -> str:
    url = "https://generativelanguage.googleapis.com/vbeta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    res = requests.post(url, headers=headers, json=payload)
    print(f"📡 استجابة Gemini - الكود: {res.status_code}")
    print(f"📄 النص الراجع: {res.text}")
    
    if res.status_code == 200:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        raise Exception(f"Gemini API Error {res.status_code}: {res.text}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    res = requests.post(url, data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
    print(f"📡 استجابة Telegram - الكود: {res.status_code}")
    print(f"📄 الرد: {res.text}")
    return res.json()

print("🔥 يتم توليد المحتوى الذكي...")

try:
    feed = feedparser.parse('https://artificialintelligence-news.com/feed/')
    if feed.entries:
        item = feed.entries0 if hasattr(feed, 'entries0') else feed.entries[0]
        prompt_news = f"""
        Act as a viral, top-tier AI tech Twitter/X influencer.
        Rewrite this news into a punchy, high-engagement tweet (max 280 chars) with 2 relevant hashtags and the link:
        Title: {item.title}
        Link: {item.link}
        """
        res_news = generate_with_gemini(prompt_news)
        send_telegram(f"📰 *خبر تقني جديد*:\n\n{res_news}")
    else:
        print("⚠️ لم يتم العثور على مقالات في الـ RSS Feed.")
except Exception as e:
    print(farror := f"❌ حدث خطأ رئيسي: {e}")

print("✅ انتهى تشغيل السكربت.")

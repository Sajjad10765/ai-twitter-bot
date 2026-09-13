import os
import feedparser
import requests
import google.generativeai as genai

# جلب المفاتيح من الـ Secrets
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

# إعداد مفتاح جوجل
genai.configure(api_key=GEMINI_API_KEY)

def generate_with_gemini(prompt: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # أزلنا الـ parse_mode لتجنب مشاكل الرفض بسبب الرموز
    res = requests.post(url, data={'chat_id': CHAT_ID, 'text': text})
    print(f"📡 استجابة Telegram - الكود: {res.status_code}")
    print(f"📄 الرد: {res.text}")
    return res.json()

print("🔥 جاري جلب الخبر وتوليده بواسطة الذكاء الاصطناعي...")

try:
    feed = feedparser.parse('https://artificialintelligence-news.com/feed/')
    if feed.entries:
        item = feed.entries[0]
        print(f"📌 عنوان الخبر الأصلي: {item.title}")
        
        prompt_news = f"""
        Act as a viral, top-tier AI tech Twitter/X influencer.
        Rewrite this news into a punchy, high-engagement tweet (max 280 chars) with 2 relevant hashtags and the link:
        Title: {item.title}
        Link: {item.link}
        """
        
        res_news = generate_with_gemini(prompt_news)
        print(f"🤖 النص المولّد: {res_news}")
        
        message = f"📰 خبر تقني جديد:\n\n{res_news}"
        send_telegram(message)
        print("✅ تم الإرسال إلى تيليجرام بنجاح!")
    else:
        print("⚠️ لم يتم العثور على مقالات في الـ RSS Feed.")
except Exception as e:
    print(f"❌ حدث خطأ رئيسي: {e}")
    raise e # إجبار الـ Action على الفشل لكي نرى الخطأ بوضوح إذا حدث

print("✅ انتهى تشغيل السكربت.")

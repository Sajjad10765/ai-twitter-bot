import os
import feedparser
import requests

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def generate_with_gemini(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        data = res.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    else:
        raise Exception(f"Gemini API Error {res.status_code}: {res.text}")

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    res = requests.post(url, data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
    return res.json()

print("🔥 يتم توليد المحتوى الذكي...")

# 1. أخبار
feed = feedparser.parse('https://artificialintelligence-news.com/feed/')
if feed.entries:
    item = feed.entries[0]
    prompt_news = f"""
    Act as a viral, top-tier AI tech Twitter/X influencer.
    Rewrite this news into a punchy, high-engagement tweet (max 280 chars) with 2 relevant hashtags and the link:
    Title: {item.title}
    Link: {item.link}
    """
    res_news = generate_with_gemini(prompt_news)
    send_telegram(f"📰 *خبر تقني جديد*:\n\n{res_news}")

# 2. أداة ذكاء اصطناعي (أفلييت)
prompt_ai_tool = """
Act as a pro AI affiliate marketer on Twitter/X.
Write a short, killer, high-converting tweet (max 240 chars) recommending an insane AI tool, with a strong call to action.
"""
res_tool = generate_with_gemini(prompt_ai_tool)
send_telegram(f"🚀 *أداة ذكاء اصطناعي (أفلييت)*:\n\n{res_tool}")

# 3. نكتة / meme تقني
prompt_meme = """
Act as a sarcastic, witty tech Twitter/X creator. Write a short, hilarious, ultra-relatable tech/programming joke or meme text.
"""
res_meme = generate_with_gemini(prompt_meme)
send_telegram(f"🤖 *تغريدة خفيفة / نكتة تقنية*:\n\n{res_meme}")

print("✅ تم إرسال اليومية كُلها بنجاح!")

import os
import feedparser
import requests
import google.generativeai as genai

# جلب المفاتيح بأمان من إعدادات GitHub Secrets
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


def send_telegram(text):
  url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
  res = requests.post(
      url, data={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
  )
  return res.json()


print('🚀 بدء توليد وجبة المحتوى الذكية...')

# 1. سحب وصياغة خبر تقني ساخن
feed = feedparser.parse('https://artificialintelligence-news.com/feed/')
if feed.entries:
  item = feed.entries[0]
  prompt_news = f"""
    Act as a viral, top-tier AI tech Twitter/X influencer. 
    Rewrite this news into a punchy, high-engagement tweet (max 240 chars) with 2 relevant hashtags and the link:
    Title: {item.title}
    Link: {item.link}
    """
  res_news = model.generate_content(prompt_news).text.strip()
  send_telegram(f'📰 *خبر تقني جديد (جاهز للنشر):*\n\n{res_news}')

# 2. توليد تغريدة أداة ذكاء اصطناعي (أفلييت) عالية التحويل
prompt_ai_tool = """
    Act as a pro AI affiliate marketer on Twitter/X. 
    Write a short, killer, high-converting tweet (max 240 chars) recommending an insane AI tool, with a strong call to action and 2 hashtags. Add a placeholder link like [رابط الأفلييت هنا: https://...].
    """
res_tool = model.generate_content(prompt_ai_tool).text.strip()
send_telegram(f'🚀 *أداة ذكاء اصطناعي (أفلييت - طكك):*\n\n{res_tool}')

# 3. توليد ميمة / نكتة تقنية تجيب ريتويت
prompt_meme = """
    Act as a sarcastic, witty tech Twitter/X creator. Write a short, hilarious, ultra-relatable tech/programming joke or meme tweet (max 240 chars) that makes tech people laugh and retweet. Include 2 relevant hashtags.
    """
res_meme = model.generate_content(prompt_meme).text.strip()
send_telegram(f'😂 *ميمة / نكتة تقنية (للتفاعل):*\n\n{res_meme}')

print('✅ تم إرسال الوجبة كاملة بنجاح!')


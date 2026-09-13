
import os
import requests
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

genai.configure(api_key=GEMINI_API_KEY)

print("🔍 بدء اختبار دمج الذكاء الاصطناعي مع تيليجرام...")

# 1. توليد نص تجريبي بواسطة Gemini
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Write a short, punchy 1-sentence tech update about AI.")
    ai_text = response.text.strip()
    print(f"🤖 النص المولّد: {ai_text}")
except Exception as e:
    print(f"❌ خطأ في توليد الذكاء الاصطناعي: {e}")
    raise e

# 2. الإرسال الفوري لتيليجرام
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
res = requests.post(url, data={'chat_id': CHAT_ID, 'text': f"🤖 اختبار مباشر:\n\n{ai_text}"})
print(f"📡 استجابة Telegram - الكود: {res.status_code}")
print(f"📄 الرد: {res.text}")

if res.status_code == 200:
    print("✅ تم الإرسال بنجاح!")
else:
    raise Exception(f"Telegram error: {res.text}")

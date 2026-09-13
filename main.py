import os
import requests

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

print("🔍 فحص الاتصال بـ Telegram...")
print(f"Chat ID المستلم: {CHAT_ID}")

url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {
    'chat_id': CHAT_ID,
    'text': '🚀 تجربة البوت: السلام عليكم! إذا وصلتك هاي الرسالة فالبوت شغال 100%'
}

response = requests.post(url, data=data)

print(f"📡 رمز استجابة تيليجرام: {response.status_code}")
print(f"📄 نص الرد: {response.text}")

if response.status_code == 200:
    print("✅ تم الإرسال للتيليجرام بنجاح!")
else:
    print("❌ فشل الإرسال، تحسس المفاتيح أو الـ Chat ID!")

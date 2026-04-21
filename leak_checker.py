import telebot
import requests

BOT_TOKEN = 'YOUR_BOT_TOKEN' 
RAPIDAPI_KEY = 'YOUR_API_KEY' 

bot = telebot.TeleBot(BOT_TOKEN)

def check_leak(email):
    url = "https://breachdirectory.p.rapidapi.com/"
    querystring = {"func": "auto", "term": email}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "breachdirectory.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        if not data.get('result'):
            return "No leaks found for this email"
        
        result_text = f"found leaked for {email}:\n\n"
        for entry in data['result']:
            source = entry.get('sources', ['unknown sources'])[0]
            has_password = "Yes" if entry.get('hash') else "No"
            result_text += f"🔹 Source: {source}\n   Password: {has_password}\n\n"
        
        return result_text

    except Exception as e:
        return "Error. Try later! ."

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "HAllo! Send me your email for check.\nUse: /check email@example.com")

@bot.message_handler(commands=['check'])
def handle_check(message):
    try:
        email = message.text.split(maxsplit=1)[1]
        bot.send_message(message.chat.id, "Checking database, please wait a second...")
        
        report = check_leak(email)
        bot.send_message(message.chat.id, report)
    except IndexError:
        bot.reply_to(message, "Write your email, foe example: /check mymail@gmail.com")

if __name__ == "__main__":
    print("Bot running...")
    bot.infinity_polling()

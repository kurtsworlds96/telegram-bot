import telebot
from flask import Flask, request
from datetime import datetime

TOKEN = '7853499885:AAHb513s1bwjch8H7r-g4MCbU-H9WpmXl0A'
ADMIN_ID = '7853499885'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/send_code', methods=['POST'])
def receive_code():
    data = request.json
    user = data.get('user')
    code = data.get('code')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if user and code:
        bot.send_message(ADMIN_ID, f"{code}\n\nОтправил: {user}\nВремя: {current_time}")
        return 'OK', 200
    else:
        return 'Ошибка: неверные данные', 400

if __name__ == "__main__":
    import os

    bot.remove_webhook()
    bot.set_webhook(url=f'https://твой-сайт-на-render.onrender.com/{TOKEN}')
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
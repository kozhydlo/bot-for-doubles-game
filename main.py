import telebot
from telebot import types

# Ваш токен бота
TOKEN = '5934353266:AAFbnT36znbxiLsaqixCl20VXA7jQmTC-7c'

discord_link = "discord.com"

# Створення об'єкту бота
bot = telebot.TeleBot(TOKEN)

# Словник для зберігання інформації про гравців
players = {}

# Обробник команди /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in players:
        players[user_id] = {"name": message.from_user.first_name, "playing": False}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Я буду грати")
    item4 = types.KeyboardButton("Дивитися, хто грає")
    item2 = types.KeyboardButton("Діскорд сервер")
    item3 = types.KeyboardButton("Я не буду грати")
    markup.add(item1, item4, item2, item3)
    bot.send_message(user_id, "Ви у грі!", reply_markup=markup)

# Обробник кнопки "Я буду грати"
@bot.message_handler(func=lambda message: message.text == "Я буду грати")
def play(message):
    user_id = message.chat.id
    if user_id in players and not players[user_id]["playing"]:
        players[user_id]["playing"] = True
        bot.send_message(user_id, f"{message.from_user.first_name} грає зараз!")
    elif user_id in players and players[user_id]["playing"]:
        bot.send_message(user_id, "Ви вже граєте!")
    else:
        bot.send_message(user_id, "Спочатку натисніть /start")

# Обробник кнопки "Я не буду грати"
@bot.message_handler(func=lambda message: message.text == "Я не буду грати")
def stop_playing(message):
    user_id = message.chat.id
    if user_id in players and players[user_id]["playing"]:
        players[user_id]["playing"] = False
        bot.send_message(user_id, "Ви більше не граєте.")
    else:
        bot.send_message(user_id, "Ви не граєте зараз.")

# Обробник кнопки "Діскорд сервер"
@bot.message_handler(func=lambda message: message.text == "Діскорд сервер")
def discord_server(message):
    user_id = message.chat.id
    bot.send_message(user_id, f"Ми спілкуємося [Дискорд]({discord_link}).", parse_mode="Markdown")

# Обробник кнопки "Дивитися, хто грає"
@bot.message_handler(func=lambda message: message.text == "Дивитися, хто грає")
def view_players(message):
    user_id = message.chat.id
    playing_players = [player["name"] for player in players.values() if player["playing"]]
    if playing_players:
        bot.send_message(user_id, f"Грають: {', '.join(playing_players)}")
    else:
        bot.send_message(user_id, "Зараз ніхто не грає.")
        
# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)

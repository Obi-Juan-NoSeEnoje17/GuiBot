import telebot
import time
import os
from dotenv import load_dotenv
from utils import bot_manager, points_manager, error_log

load_dotenv()
token =  os.getenv('TOKEN')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['hi'])
def say_hello(message):
    bot_manager.say_hello(bot, message)

@bot.message_handler(commands=['help'])
def show_commands(message):
    bot_manager.show_commands(bot, message)
    
@bot.message_handler(commands=['incoming'])
def print_incoming(message):
    bot_manager.print_incoming(bot, message)

@bot.message_handler(commands=['changeLogs'])
def print_change_logs(message):
    bot_manager.print_changeLogs(bot, message)

@bot.message_handler(commands=['gj'])
def great_work(message):
    bot_manager.great_work(bot, message)

@bot.message_handler(commands=['aj'])
def awfull_work(message):
    bot_manager.awfull_work(bot, message)

@bot.message_handler(commands=['new'])
def new_roadmap(message):
    points_manager.new_roadmap(bot, message)

@bot.message_handler(commands=['add'])
def add_point_of_day(message):
    points_manager.add_point_of_day(bot, message)

@bot.message_handler(commands=['list'])
def list_points_of_day(message):
    points_manager.list_points_of_day(bot, message)

@bot.message_handler(commands=['change'])
def change_order(message):
    points_manager.change_order(bot, message)

@bot.message_handler(commands=['edit'])
def edit_point_of_day(message):
    points_manager.edit_point_of_day(bot, message)

@bot.message_handler(commands=['remove'])
def remove_point_of_day(message):
    points_manager.remove_point_of_day(bot, message)
    
@bot.message_handler(commands=['roadmap'])
def create_roadmap(message):
    points_manager.create_roadmap(bot, message)
    
def run_bot():
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        error_log.write_error(" Bot detenido por el usuario (Ctrl+C)\n")
        bot.stop_polling()
    except Exception as e:
        error_log.write_error(f" Error: {e}. Reintentando en 5 segundos...\n")
        time.sleep(5)
        run_bot()

if __name__ == '__main__':
    run_bot()
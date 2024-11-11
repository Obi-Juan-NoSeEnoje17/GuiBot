'''
GuiBot - Telegram bot to manage the meeting documents of Universidad
de Valladolid's Grupo Universitario de Informática (GUI).
Copyright (C) 2024  Obi-Juan-NoSeEnoje17

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
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
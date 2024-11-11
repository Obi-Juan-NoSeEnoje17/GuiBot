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
from . import bot_utils

commands = {
    "help": 
        "/help [comando] \n" \
        "Muestra ayuda general o de dicho comando. \n" \
        "Argumentos: \n" \
        " - comando: comando existente.",
    
    "incoming": 
        "/incoming \n" \
        "Muestra las mejoras venideras.",
    
    "changeLogs": 
        "/changeLogs \n" \
        "Muestra los cambios de la última actualización.",
    
    "new": 
        "/new tipo_reunión \n" \
        "Genera un nuevo documento para guardar los puntos del día. Puede haber un documento abierto por cada tipo. \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'.",
    
    "add" : 
        "/add tipo_reunión punto_del_día [descripción] \n" \
        "Añade un punto del día con su descripción. \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - punto_del_día: Título del punto del día a añadir. \n" \
        " - descripción: Descripción del punto del día a añadir.",
    
    "list" : 
        "/list tipo_reunión [punto_del_día] \n" \
        "Muestra todos los puntos del día existentes o la descripción de un punto del día. \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - punto_del_día: Número del punto del día a ver su descripción.",
    
    "change" : 
        "/cambio tipo_reunión punto_del_día_1 punto_del_día_2 [punto_del_día_3] \n" \
        "Cambia el orden del punto del día 1 por el punto del día 2, si se indica un tercero, se coloca el primero entre los dos siguientes. \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - punto_del_día_n: Número de un punto del día.",
    
    "edit" : 
        "/edit tipo_reunión punto_del_día nueva_descripción \n" \
        "Edita la descripción del punto del día \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - punto_del_día: Número del punto del día a ver su descripción. \n" \
        " - nueva_descripción: Nueva descripción del punto del día.",

    "remove" : 
        "/remove tipo_reunión punto_del_día \n" \
        "Elimina uno de los puntos del día \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - punto_del_día: Número del punto del día a eliminar.",
    
    "roadmap" : 
        "/roadmap tipo_reunión fecha_reunión \n" \
        "Genera el documento .tex de la reunión \n" \
        "Argumentos: \n" \
        " - tipo_reunión: 'Junta' o 'Asamblea'. \n" \
        " - fecha_reunión: fecha de reunión en formato dd-mm-aaaa."
}

def say_hello(bot, message):
    bot.send_message(message.chat.id, "Muy buenas, mi nombre es JuanBot, y he sido creado para generar la plantilla de las juntas y asambleas", message_thread_id = message.message_thread_id)

def show_commands(bot, message):
    """
        Show all commands help
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 1 and len(command_parts) != 2:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help help", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 1:
        overallhelp = "Comandos existentes: \n"
        for command in commands.keys():
            overallhelp += " -" + command + "\n"
        bot.send_message(message.chat.id, overallhelp, message_thread_id = message.message_thread_id)
    elif len(command_parts) == 2:
        bot.send_message(message.chat.id, commands.get(command_parts[1], "Comando desconocido"), message_thread_id = message.message_thread_id)

def print_incoming(bot, message):
    """
        Show incoming commands and features
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 1:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help incoming", message_thread_id = message.message_thread_id)
    else:
        bot.send_message(message.chat.id, "/edit", message_thread_id = message.message_thread_id)
        
def print_changeLogs(bot, message):
    """
        Show the latest update changes
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 1:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help changeLogs", message_thread_id = message.message_thread_id)
    else:
        changes_message = "Cambio realizados: \n"
        with open('src/utils/logs/change_logs.log', 'r') as change_logs_reader:
            for change in change_logs_reader:
                changes_message += change
        bot.send_message(message.chat.id, changes_message, message_thread_id = message.message_thread_id)

def great_work(bot, message):
    """
        Send recognition to a member
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    if message.from_user.username == 'NoSeEnoje17' and len(message.text.split(" ")) == 2:
        bot.send_message(message.chat.id, "Muy bien " + message.text.split(" ")[1] + ". Estás haciendo un buen trabajo, sigue así", message_thread_id = message.message_thread_id)
    
def awfull_work(bot, message):
    """
        Encorage a member
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    if message.from_user.username == 'NoSeEnoje17' and len(message.text.split(" ")) == 2:
        bot.send_message(message.chat.id, "Muy mal " + message.text.split(" ")[1] + ". Debes ponerte las pilas o tendré que darte con el palo. No me obligues, que sé que lo puedes hacer mejor. \nLETS GOOO QUE TU PUEDES!!!", message_thread_id = message.message_thread_id)
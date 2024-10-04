import telebot
from create_latex_context import *
TOKEN = "7653047311:AAF2We2sxsdvvln-qdg0srosF2JcBO5mS8M"
bot = telebot.TeleBot(TOKEN)

def format_date_date(date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    return day + " " + month + " " + year

def format_date_title(date):
    day = date.split("-")[0]
    month = date.split("-")[1]
    year = date.split("-")[2]
    return year + "-" + month + "-" + day

def check_date(date):
    return len(date.split("-")) != 3

@bot.message_handler(commands=['roadmap'])
def create_roadmap(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 3:
        bot.reply_to(message,"Uso de comando: \n/roadmap tipo fecha \nTipo: 'Junta' o 'Asamblea'\nFecha: dd-mm-aaaa (17-Mayo-2003)")

    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message,"Uso de comando: \n/roadmap tipo fecha \nTipo: 'Junta' o 'Asamblea'\nFecha: dd-mm-aaaa (17-Mayo-2003)")

    elif check_date(command_parts[2]):
        bot.reply_to(message,"Uso de comando: \n/roadmap tipo fecha \nTipo: 'Junta' o 'Asamblea'\nFecha: dd-mm-aaaa (17-Mayo-2003)")

    else:    
        type = command_parts[1].capitalize()
        date = command_parts[2]
        try:
            latex_content = create_latex_content(type, format_date_date(date))
            roadmap_name = format_date_title(date) + ".tex"
            with open(roadmap_name, "w") as new_roadmap:
                new_roadmap.write(latex_content)

            with open(roadmap_name, "rb") as send_roadmap:
                bot.send_document(message.chat.id, send_roadmap)
                bot.send_message(message.chat.id, "Para eliminar el arhicvo con los puntos del día puede ejecutar /delete o /new")
        except Exception as e:
            bot.reply_to(message, "Error al crear el PDF\n" + str(e))

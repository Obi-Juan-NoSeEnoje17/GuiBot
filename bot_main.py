import telebot
import time
import os
from dotenv import load_dotenv
from bot_utils import *

load_dotenv()
token =  os.getenv('TOKEN')

bot = telebot.TeleBot(token)  

@bot.message_handler(commands=['hola'])
def say_hello(message):
    bot.send_message(message.chat.id, "Muy buenas, mi nombre es JuanBot, y he sido creado para generar la plantilla de las juntas y asambleas", message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['help'])
def show_commands(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 1 and len(command_parts) != 2:
        bot.reply_to(message, "Uso de comando \n/help : muestra ayuda general \n/help comando : muestra ayuda específica", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 1:
        overall_help = "Comandos existentes : /hola /help /new /add /list /change /remove /roadmap\nUtilice /help comando para ver el uso de dicho comando"
        bot.send_message(message.chat.id, overall_help, message_thread_id = message.message_thread_id)
    elif len(message.text.split(" ")) == 2:
        commands = {
            "help" : "/help [comando] \nMuestra ayuda general o de dicho comando \ncomando: comando existente.",
            "new" : "/new tipo_reunión\nGenera un nuevo documento para guardar los puntos del día\ntipo_reunión: 'Junta' o 'Asamblea'\nPuede haber un documento abierto por cada tipo.",
            "add" : "/add tipo_reunión punto_del_dia [descripción]\nAñade al documento existente el punto del día con su descripción\ntipo_reunión: 'Junta' o 'Asamblea'",
            "list" : "/list tipo_reunión [punto_del_día]\nMuestra todos los puntos del día existentes, sin la descripción, salvo que se indique dicho punto del día\ntipo_reunión: 'Junta' o 'Asamblea'",
            "change" : "/cambio tipo_reunión num_punto_del_dia_1 num_punto_del_dia_2 \nCambia el orden de los puntos del día\ntipo_reunión: 'Junta' o 'Asamblea'",
            "roadmap" : "/roadmap tipo fecha \nGenera el documento .tex \ntipo: 'Junta' o 'Asamblea' \nfecha: celebración de dicha reunión en formato dd-mm-aaaa",
            "remove" : "/remove tipo_reunión punto_del_día\nElimina uno de los puntos del día\ntipo_reunión: 'Junta' o 'Asamblea'"
        }
        bot.send_message(message.chat.id, commands.get(message.text.split(" ")[1], "Comando desconocido"), message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['new'])
def new_roadmap(message):
    command_parts = message.text.split(" ")
    if len(command_parts) == 2 and len(command_parts) != 3:
        bot.send_message(message.chat.id, "WARNING: /new va a borrar todo el contenido actual, si aún así quiere continuar, ejecute '/new ToySeguroJefe'", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != 'Junta' and command_parts[1].capitalize() != 'Asamblea':
        bot.reply_to(message, "El tipo de documento debe ser 'Junta' o 'Asamblea'")
    else:
        type = command_parts[1].capitalize()
        try:
            with open("points_of_day_" + type + ".txt", "w") as points_of_day_write:
                points_of_day_write.write("")
        except Exception:
            bot.reply_to(message, "Error al crear archivo de puntos a hablar", message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['add'])
def add_point_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) < 3:
        bot.reply_to(message,"Uso de comando: \n/add punto_del_dia tipo_reunión [descripción]", message_thread_id = message.message_thread_id)
    else:
        new_point_of_day = command_parts[2]
        type = command_parts[1].capitalize()
        try: 
            with open('points_of_day_' + type + '.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if (point_of_day.strip().split(":")[0] == new_point_of_day):
                        bot.reply_to(message, "Punto del día añadido anteriormente", message_thread_id = message.message_thread_id)
                        return
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
        with open('points_of_day_' + type + '.txt', 'a') as points_of_day_write:
            points_of_day_write.write(new_point_of_day + ": ")
            for desc in command_parts[3:]:
                points_of_day_write.write(desc + " ")
            points_of_day_write.write("\n")

@bot.message_handler(commands=['list'])
def list_points_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2 and len(command_parts) != 3:
        bot.reply_to(message, "Uso de comando: \n/list tipo_reunión [punto_del_día]", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 2:
        try: 
            type = command_parts[1].capitalize()
            list_points_of_day = "Puntos del diá de la próxima " + type + ":\n"
            with open('points_of_day_' + type + '.txt', 'r') as points_of_day_read:
                contador = 1
                for point_of_day in points_of_day_read:
                    list_points_of_day = list_points_of_day + str(contador) + ": " + point_of_day.split(":")[0] + "\n"
                    contador = contador + 1
            bot.send_message(message.chat.id, list_points_of_day, message_thread_id = message.message_thread_id)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
    else:
        try:
            type = command_parts[1].capitalize()
            command = command_parts[2] 
            desc_points_of_day = "Descripción de " + command + "\n"
            with open('points_of_day_' + type + '.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if point_of_day.split(":")[0] == command:
                        bot.send_message(message.chat.id, desc_points_of_day + point_of_day, message_thread_id = message.message_thread_id)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
        
@bot.message_handler(commands=['change'])
def change_order_points_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 4:
        bot.reply_to(message, "Uso de comando: \n/cambio tipo_reunión punto_del_dia_1 punto_del_dia_2", message_thread_id = message.message_thread_id)
    else:
        type = command_parts[1].capitalize()
        first_point_of_day = int(command_parts[2])
        second_point_of_day = int(command_parts[3])
        with open('points_of_day_' + type + '.txt', 'r') as points_of_day_read:
            list_points_of_day = points_of_day_read.readlines()
            number_points_of_day = len(list_points_of_day)
        if number_points_of_day < first_point_of_day or number_points_of_day < second_point_of_day:
            bot.reply_to(message, "Indices de puntos del día erróneos, intentelo de nuevo", message_thread_id = message.message_thread_id)
        else:
            list_points_of_day[first_point_of_day-1], list_points_of_day[second_point_of_day-1] = list_points_of_day[second_point_of_day-1], list_points_of_day[first_point_of_day-1]
            with open('points_of_day_' + type + '.txt', 'w') as points_of_day_write:
                points_of_day_write.writelines(list_points_of_day)

@bot.message_handler(commands=['remove'])
def remove_point_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 3:
        bot.reply_to(message, "Uso de comando: \n/remove tipo_reunión punto_del_día", message_thread_id = message.message_thread_id)
    else:
        type = command_parts[1]
        point_of_day_to_remove = command_parts[2]
        try: 
            actual_points_of_day = []
            with open('points_of_day_'+type+'.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if (point_of_day.split(":")[0] != point_of_day_to_remove):
                        actual_points_of_day.append(point_of_day)
            with open('points_of_day_'+type+'.txt', 'w') as points_of_day_write:
                for point_of_day in actual_points_of_day:
                    points_of_day_write.write(point_of_day)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día", message_thread_id = message.message_thread_id) 

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


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text, message_thread_id = message.message_thread_id)

def run_bot():
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("Bot detenido por el usuario (Ctrl+C)")
        bot.stop_polling() 
    except Exception as e:
        print(f"Error: {e}. Reintentando en 5 segundos...")
        time.sleep(5)
        run_bot()

if __name__ == '__main__':
    run_bot()
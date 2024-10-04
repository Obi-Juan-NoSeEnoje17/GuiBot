import telebot
import time
TOKEN = "7653047311:AAF2We2sxsdvvln-qdg0srosF2JcBO5mS8M" 
bot = telebot.TeleBot(TOKEN)  
from roadmap import *

@bot.message_handler(commands=['hola'])
def say_hello(message):
    bot.send_message(message.chat.id, "Muy buenas, mi nombre es JuanBot, y he sido creado para generar la plantilla de las juntas y asambleas", message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['help'])
def show_commands(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 1 and len(command_parts) != 2:
        bot.reply_to(message, "Uso de comando \n/help : muestra ayuda general \n/help comando : muestra ayuda específica", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 1:
        overall_help = "Comandos existentes : /help /new /add /roadmap /delete \nUtilice /help comando para ver el uso de dicho comando"
        bot.send_message(message.chat.id, overall_help, message_thread_id = message.message_thread_id)
    elif len(message.text.split(" ")) == 2:
        commands = {
            "help" : "/help [comando] \nMuestra ayuda general o de dicho comando \ncomando: comando existente",
            "new" : "/new \nGenera un nuevo documento para guardar los puntos del día",
            "add" : "/add punto_del_dia [descripción]\nAñade al documento existente el punto del día con su descripción",
            "list" : "/list [punto_del_día]\nMuestra todos los puntos del día existentes, sin la descripción, salvo que se indique dicho punto del día",
            "roadmap" : "/roadmap tipo fecha \nGenera el documento .tex \ntipo: 'Junta' o 'Asamblea' \nfecha: celebración de dicha reunión en formato dd-mm-aaaa",
            "remove punto_del_día" : "Elimina uno de los puntos del día",
            "delete" : "Elimina manualmente el archivo de puntos del día. Si se ejecuta /new se reemplaza por otro"
        }
        bot.send_message(message.chat.id, commands.get(message.text.split(" ")[1], "Comando desconocido"), message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['new'])
def new_roadmap(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 1:
        bot.reply_to(message,"Uso de comando: \n/new", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 1:
        bot.send_message(message.chat.id, "WARNING: /new va a borrar todo el contenido actual, si aún así quiere continuar, ejecute '/new ToySeguroJefe'", message_thread_id = message.message_thread_id)
    else:
        try:
            with open("points_of_day.txt", "w") as points_of_day_write:
                points_of_day_write.write("")
        except Exception:
            bot.reply_to(message, "Error al crear archivo de puntos a hablar", message_thread_id = message.message_thread_id)
        bot.send_message(message.chat.id, "Archivo creado", message_thread_id = message.message_thread_id)   


@bot.message_handler(commands=['add'])
def add_point_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) < 2:
        bot.reply_to(message,"Uso de comando: \n/add punto_del_dia [descripción]", message_thread_id = message.message_thread_id)
    else:
        new_point_of_day = command_parts[1]
        try: 
            with open('points_of_day.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if (point_of_day.strip() == "PDD: " + new_point_of_day):
                        bot.reply_to(message, "Punto del día añadido anteriormente", message_thread_id = message.message_thread_id)
                        return
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)

        with open('points_of_day.txt', 'a') as points_of_day_write:
            points_of_day_write.write("PDD: " + new_point_of_day + "-")
            for desc in command_parts[2:]:
                points_of_day_write.write(desc + " ")
            points_of_day_write.write("\n")
        bot.send_message(message.chat.id,  new_point_of_day + " añadido a los puntos del día", message_thread_id = message.message_thread_id)

@bot.message_handler(commands=['list'])
def list_points_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 1 and len(command_parts) != 2:
        bot.reply_to(message, "Uso de comando: \n/list [punto_del_día]", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 1:
        try: 
            list_points_of_day = "Puntos del diá:\n"
            with open('points_of_day.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    list_points_of_day = list_points_of_day + point_of_day.split("-")[0].replace("PDD: " , "") + "\n"
            bot.send_message(message.chat.id, list_points_of_day, message_thread_id = message.message_thread_id)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
    else:
        try:
            command = command_parts[1] 
            list_points_of_day = "Descripción de\n"
            with open('points_of_day.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if point_of_day.split("-")[0] == "PDD: " + command:
                        bot.send_message(message.chat.id, point_of_day.split("-")[0] + ": " + point_of_day.split("-")[1], message_thread_id = message.message_thread_id)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
        
    

@bot.message_handler(commands=['remove'])
def remove_point_of_day(message):
    command_parts = message.text.split(" ")
    if len(command_parts) != 2:
        bot.reply_to(message, "Uso de comando: \n/remove punto_del_día", message_thread_id = message.message_thread_id)
    else:
        point_of_day_to_remove = command_parts[1]
        try: 
            with open('points_of_day.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if (point_of_day.split("-")[0] == "PDD: " + point_of_day_to_remove):
                        position = point_of_day
                        actual_points_of_day = points_of_day_read.readlines()
                        with open('points_of_day.txt' , 'w') as points_of_day_write:
                            for point_of_day_eliminate, point_of_day in enumerate(actual_points_of_day):
                                if point_of_day_eliminate != position:
                                    points_of_day_write.write(point_of_day)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día", message_thread_id = message.message_thread_id) 

@bot.message_handler(commands=['delete'])
def delete(message):
    bot.reply_to(message.text, "Comando no implementado, en proceso...", message_thread_id = message.message_thread_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text, message_thread_id = message.message_thread_id)
    #message_thread_id = message.message_thread_id

def run_bot():
    try:
        bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("Bot detenido por el usuario (Ctrl+C)")
        bot.stop_polling() 
    except Exception as e:
        print(f"Error: {e}. Reintentando en 15 segundos...")
        time.sleep(15)
        run_bot()

if __name__ == '__main__':
    run_bot()

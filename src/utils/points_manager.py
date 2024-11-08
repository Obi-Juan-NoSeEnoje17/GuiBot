from . import bot_utils

def new_roadmap(bot, message):
    """
        Creates new file to save points of day
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 3:
        bot.send_message(message.chat.id, "WARNING: /new va a borrar todo el contenido actual, si aún así quiere continuar, ejecute '/new tipo_reunion confirmacion'", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message,"Error en comando: tipo_reunion \nEjecute /help new", message_thread_id = message.message_thread_id)
    elif command_parts[2] == "confirmacion":
        meeting_type = command_parts[1].capitalize()
        try:
            with open("src/meeting_files/points_of_day_" + meeting_type + ".txt", "w") as points_of_day_write:
                points_of_day_write.write("")
        except Exception:
            bot.reply_to(message, "Error al crear el archivo nuevo", message_thread_id = message.message_thread_id)
    else:
        bot.reply_to(message, "Error en comando: confirmacion \nEjecute /help new", message_thread_id = message.message_thread_id)

def add_point_of_day(bot, message):
    """
        Add a point of day to the current meeting file
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text.replace("\n", " "))
    if len(command_parts) < 3:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help add", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message,"Error en comando: tipo_reunion \nEjecute /help add", message_thread_id = message.message_thread_id)
    else:
        meeting_type = command_parts[1].capitalize()
        new_point_of_day = command_parts[2]
        try:
            with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'r') as points_of_day_read:
                for point_of_day in points_of_day_read:
                    if (point_of_day.strip().split(":")[0] == new_point_of_day):
                        bot.reply_to(message, "Punto del día añadido anteriormente", message_thread_id = message.message_thread_id)
                        return
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
            
        with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'a') as points_of_day_write:
            points_of_day_write.write(new_point_of_day + ": ")
            for desc in command_parts[3:]:
                points_of_day_write.write(desc + " ")
            points_of_day_write.write("\n")

def list_points_of_day(bot, message):
    """
        List all te current points of day of the meeting, or list the description of a determine point_of_day
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 2 and len(command_parts) != 3:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help list", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message,"Error en comando: tipo_reunion \nEjecute /help list", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 2:
        try:
            meeting_type = command_parts[1].capitalize()
            list_points_of_day = "Puntos del día de la próxima " + meeting_type + ":\n"
            with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'r') as points_of_day_read:
                contador = 1
                for point_of_day in points_of_day_read:
                    list_points_of_day = list_points_of_day + str(contador) + ": " + point_of_day.split(":")[0] + "\n"
                    contador = contador + 1
            bot.send_message(message.chat.id, list_points_of_day, message_thread_id = message.message_thread_id)
        except IOError:
            bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
    else:
        try:
            command = int(command_parts[2])
            try:
                meeting_type = command_parts[1].capitalize()
                desc_points_of_day = "Descripción de "
                with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'r') as points_of_day_read:
                    for line_number, point_of_day in enumerate(points_of_day_read, start=1):
                        if line_number == command:
                            bot.send_message(message.chat.id, desc_points_of_day + point_of_day.split(": ")[0] + " \n" + point_of_day.split(": ")[1], message_thread_id = message.message_thread_id)
            except IOError:
                bot.reply_to(message, "No existe ningún archivo de puntos del día, puede crearlo con /new", message_thread_id = message.message_thread_id)
        except ValueError:
            bot.reply_to(message, "Error en comando: punto_del_día \nEjecute /help list", message_thread_id = message.message_thread_id)

def change_order(bot, message):
    """
        Change the order of the points of day of the meeting file
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 4 and len(command_parts) != 5:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help change", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message, "Error en comando: tipo_reunion \nEjecute /help change", message_thread_id = message.message_thread_id)
    elif len(command_parts) == 4:
        try:
            first_point_of_day = int(command_parts[2])
            second_point_of_day = int(command_parts[3])
            meeting_type = command_parts[1].capitalize()
            with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'r') as points_of_day_read:
                list_points_of_day = points_of_day_read.readlines()
                number_points_of_day = len(list_points_of_day)
            if number_points_of_day < first_point_of_day or number_points_of_day < second_point_of_day:
                bot.reply_to(message, "Error en comando: point_of_day \nEjecute /help change", message_thread_id = message.message_thread_id)
            else:
                list_points_of_day[first_point_of_day-1], list_points_of_day[second_point_of_day-1] = list_points_of_day[second_point_of_day-1], list_points_of_day[first_point_of_day-1]
                with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'w') as points_of_day_write:
                    points_of_day_write.writelines(list_points_of_day)
        except ValueError:
            bot.reply_to(message, "Error en comando: punto_del_día \nEjecute /help change", message_thread_id = message.message_thread_id)
    else:
        try:
            first_point_of_day = int(command_parts[2])
            second_point_of_day = int(command_parts[3])
            third_point_of_day = int(command_parts[4])
            meeting_type = command_parts[1].capitalize()
            with open('src/meeting_files/points_of_day_' + meeting_type + '.txt', 'r') as points_of_day_read:
                list_points_of_day = points_of_day_read.readlines()
                number_points_of_day = len(list_points_of_day)
            if number_points_of_day < first_point_of_day or number_points_of_day < second_point_of_day or number_points_of_day < third_point_of_day:
                bot.reply_to(message, "Error en comando: point_of_day \nEjecute /help change", message_thread_id = message.message_thread_id)
            else:
                # TODO
                pass
        except ValueError:
            bot.reply_to(message, "Error en comando: punto_del_día \nEjecute /help change", message_thread_id = message.message_thread_id)

def edit_point_of_day(bot, message):
    bot.send_message(message.chat.id, "En proceso jiji \n", message_thread_id = message.message_thread_id)

def remove_point_of_day(bot, message):
    """
        Remove a point of day of the meeting file
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 3:
        bot.reply_to(message, "Error en comando: formato \nEjecute /help remove", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message, "Error en comando: tipo_reunion \nEjecute /help remove", message_thread_id = message.message_thread_id)
    else:
        meeting_type = command_parts[1].capitalize()
        try:
            point_of_day_to_remove = int(command_parts[2])
            try:
                actual_points_of_day = []
                with open('src/meeting_files/points_of_day_'+ meeting_type+'.txt', 'r') as points_of_day_read:
                    for line_number, point_of_day in enumerate(points_of_day_read, start=1):
                        if line_number != point_of_day_to_remove:
                            actual_points_of_day.append(point_of_day)
                            
                with open('src/meeting_files/points_of_day_'+meeting_type+'.txt', 'w') as points_of_day_write:
                    for point_of_day in actual_points_of_day:
                        points_of_day_write.write(point_of_day)
            except IOError:
                bot.reply_to(message, "No existe ningúnrchivo de puntos del día", message_thread_id = message.message_thread_id)
        except ValueError:
            bot.reply_to(message, "Error en comando: point_of_day \nEjecute /help remove", message_thread_id = message.message_thread_id)

def create_roadmap(bot, message):
    """
        Create the .tex file of the current points of the of the meeting
    Args:
        bot (Telebot): GuiBot
        message (Message): message with command information
    """
    command_parts = bot_utils.split_command(message.text)
    if len(command_parts) != 3:
        bot.reply_to(message,"Error en comando: formato \nEjecute /help roadmap", message_thread_id = message.message_thread_id)
    elif command_parts[1].capitalize() != "Junta" and command_parts[1].capitalize() != "Asamblea":
        bot.reply_to(message,"Error en comando: tipo_reunion \nEjecute /help roadmap", message_thread_id = message.message_thread_id)
    elif bot_utils.check_date(command_parts[2]):
        bot.reply_to(message,"Error en comando: fecha\nEjecute /help roadmap", message_thread_id = message.message_thread_id)
    else:
        meeting_type = command_parts[1].capitalize()
        date = command_parts[2]
        try:
            latex_content = bot_utils.create_latex_content(meeting_type, bot_utils.format_date_date(date))
            roadmap_name = "src/tex_files/"+bot_utils.format_date_title(date) + ".tex"
            with open(roadmap_name, "w") as new_roadmap:
                new_roadmap.write(latex_content)

            with open(roadmap_name, "rb") as send_roadmap:
                bot.send_document(message.chat.id, send_roadmap)
                bot.send_message(message.chat.id, "Para eliminar el arhicvo con los puntos del día puede ejecutar /delete o /new")
        except Exception as e:
            bot.reply_to(message, "Error al crear el PDF\n" + str(e))
from datetime import datetime

def write_error(error_message):
    with open("src/utils/logs/error.log" , 'a') as error_writer:
        error_writer.write(datetime.now().strftime("%d de %B de %Y, %I:%M %p") + error_message)

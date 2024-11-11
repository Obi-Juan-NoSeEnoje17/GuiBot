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
from datetime import datetime

def write_error(error_message):
    with open("src/utils/logs/error.log" , 'a') as error_writer:
        error_writer.write(datetime.now().strftime("%d de %B de %Y, %I:%M %p") + error_message)

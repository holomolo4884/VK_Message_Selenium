"""
Инициализация пакета src.
Экспортирует все основные функции для удобного импорта.
"""

# Импортируем все основные функции и константы
from src.config import USER_ID, MESSAGE_TEXT, COOKIES_FILE, HEADLESS_MODE, PROFILE_DIR
from src.driver_setup import setup_driver
from src.auth import check_auth, manual_auth, handle_auth
from src.messenger import find_message_input, send_message_safely, go_to_dialog
from src.utils import save_cookies, load_cookies, clear_browser_data, remove_cookies_file

# Указываем, что экспортируется при использовании "from src import *"
__all__ = [
    'USER_ID',
    'MESSAGE_TEXT',
    'COOKIES_FILE',
    'HEADLESS_MODE',
    'PROFILE_DIR',
    'setup_driver',
    'check_auth',
    'manual_auth',
    'handle_auth',
    'find_message_input',
    'send_message_safely',
    'go_to_dialog',
    'save_cookies',
    'load_cookies',
    'clear_browser_data',
    'remove_cookies_file'
]
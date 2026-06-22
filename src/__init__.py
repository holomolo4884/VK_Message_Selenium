"""
Пакет для автоматизации ВКонтакте.

Этот пакет предоставляет инструменты для:
- Авторизации в ВКонтакте
- Отправки сообщений
- Работы с cookies
- Логирования действий

Основные модули:
    config      - настройки проекта
    driver_setup - настройка браузера
    auth        - авторизация и cookies
    messenger   - отправка сообщений
    logger      - логирование
    retry       - повторные попытки
    utils       - вспомогательные функции
"""

# Экспортируем основные функции и константы
from src.config import (
    USER_IDS,
    MESSAGE_TEXT,
    COOKIES_FILE,
    HEADLESS_MODE,
    PROFILE_DIR,
    DELAY_BETWEEN_MESSAGES,
    MAX_RETRIES
)

from src.driver_setup import setup_driver
from src.auth import check_auth, manual_auth, handle_auth
from src.messenger import (
    find_message_input,
    send_message_to_user,
    send_messages_to_multiple,
    go_to_dialog
)
from src.utils import save_cookies, load_cookies, clear_browser_data, remove_cookies_file
from src.logger import logger
from src.retry import retry

# Указываем, что экспортируется при использовании "from src import *"
__all__ = [
    # Конфигурация
    'USER_IDS',
    'MESSAGE_TEXT',
    'COOKIES_FILE',
    'HEADLESS_MODE',
    'PROFILE_DIR',
    'DELAY_BETWEEN_MESSAGES',
    'MAX_RETRIES',
    
    # Драйвер
    'setup_driver',
    
    # Авторизация
    'check_auth',
    'manual_auth',
    'handle_auth',
    
    # Сообщения
    'find_message_input',
    'send_message_to_user',
    'send_messages_to_multiple',
    'go_to_dialog',
    
    # Утилиты
    'save_cookies',
    'load_cookies',
    'clear_browser_data',
    'remove_cookies_file',
    
    # Логирование
    'logger',
    
    # Декораторы
    'retry'
]
"""
Конфигурационный файл проекта.
Содержит все настройки, которые пользователь может изменять.
Поддерживает загрузку из .env файла.
"""

import os
from dotenv import load_dotenv


# Загружаем переменные из .env файла (если есть)
load_dotenv()


# НАСТРОЙКА ПРОЕКТА

# ID пользователей или группы ВКонтакте, кому отправляем сообщение
# Можно взять из ссылки на профиль: vk.com/id123456789
USER_IDS = os.getenv("VK_USER_IDS").split(',')
# "580765950 "Привет леди ди, это сообщение отправлено автоматически!" "vk_cookies.pkl""
# Очищаем от пробелов
USER_IDS = [uid.strip() for uid in USER_IDS if uid.strip()]

# Текст сообщения (можно загрузить из файла или переменной)
MESSAGE_TEXT = os.getenv("VK_MESSAGE_TEXT")

# Файл для хранения cookies
COOKIES_FILE = os.getenv("VK_COOKIES_FILE", )

# Режим работы браузера
HEADLESS_MODE = os.getenv("VK_HEADLESS_MODE").lower() == "true"

# Папка с профилем Chrome
PROFILE_DIR = os.getenv("VK_PROFILE_DIR")

# Задержки между отправками (сек)
DELAY_BETWEEN_MESSAGES = int(os.getenv("VK_DELAY_SECONDS"))

# Максимальное количество попыток
MAX_RETRIES = int(os.getenv("VK_MAX_RETRIES"))


# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ

# Путь к папке с вложениями (фото, документы)
ATTACHMENTS_DIR = os.path.join(os.getcwd(), "attachments")
if not os.path.exists(ATTACHMENTS_DIR):
    os.makedirs(ATTACHMENTS_DIR)

# Папка для логов
LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

print(f"📋 Настройки загружены:")
print(f"   Получатели: {USER_IDS}")
print(f"   Режим headless: {HEADLESS_MODE}")
print(f"   Задержка: {DELAY_BETWEEN_MESSAGES} сек")
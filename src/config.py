"""
Конфигурационный файл проекта.

Содержит все настройки проекта. Поддерживает загрузку из .env файла.
Если переменная не найдена в .env, используется значение по умолчанию.
"""

import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла (если есть)
load_dotenv()

# ============================================================
# НАСТРОЙКИ ПРОЕКТА
# ============================================================

# ID пользователей (можно через запятую для нескольких)
# Пример: "123456789,987654321,durov"
USER_IDS_STR = os.getenv("VK_USER_IDS")
USER_IDS = [uid.strip() for uid in USER_IDS_STR.split(",") if uid.strip()]

# Текст сообщения
MESSAGE_TEXT = os.getenv("VK_MESSAGE_TEXT", "Привет! Это автоматическое сообщение!")

# Файл для хранения cookies
COOKIES_FILE = os.getenv("VK_COOKIES_FILE", "vk_cookies.pkl")

# Режим работы браузера
# True - браузер работает в фоне (без GUI)
# False - браузер виден (удобно для отладки)
HEADLESS_MODE = os.getenv("VK_HEADLESS_MODE", "False").lower() == "true"

# Путь к папке с профилем Chrome
PROFILE_DIR = os.getenv("VK_PROFILE_DIR", os.path.join(os.getcwd(), "chrome_profile"))

# Задержка между отправками (сек)
DELAY_BETWEEN_MESSAGES = int(os.getenv("VK_DELAY_SECONDS", "3"))

# Максимальное количество попыток при ошибках
MAX_RETRIES = int(os.getenv("VK_MAX_RETRIES", "3"))

# ============================================================
# ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ (не требуют изменения)
# ============================================================

# Путь к папке с логами
LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Путь к папке с cookies файлам
if not os.path.exists(PROFILE_DIR):
    os.makedirs(PROFILE_DIR)

# ============================================================
# ИНФОРМАЦИЯ О НАСТРОЙКАХ (выводится при запуске)
# ============================================================

print("=" * 50)
print("📋 НАСТРОЙКИ ПРОЕКТА")
print("=" * 50)
print(f"👤 Получатели: {USER_IDS}")
print(f"📝 Текст сообщения: {MESSAGE_TEXT[:50]}..." if len(MESSAGE_TEXT) > 50 else f"📝 Текст сообщения: {MESSAGE_TEXT}")
print(f"🖥️  Headless режим: {HEADLESS_MODE}")
print(f"⏱️  Задержка между сообщениями: {DELAY_BETWEEN_MESSAGES} сек")
print(f"🔄 Максимум попыток: {MAX_RETRIES}")
print(f"📁 Профиль Chrome: {PROFILE_DIR}")
print(f"🍪 Файл cookies: {COOKIES_FILE}")
print("=" * 50)
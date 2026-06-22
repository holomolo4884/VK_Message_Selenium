"""
Настройка логирования для проекта.
Записывает все события в файл и выводит в консоль.
"""

import logging
import os
from datetime import datetime

# Папка для логов
LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Имя файла лога с датой
LOG_FILE = os.path.join(LOG_DIR, f"vk_auto_{datetime.now().strftime("%y-%m-%d")}.log")


def setup_logger(name="VK_Auto"):
    """
    Настраивает и возвращает логгер.
    
    Аргументы:
        name: имя логгера
    
    Возвращает:
        logging.Logger: настроенный логгер
    """

    # Создаём логер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Если у логера уже есть обработчик, не добавляем новые
    if logger.handlers:
        return logger
    
    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для файла (все уровни)
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Обработчик для консоли (только INFO и выше)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Добавляем обработчик
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Создаём глобальный логгер для всего проекта
logger = setup_logger()
"""
Вспомогательные утилиты для работы с файлами и данными.
Содержит функции для работы с cookies и очистки данных.
"""

import os
import pickle  # Для сериализации cookies в файл
from src.logger import logger


def save_cookies(driver, cookies_file):
    """
    Сохраняет cookies текущей сессии в файл.
    
    Аргументы:
        driver: экземпляр WebDriver
        cookies_file: путь к файлу для сохранения
    
    Возвращает:
        bool: True если успешно, False если ошибка
    """
    try:
        # Получаем все cookies из браузера
        cookies = driver.get_cookies()
        
        # Сохраняем в файл с помощью pickle
        with open(cookies_file, 'wb') as file:
            pickle.dump(cookies, file)
        
        logger.debug("✅ Cookies сохранены")
        return True
    except Exception as e:
        logger.error(f"❌ Не удалось сохранить cookies: {e}")
        return False


def load_cookies(driver, cookies_file):
    """
    Загружает cookies из файла в браузер.
    
    Аргументы:
        driver: экземпляр WebDriver
        cookies_file: путь к файлу с cookies
    
    Возвращает:
        bool: True если успешно, False если файла нет или ошибка
    """
    # Проверяем, существует ли файл
    if not os.path.exists(cookies_file):
        return False
    
    logger.debug("Нашёл файл с cookies, загружаю...")
    
    try:
        # Загружаем cookies из файла
        with open(cookies_file, 'rb') as file:
            cookies = pickle.load(file)
            
            # Добавляем каждый cookie в браузер
            for cookie in cookies:
                try:
                    # Удаляем параметр 'sameSite', если есть (может вызывать ошибку)
                    if 'sameSite' in cookie:
                        del cookie['sameSite']
                    
                    # Преобразуем expiry в int (требование Selenium)
                    if 'expiry' in cookie:
                        cookie['expiry'] = int(cookie['expiry'])
                    
                    driver.add_cookie(cookie)
                except Exception as e:
                    # Игнорируем ошибки отдельных cookies
                    pass
        
        logger.debug("Cookies загружены, обновляю страницу...")
        driver.refresh()  # Обновляем страницу, чтобы применить cookies
        return True
        
    except Exception as e:
        logger.error(f"❌ Ошибка при загрузке cookies: {e}")
        return False


def clear_browser_data(driver):
    """
    Очищает все данные браузера (кеш, cookies, хранилище).
    Используется при проблемах с авторизацией.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если успешно, False если ошибка
    """
    try:
        # Очищаем кеш браузера
        driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        
        # Очищаем cookies
        driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
        
        # Очищаем локальное хранилище и сессионное хранилище
        driver.execute_cdp_cmd('Storage.clearDataForOrigin', {
            'origin': 'https://vk.com',
            'storageTypes': 'all'
        })
        
        logger.debug("✅ Данные браузера очищены")
        return True
    except Exception as e:
        logger.error(f"❌ Не удалось очистить данные браузера: {e}")
        return False


def remove_cookies_file(cookies_file):
    """
    Удаляет файл с cookies.
    
    Аргументы:
        cookies_file: путь к файлу
    
    Возвращает:
        bool: True если файл удалён, False если файла нет
    """
    if os.path.exists(cookies_file):
        os.remove(cookies_file)
        logger.info("Файл cookies удалён")
        return True
    return False
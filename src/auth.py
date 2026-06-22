"""
Функции для авторизации в ВКонтакте.

Поддерживает автоматическую авторизацию через cookies и ручной вход.
Использует профиль Chrome для сохранения сессии между запусками.
"""

from selenium.webdriver.common.by import By
from src.utils import load_cookies, save_cookies, clear_browser_data, remove_cookies_file
from src.config import COOKIES_FILE
from src.logger import logger
import time


def check_auth(driver):
    """
    Проверяет, авторизован ли пользователь в ВКонтакте.
    
    Принцип: ищет элемент "Моя страница" (ID: l_pr), который есть
    только у авторизованных пользователей.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если авторизован, False если нет
    
    Пример:
        >>> if check_auth(driver):
        ...     print("Пользователь авторизован")
        ... else:
        ...     print("Требуется авторизация")
    """
    try:
        driver.find_element(By.ID, "l_pr")
        logger.debug("✅ Пользователь авторизован")
        return True
    except:
        logger.debug("❌ Пользователь не авторизован")
        return False


def manual_auth(driver):
    """
    Запрашивает ручную авторизацию у пользователя.
    
    Используется когда cookies не сработали или их нет.
    Пользователь входит вручную в открывшемся браузере.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если авторизация успешна, False если нет
    """
    
    logger.warning("🔐 Требуется ручная авторизация")
    
    print("\n" + "=" * 50)
    print("🔐 ТРЕБУЕТСЯ АВТОРИЗАЦИЯ")
    print("=" * 50)
    print("ВНИМАНИЕ! Возможна ошибка 'ERR_TOO_MANY_REDIRECTS'")
    print("Если увидите эту ошибку:")
    print("1. Вручную перейдите на https://vk.com/ в этом же окне браузера")
    print("2. Авторизуйтесь (через QR-код или логин/пароль)")
    print("3. Вернитесь в консоль и нажмите Enter")
    print("=" * 50)
    print("Либо если вы уже авторизованы, просто нажмите Enter")
    print("=" * 50)
    
    # Ждём нажатия Enter от пользователя
    input()
    
    # Проверяем, авторизовались ли
    if check_auth(driver):
        logger.info("✅ Авторизация успешна!")
        return True
    else:
        # Пробуем перейти на главную страницу (иногда помогает)
        logger.info("Пробую перейти на главную страницу...")
        driver.get("https://vk.com/")
        time.sleep(2)
        
        if check_auth(driver):
            logger.info("✅ Авторизация успешна!")
            return True
        else:
            logger.error("❌ Авторизация не удалась")
            return False


def handle_auth(driver):
    """
    Полный процесс авторизации.
    
    Сначала пытается использовать cookies, при неудаче - ручной вход.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если авторизация успешна, False если нет
    
    Алгоритм:
        1. Пытается загрузить cookies из файла
        2. Если cookies есть и работают - авторизация успешна
        3. Если cookies не работают - очищает данные и удаляет файл
        4. Запрашивает ручную авторизацию
        5. Сохраняет новые cookies для будущих сессий
    """
    
    logger.info("🔄 Начинаю процесс авторизации...")
    
    # ============================================================
    # ШАГ 1: ПЫТАЕМСЯ ЗАГРУЗИТЬ COOKIES
    # ============================================================
    
    cookies_loaded = load_cookies(driver, COOKIES_FILE)
    
    if cookies_loaded:
        # Ждём применения cookies
        time.sleep(3)
        
        # Проверяем, сработали ли cookies
        if check_auth(driver):
            logger.info("✅ Успешно залогинились через cookies!")
            return True
        else:
            logger.warning("⚠️ Cookies не сработали или вызвали ошибку")
            
            # ============================================================
            # ШАГ 2: ОЧИЩАЕМ ПРОБЛЕМНЫЕ ДАННЫЕ
            # ============================================================
            
            clear_browser_data(driver)
            driver.delete_all_cookies()
            remove_cookies_file(COOKIES_FILE)
            
            # Перезагружаем страницу
            driver.get("https://vk.com/")
            time.sleep(2)
    
    # ============================================================
    # ШАГ 3: РУЧНАЯ АВТОРИЗАЦИЯ
    # ============================================================
    
    logger.info("Переходим к ручной авторизации...")
    
    if not manual_auth(driver):
        logger.error("❌ Ручная авторизация не удалась")
        return False
    
    # ============================================================
    # ШАГ 4: СОХРАНЯЕМ НОВЫЕ COOKIES
    # ============================================================
    
    save_cookies(driver, COOKIES_FILE)
    logger.info("✅ Cookies сохранены для будущих сессий!")
    
    return True
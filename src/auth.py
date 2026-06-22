"""
Функции для авторизации в ВКонтакте.
Поддерживает автоматическую авторизацию через cookies и ручной вход.
"""

from selenium.webdriver.common.by import By
from src.utils import load_cookies, save_cookies, clear_browser_data, remove_cookies_file
from src.config import COOKIES_FILE
import time

def check_auth(driver):
    """
    Проверяет, авторизован ли пользователь в ВКонтакте.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если авторизован, False если нет
    
    Принцип:
        Ищет элемент "Моя страница" (ID: l_pr), который есть только
        у авторизованных пользователей.
    """
    try:
        driver.find_element(By.ID, "l_pr")
        return True
    except:
        return False


def manual_auth(driver):
    """
    Запрашивает ручную авторизацию у пользователя.
    Используется когда cookies не сработали или их нет.
    
    Аргументы:
        driver: экземпляр WebDriver
    
    Возвращает:
        bool: True если авторизация успешна, False если нет
    """
    
    print("\n" + "="*50)
    print("🔐 ТРЕБУЕТСЯ АВТОРИЗАЦИЯ")
    print("="*50)
    print("ВНИМАНИЕ! Возможна ошибка 'ERR_TOO_MANY_REDIRECTS'")
    print("Если увидите эту ошибку:")
    print("1. Вручную перейдите на https://vk.com/ в этом же окне браузера")
    print("2. Авторизуйтесь (через QR-код или логин/пароль)")
    print("3. Вернитесь в консоль и нажмите Enter")
    print("="*50)
    print("Либо если вы уже авторизованы, просто нажмите Enter")
    print("="*50)
    
    # Ждём нажатия Enter от пользователя
    input()
    
    # Проверяем, авторизовались ли
    if check_auth(driver):
        print("✅ Авторизация успешна!")
        return True
    else:
        # Пробуем перейти на главную страницу (иногда помогает)
        print("Пробую перейти на главную страницу...")
        driver.get("https://vk.com/")
        time.sleep(2)
        
        if check_auth(driver):
            print("✅ Авторизация успешна!")
            return True
        else:
            print("❌ Авторизация не удалась")
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
    
    # Пытаемся загрузить cookies из файла
    cookies_loaded = load_cookies(driver, COOKIES_FILE)
    
    if cookies_loaded:
        # Ждём применения cookies
        time.sleep(3)
        
        # Проверяем, сработали ли cookies
        if check_auth(driver):
            print("✅ Успешно залогинились через cookies!")
            return True
        else:
            print("⚠️ Cookies не сработали или вызвали ошибку.")
            
            # Очищаем все данные
            clear_browser_data(driver)
            driver.delete_all_cookies()
            remove_cookies_file(COOKIES_FILE)
            
            # Перезагружаем страницу
            driver.get("https://vk.com/")
            time.sleep(2)
    
    # Если cookies не сработали, просим войти вручную
    if not manual_auth(driver):
        return False
    
    # Сохраняем новые cookies для будущих сессий
    save_cookies(driver, COOKIES_FILE)
    print("✅ Cookies сохранены! В следующий раз войдёте автоматически.")
    
    return True
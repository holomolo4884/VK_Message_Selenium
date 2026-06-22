"""
Настройка и запуск браузера Chrome.
Содержит конфигурацию для маскировки автоматизации.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.config import PROFILE_DIR, HEADLESS_MODE
import os


def setup_driver():
    """
    Настраивает и запускает драйвер Chrome с маскировкой.
    
    Возвращает:
        WebDriver: настроенный экземпляр драйвера
    
    Особенности:
        - Создаёт отдельный профиль Chrome для сохранения сессии
        - Маскирует признаки автоматизации (чтобы сайты не блокировали)
        - Отключает уведомления и всплывающие окна
    """
    
    # Создаём папку для профиля, если её нет
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
    
    # Настройки для маскировки под реального пользователя
    options = Options()
    
    # Скрываем признаки автоматизации
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Отключаем лишние уведомления
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Отключаем GPU для стабильности
    options.add_argument("--disable-gpu")
    
    # Используем профиль пользователя для сохранения сессии
    # Благодаря этому не нужно входить каждый раз
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    
    # Если включён headless-режим, браузер работает в фоне
    if HEADLESS_MODE:
        options.add_argument("--headless")
    
    # Запускаем браузер
    driver = webdriver.Chrome(options=options)
    
    
    # МАСКИРОВКА WEBDRIVER (обход антибот-систем)

    # Первая маскировка: удаляем свойство webdriver
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    # Вторая маскировка: дополнительные скрытые свойства
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            // Удаляем navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            
            // Добавляем chrome (обычно есть у реальных пользователей)
            window.chrome = { runtime: {} };
            
            // Маскируем разрешения (permissions)
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        '''
    })
    
    return driver
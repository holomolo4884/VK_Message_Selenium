"""
Настройка и запуск браузера Chrome.

Содержит конфигурацию для маскировки автоматизации,
чтобы сайты не могли определить, что используется Selenium.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.config import PROFILE_DIR, HEADLESS_MODE
from src.logger import logger
import os


def setup_driver():
    """
    Настраивает и запускает драйвер Chrome с маскировкой.
    
    Особенности:
        - Создаёт отдельный профиль Chrome для сохранения сессии
        - Маскирует признаки автоматизации
        - Отключает уведомления и всплывающие окна
        - Поддерживает headless-режим
    
    Возвращает:
        WebDriver: настроенный экземпляр драйвера
    """
    
    # Создаём папку для профиля, если её нет
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR)
        logger.debug(f"📁 Создана папка профиля: {PROFILE_DIR}")
    
    # Настройки для маскировки под реального пользователя
    options = Options()
    
    # ============================================================
    # МАСКИРОВКА ПРИЗНАКОВ АВТОМАТИЗАЦИИ
    # ============================================================
    
    # Скрываем флаг автоматизации
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Отключаем автоматизацию в настройках
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # ============================================================
    # НАСТРОЙКИ ДЛЯ УДОБСТВА
    # ============================================================
    
    # Отключаем лишние уведомления
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    
    # Отключаем GPU для стабильности
    options.add_argument("--disable-gpu")
    
    # Добавляем аргументы для решения проблемы DevToolsActivePort
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")

    # ============================================================
    # ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
    # ============================================================
    
    # Используем профиль пользователя для сохранения сессии
    # Благодаря этому не нужно входить каждый раз
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    
    # ============================================================
    # HEADLESS РЕЖИМ
    # ============================================================
    
    # Если включён headless-режим, браузер работает в фоне
    if HEADLESS_MODE:
        options.add_argument("--headless")
        logger.debug("🖥️  Запуск в headless-режиме (браузер не виден)")
    
    # ============================================================
    # ЗАПУСК БРАУЗЕРА
    # ============================================================
    
    # Запускаем браузер с настройками
    driver = webdriver.Chrome(options=options)
    
    # ============================================================
    # МАСКИРОВКА WEBDRIVER (обход антибот-систем)
    # ============================================================
    
    # Первая маскировка: удаляем свойство webdriver у navigator
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
            
            // Добавляем объект chrome (обычно есть у реальных пользователей)
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
    
    logger.debug("✅ Браузер запущен и настроен")
    return driver
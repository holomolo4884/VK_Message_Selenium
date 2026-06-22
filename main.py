"""
Главный файл для запуска скрипта автоматизации VK.
Содержит основную логику программы.
"""

from selenium.webdriver.support.ui import WebDriverWait
import time

# Импортируем всё из пакета src
from src import (
    USER_IDS,                    # Получатели
    MESSAGE_TEXT,                # Текст сообщения
    COOKIES_FILE,                # Файл для cookies
    DELAY_BETWEEN_MESSAGES,      # Задержка
    setup_driver,                # Запуск браузера
    check_auth,                  # Проверка авторизации
    handle_auth,                 # Авторизация
    send_messages_to_multiple,   # Отправка сообщений
    save_cookies,                # Сохранение cookies
    logger                       # Логирование
)


def main():
    """
    Главная функция программы.
    
    Шаги выполнения:
        1. Настройка и запуск драйвера Chrome
        2. Открытие ВКонтакте
        3. Авторизация (cookies или ручной вход)
        4. Проверка авторизации
        5. Переход в диалог
        6. Поиск поля ввода и отправка сообщения
        7. Сохранение cookies и закрытие браузера
    
    Возвращает:
        bool: True если всё успешно, False если ошибка
    """
    
    driver = None  # Инициализируем драйвер для использования в finally
    
    try:
        logger.info("=" * 50)
        logger.info("🚀 ЗАПУСК СКРИПТА")
        logger.info("=" * 50)
        logger.info(f"Получатели: {USER_IDS}")
        logger.info(f"Текст: {MESSAGE_TEXT[:50]}...")
        
        # 1. Запускаем браузер
        driver = setup_driver()
        driver.get("https://vk.com/")
        wait = WebDriverWait(driver, 15)
        time.sleep(DELAY_BETWEEN_MESSAGES)
        
        # 2. Авторизация
        if not handle_auth(driver):
            logger.error("❌ Авторизация не удалась")
            return False
        
        if not check_auth(driver):
            logger.error("❌ Пользователь не авторизован")
            return False
        
        logger.info("✅ Авторизация успешна")
        
        # 3. Отправка сообщений
        results = send_messages_to_multiple(driver, USER_IDS, MESSAGE_TEXT, wait)

        # 4. Статистика
        success_count = sum(1 for v in results.values() if v)
        logger.info("=" * 50)
        logger.info(f"✅ Успешно: {success_count}/{len(USER_IDS)}")
        logger.info("=" * 50)
        
        return True
        
    except Exception as e:
        # Обработка непредвиденных ошибок
        logger.error(f"❌ Произошла ошибка: {e}")
        return False
    
    finally:
        if driver:
            # Сохраняем актуальные cookies перед закрытием
            save_cookies(driver, COOKIES_FILE)
            
            # Закрываем браузер
            driver.quit()
            logger.info("Браузер закрыт")


# ТОЧКА ВХОДА В ПРОГРАММУ
if __name__ == "__main__":
    """
    Конструкция if __name__ == "__main__" гарантирует,
    что функция main() запустится только при прямом запуске файла,
    а не при импорте как модуля.
    """
    main()
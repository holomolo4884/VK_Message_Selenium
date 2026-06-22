"""
Главный файл для запуска скрипта автоматизации VK.
Содержит основную логику программы.
"""

from selenium.webdriver.support.ui import WebDriverWait
import time

# Импортируем всё из пакета src
from src import (
    USER_ID,
    MESSAGE_TEXT,
    COOKIES_FILE,
    setup_driver,
    check_auth,
    handle_auth,
    find_message_input,
    send_message_safely,
    go_to_dialog,
    save_cookies,
    clear_browser_data,
    remove_cookies_file
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
        # ШАГ 1: НАСТРОЙКА И ЗАПУСК БРАУЗЕРА
        driver = setup_driver()
        print("Открыл ВК")
        
        # ШАГ 2: ОТКРЫТИЕ ВКОНТАКТЕ
        driver.get("https://vk.com/")
        wait = WebDriverWait(driver, 15)  # Таймаут ожидания 15 секунд
        time.sleep(3)  # Даём время на загрузку
        
        # ШАГ 3: АВТОРИЗАЦИЯ
        if not handle_auth(driver):
            print("❌ Авторизация не удалась. Завершаю работу.")
            return False
        
        # ШАГ 4: ПРОВЕРКА АВТОРИЗАЦИИ
        if not check_auth(driver):
            print("⚠️ Вы не авторизованы! Попробуйте перезапустить скрипт.")
            print("Если ошибка повторяется, удалите папку chrome_profile и файл cookies")
            input("Нажмите Enter для выхода...")
            return False
        
        # ШАГ 5: ПЕРЕХОД В ДИАЛОГ
        if not go_to_dialog(driver, USER_ID):
            # Если не удалось перейти в диалог, очищаем данные
            clear_browser_data(driver)
            driver.delete_all_cookies()
            remove_cookies_file(COOKIES_FILE)
            print("Удалите папку chrome_profile и перезапустите скрипт")
            return False
        
        # ШАГ 6: ОТПРАВКА СООБЩЕНИЯ
        print("\nИщу поле ввода сообщения...")
        message_input = find_message_input(driver, wait)
        
        if message_input:
            # Поле найдено - отправляем сообщение
            success = send_message_safely(driver, message_input, MESSAGE_TEXT)
            if success:
                print("\n✅ Сообщение успешно отправлено!")
            else:
                print("\n❌ Не удалось отправить сообщение")
        else:
            # Поле не найдено
            print("❌ Не удалось найти поле ввода")
            print("💡 Подсказка: обновите селекторы поля ввода")
        
        # ШАГ 7: ОЖИДАНИЕ РЕЗУЛЬТАТА
        print("\nОжидание 5 секунд...")
        time.sleep(5)  # Даём время увидеть результат в браузере
        
        return True
        
    except Exception as e:
        # Обработка непредвиденных ошибок
        print(f"❌ Произошла ошибка: {e}")
        return False
    
    finally:
        # ШАГ 8: ЗАВЕРШЕНИЕ РАБОТЫ
        if driver:
            # Сохраняем актуальные cookies перед закрытием
            save_cookies(driver, COOKIES_FILE)
            
            # Закрываем браузер
            driver.quit()
            print("\nБраузер закрыт")


# ТОЧКА ВХОДА В ПРОГРАММУ
if __name__ == "__main__":
    """
    Конструкция if __name__ == "__main__" гарантирует,
    что функция main() запустится только при прямом запуске файла,
    а не при импорте как модуля.
    """
    main()
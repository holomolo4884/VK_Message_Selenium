"""
Функции для работы с сообщениями ВКонтакте.
Поиск поля ввода и отправка сообщений.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time


def find_message_input(driver, wait):
    """
    Находит поле ввода сообщения в диалоге.
    Использует несколько селекторов для разных версий интерфейса.
    
    Аргументы:
        driver: экземпляр WebDriver
        wait: объект WebDriverWait для ожидания элементов
    
    Возвращает:
        WebElement: найденное поле ввода, или None если не найдено
    """
    
    # Список возможных селекторов (от точных к общим)
    selectors = [
        "span.ComposerInput__input.ConvoComposer__input.ComposerInput__input--fixed[contenteditable='true']",
        "span.ComposerInput__input[contenteditable='true']",
        "[contenteditable='true']"
    ]
    
    # Пробуем каждый селектор по очереди
    for selector in selectors:
        try:
            # Ждём появления элемента
            message_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            print(f"✅ Нашёл поле ввода через: {selector}")
            return message_input
        except:
            continue
    
    # Если ничего не нашли, пробуем найти любой editable элемент
    try:
        message_input = driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
        print("✅ Нашёл через contenteditable")
        return message_input
    except:
        return None


def send_message_safely(driver, message_input, text):
    """
    Безопасно отправляет сообщение.
    Вводит текст посимвольно, пропуская неподдерживаемые символы.
    
    Аргументы:
        driver: экземпляр WebDriver
        message_input: найденное поле ввода
        text: текст для отправки
    
    Возвращает:
        bool: True если успешно, False если ошибка
    
    Особенности:
        - Вводит текст посимвольно для обхода проблем с юникодом
        - Пробует разные способы отправки (кнопка или Enter)
    """
    try:
        # Кликаем в поле ввода (активируем его)
        message_input.click()
        time.sleep(0.3)
        
        # Если это обычное поле input или textarea - очищаем его
        if message_input.tag_name in ["input", "textarea"]:
            message_input.clear()
        
        # Вводим текст посимвольно (обход ошибок с символами)
        print("Ввожу текст посимвольно...")
        for char in text:
            try:
                message_input.send_keys(char)
                time.sleep(0.02)  # Небольшая задержка между символами
            except Exception as e:
                # Если символ не поддерживается - пропускаем его
                print(f"⚠️ Пропущен неподдерживаемый символ: {char}")
                continue
        
        print(f"✅ Ввёл текст: {text}")
        time.sleep(0.5)
        

        # ОТПРАВКА СООБЩЕНИЯ        
        # Способ 1: Пробуем найти кнопку "Отправить"
        try:
            send_button = driver.find_element(By.CSS_SELECTOR, 
                "button[aria-label='Отправить'], button.ComposerSendButton__button")
            send_button.click()
            print("✅ Отправил через кнопку")
        except:
            # Способ 2: Если кнопки нет, используем клавишу Enter
            message_input.send_keys(Keys.RETURN)
            print("✅ Отправил через Enter")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при отправке: {e}")
        return False


def go_to_dialog(driver, user_id):
    """
    Переходит в диалог с указанным пользователем или группой.
    
    Аргументы:
        driver: экземпляр WebDriver
        user_id: ID пользователя или группы
    
    Возвращает:
        bool: True если успешно, False если перекинуло на страницу входа
    """
    
    print(f"\nПерехожу в диалог с ID {user_id}...")
    
    # Формируем URL для перехода в диалог
    driver.get(f"https://vk.com/im?sel={user_id}")
    time.sleep(3)  # Даём время загрузиться диалогу
    
    # Проверяем, не перекинуло ли на страницу входа
    if "login" in driver.current_url or "auth" in driver.current_url:
        print("⚠️ Похоже, сессия истекла. Нужно авторизоваться заново.")
        return False
    
    return True
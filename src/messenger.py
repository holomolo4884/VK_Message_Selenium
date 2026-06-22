"""
Модуль для работы с сообщениями ВКонтакте.

Этот модуль содержит функции для:
- Поиска поля ввода сообщения
- Отправки сообщений отдельным пользователям
- Отправки сообщений нескольким пользователям
- Перехода в диалоги
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

from src.logger import logger
from src.retry import retry
from src.config import DELAY_BETWEEN_MESSAGES


def find_message_input(driver, wait):
    """
    Находит поле ввода сообщения в диалоге ВКонтакте.
    
    Функция пробует несколько селекторов, потому что интерфейс ВК
    может отличаться в разных версиях или для разных пользователей.
    
    Аргументы:
        driver: экземпляр WebDriver
        wait: объект WebDriverWait для ожидания элементов
    
    Возвращает:
        WebElement: найденное поле ввода, или None если не найдено
    """
    
    # Список селекторов от самых точных к самым общим
    selectors = [
        # Основной селектор для нового интерфейса ВК
        "span.ComposerInput__input.ConvoComposer__input.ComposerInput__input--fixed[contenteditable='true']",
        # Запасной селектор
        "span.ComposerInput__input[contenteditable='true']",
        # Самый общий селектор
        "[contenteditable='true']"
    ]
    
    # Пробуем каждый селектор по очереди
    for selector in selectors:
        try:
            message_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            logger.debug(f"✅ Нашёл поле ввода через: {selector}")
            return message_input
        except:
            continue
    
    # Если все селекторы не сработали, пробуем последний способ
    try:
        message_input = driver.find_element(By.CSS_SELECTOR, "[contenteditable='true']")
        logger.debug("✅ Нашёл поле ввода через contenteditable")
        return message_input
    except:
        logger.error("❌ Не удалось найти поле ввода")
        return None


@retry(max_attempts=3, delay=2)
def send_message_to_user(driver, user_id, text, wait):
    """
    Отправляет сообщение одному пользователю ВКонтакте.
    
    Аргументы:
        driver: экземпляр WebDriver
        user_id: ID получателя
        text: текст сообщения
        wait: WebDriverWait
    
    Возвращает:
        bool: True если успешно, False если ошибка
    """
    
    logger.info(f"📨 Отправка сообщения пользователю {user_id}")
    
    # Переходим в диалог
    driver.get(f"https://vk.com/im?sel={user_id}")
    time.sleep(2)
    
    # Находим поле ввода
    message_input = find_message_input(driver, wait)
    if not message_input:
        logger.error(f"❌ Не найден input для {user_id}")
        return False
    
    # Вводим текст
    message_input.click()
    time.sleep(0.3)
    
    # Вводим текст посимвольно
    for char in text:
        try:
            message_input.send_keys(char)
            time.sleep(0.02)
        except:
            continue
    
    logger.debug(f"Ввёл текст: {text[:50]}..." if len(text) > 50 else f"Ввёл текст: {text}")
    time.sleep(0.5)
    
    # Отправляем
    try:
        send_button = driver.find_element(By.CSS_SELECTOR, 
            "button[aria-label='Отправить'], button.ComposerSendButton__button")
        send_button.click()
        logger.info(f"✅ Отправил {user_id} через кнопку")
    except:
        message_input.send_keys(Keys.RETURN)
        logger.info(f"✅ Отправил {user_id} через Enter")
    
    return True


def send_messages_to_multiple(driver, user_ids, text, wait):
    """
    Отправляет сообщения нескольким пользователям.
    
    Аргументы:
        driver: экземпляр WebDriver
        user_ids: список ID получателей
        text: текст сообщения
        wait: WebDriverWait
    
    Возвращает:
        dict: статистика отправки {user_id: success}
    """
    
    results = {}
    total = len(user_ids)
    
    logger.info(f"📨 Начинаю отправку {total} сообщениям...")
    
    for idx, user_id in enumerate(user_ids, 1):
        logger.info(f"[{idx}/{total}] Обработка {user_id}...")
        
        try:
            success = send_message_to_user(driver, user_id, text, wait)
            results[user_id] = success
            
            if success:
                logger.info(f"✅ [{idx}/{total}] Отправлено {user_id}")
            else:
                logger.error(f"❌ [{idx}/{total}] Не удалось отправить {user_id}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке {user_id}: {e}")
            results[user_id] = False
        
        # Задержка между отправками
        if idx < total:
            logger.debug(f"Ожидание {DELAY_BETWEEN_MESSAGES} сек...")
            time.sleep(DELAY_BETWEEN_MESSAGES)
    
    # Статистика
    success_count = sum(1 for v in results.values() if v)
    failed_count = total - success_count
    
    logger.info("=" * 50)
    logger.info("📊 СТАТИСТИКА ОТПРАВКИ")
    logger.info("=" * 50)
    logger.info(f"✅ Успешно: {success_count}/{total}")
    logger.info(f"❌ Ошибок: {failed_count}/{total}")
    
    if failed_count > 0:
        failed_users = [uid for uid, success in results.items() if not success]
        logger.warning(f"Не удалось отправить: {failed_users}")
    
    return results


def go_to_dialog(driver, user_id):
    """
    Переходит в диалог с указанным пользователем или группой.
    
    Аргументы:
        driver: экземпляр WebDriver
        user_id: ID пользователя или группы
    
    Возвращает:
        bool: True если успешно, False если перекинуло на страницу входа
    """
    
    logger.info(f"🔄 Перехожу в диалог с {user_id}")
    
    driver.get(f"https://vk.com/im?sel={user_id}")
    time.sleep(3)
    
    if "login" in driver.current_url or "auth" in driver.current_url:
        logger.warning("⚠️ Сессия истекла")
        return False
    
    logger.info(f"✅ Перешёл в диалог с {user_id}")
    return True
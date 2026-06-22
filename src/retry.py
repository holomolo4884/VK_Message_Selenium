"""
Декоратор для повторных попыток выполнения функций.
Полезно при нестабильном соединении или временных ошибках.
"""

import time
from functools import wraps
from src.logger import logger


def retry(max_attempts=3, delay=2, backoff=2, exceptions=(Exception,)):
    """
    Декоратор для повторных попыток выполнения функции.
    
    Аргументы:
        max_attempts: максимальное количество попыток
        delay: задержка между попытками (сек)
        backoff: множитель увеличения задержки
        exceptions: кортеж исключений, при которых нужно повторять
    
    Пример:
        @retry(max_attempts=5, delay=1)
        def unstable_function():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.debug(f"Попытка {attempt}/{max_attempts} для {func.__name__}")
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"✅ Функция {func.__name__} выполнилась с {attempt} попытки")
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    logger.warning(f"⚠️ Попытка {attempt}/{max_attempts} не удалась: {e}")
                    
                    if attempt == max_attempts:
                        logger.error(f"❌ Функция {func.__name__} не выполнилась после {max_attempts} попыток")
                        raise last_exception
                    
                    logger.debug(f"Ожидание {current_delay} сек перед следующей попыткой...")
                    time.sleep(current_delay)
                    current_delay *= backoff  # Увеличиваем задержку
            
            return None
        return wrapper
    return decorator
import logging

import aiosqlite

file_path = r"C:\Users\Алексей\PycharmProjects\Bot\bot\test.db"

logger = logging.getLogger("HabitBot")


async def get_connection():
    """Создаем соединение с настройками для избежания блокировок"""
    conn = await aiosqlite.connect(
        file_path,
        timeout=30,  # Увеличиваем время ожидания
        isolation_level=None  # Автоматическое управление транзакциями
    )
    await conn.execute("PRAGMA journal_mode=WAL")  # Включаем WAL-режим
    await conn.execute("PRAGMA busy_timeout=30000")  # 30 секунд ожидания
    return conn


async def add_user(telegram_id: int, name: str):
    """Добавление пользователя с обработкой ошибок"""
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                                 INSERT INTO users (telegram_id, name)
                                 VALUES (?, ?)
                                 ''', (telegram_id, name))
            await conn.commit()
    except Exception as e:
        await conn.rollback()
        logger.error(f"Error adding user: {e}")
        raise
    finally:
        await conn.close()


async def add_habit(telegram_id: int, name: str, times_per_day: int):
    """Добавление привычки с транзакцией"""
    name = name.capitalize()
    conn = await get_connection()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                                 INSERT INTO habits (telegram_id, name, times_per_day)
                                 VALUES (?, ?, ?)
                                 ''', (telegram_id, name, times_per_day)
                                 )
            await conn.commit()
            logger.debug(f"Habit added for {telegram_id}")
    except Exception as e:
        await conn.rollback()
        logger.error(f"Error adding habit: {e}")
        raise
    finally:
        await conn.close()


async def get_habits(telegram_id: int):
    """Получение списка привычек"""
    conn = await get_connection()
    logger.info("Getting habits...")
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                                 SELECT *
                                 FROM habits
                                 WHERE telegram_id = ?
                                 ''', (telegram_id,))
            logger.info("Got habits...")
            # Возвращает в формате [(ID, name, amount),]
            return await cursor.fetchall()
    except Exception as e:
        logger.error(f"Error getting habits: {e}")
        return []
    finally:
        await conn.close()


async def get_habit(telegram_id: int, habit: str):
    """Получение конкретной привычки"""
    conn = await get_connection()
    habit = habit.capitalize()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                                 SELECT *
                                 FROM habits
                                 WHERE telegram_id = ?
                                   AND name = ?
                                 ''', (telegram_id, habit))
            return await cursor.fetchone()
    except Exception as e:
        logger.error(f"Error getting habit: {e}")
        return None
    finally:
        await conn.close()


async def delete_habit(telegram_id: int, habit: str):
    """Удаление привычки с обработкой ошибок"""
    habit = habit.capitalize()
    conn = await get_connection()
    try:
        logger.info(f"Starting delete for {telegram_id}:{habit}")
        async with conn.cursor() as cursor:
            await cursor.execute('''
                                 DELETE
                                 FROM habits
                                 WHERE telegram_id = ?
                                   AND name = ?
                                 ''', (telegram_id, habit))
            await conn.commit()
            logger.info(f"Successfully deleted {habit} for {telegram_id}")
            return True
    except Exception as e:
        await conn.rollback()
        logger.error(f"Error deleting habit: {e}")
        return False
    finally:
        await conn.close()

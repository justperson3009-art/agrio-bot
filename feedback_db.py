"""
База данных обратной связи (SQLite)
Хранит: полезные ответы, жалобы, статистику запросов
"""

import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "feedback.db")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Инициализация таблиц"""
    conn = _get_conn()
    c = conn.cursor()

    # Отзывы: полезно/не полезно
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message_text TEXT,
            is_positive INTEGER,  -- 1 = полезно, 0 = не полезно
            comment TEXT,         -- комментарий при "не полезно"
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Статистика запросов (для подсчёта по неделям)
    c.execute("""
        CREATE TABLE IF NOT EXISTS request_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Подписки на рассылку
    c.execute("""
        CREATE TABLE IF NOT EXISTS tip_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def add_feedback(user_id: int, message_text: str, is_positive: bool, comment: str = None):
    """Добавить отзыв"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO feedback (user_id, message_text, is_positive, comment) VALUES (?, ?, ?, ?)",
        (user_id, message_text[:500], 1 if is_positive else 0, comment)
    )
    conn.commit()
    conn.close()


def log_request(user_id: int):
    """Записать запрос в статистику"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO request_stats (user_id) VALUES (?)",
        (user_id,)
    )
    conn.commit()
    conn.close()


def add_subscriber(user_id: int):
    """Добавить подписчика на рассылку"""
    conn = _get_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO tip_subscribers (user_id) VALUES (?)", (user_id,))
        conn.commit()
    except:
        pass
    conn.close()


def remove_subscriber(user_id: int):
    """Удалить подписчика"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM tip_subscribers WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def get_stats() -> dict:
    """Получить полную статистику"""
    conn = _get_conn()
    c = conn.cursor()

    # Уникальные пользователи
    c.execute("SELECT COUNT(DISTINCT user_id) FROM request_stats")
    total_users = c.fetchone()[0]

    # Всего запросов
    c.execute("SELECT COUNT(*) FROM request_stats")
    total_requests = c.fetchone()[0]

    # Запросов за неделю
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute("SELECT COUNT(*) FROM request_stats WHERE created_at >= ?", (week_ago,))
    weekly_requests = c.fetchone()[0]

    # Полезных ответов
    c.execute("SELECT COUNT(*) FROM feedback WHERE is_positive = 1")
    positive_feedback = c.fetchone()[0]

    # Не полезных ответов
    c.execute("SELECT COUNT(*) FROM feedback WHERE is_positive = 0")
    negative_feedback = c.fetchone()[0]

    # Подписчиков
    c.execute("SELECT COUNT(*) FROM tip_subscribers")
    subscribers = c.fetchone()[0]

    # Жалобы с комментариями
    c.execute("SELECT COUNT(*) FROM feedback WHERE is_positive = 0 AND comment IS NOT NULL AND comment != ''")
    complaints_count = c.fetchone()[0]

    conn.close()

    return {
        "total_users": total_users,
        "total_requests": total_requests,
        "weekly_requests": weekly_requests,
        "positive_feedback": positive_feedback,
        "negative_feedback": negative_feedback,
        "subscribers": subscribers,
        "complaints_count": complaints_count,
    }


def get_complaints(limit: int = 20) -> list:
    """Получить последние жалобы с комментариями"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id, user_id, message_text, comment, created_at FROM feedback "
        "WHERE is_positive = 0 AND comment IS NOT NULL AND comment != '' "
        "ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()

    complaints = []
    for row in rows:
        complaints.append({
            "id": row["id"],
            "user_id": row["user_id"],
            "message_text": row["message_text"],
            "comment": row["comment"],
            "created_at": row["created_at"],
        })
    return complaints


def delete_complaint(complaint_id: int):
    """Удалить жалобу после обработки"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id = ?", (complaint_id,))
    conn.commit()
    conn.close()


def get_subscribers_list() -> list:
    """Список всех подписчиков"""
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT user_id, subscribed_at FROM tip_subscribers ORDER BY subscribed_at")
    rows = c.fetchall()
    conn.close()
    return [{"user_id": r["user_id"], "subscribed_at": r["subscribed_at"]} for r in rows]


# Инициализация при импорте
init_db()

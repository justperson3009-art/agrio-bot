"""
Обработчик обратной связи — кнопки 👍 Полезно / 👎 Не полезно
"""

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from feedback_db import add_feedback

router = Router(name="feedback")
logger = logging.getLogger(__name__)


@router.callback_query(F.data == "subscribe:yes")
async def handle_subscribe_yes(callback: CallbackQuery):
    """Пользователь нажал 'Подписаться'"""
    from feedback_db import add_subscriber
    user_id = callback.from_user.id
    add_subscriber(user_id)

    await callback.answer("✅ Вы подписались!", show_alert=False)
    await callback.message.edit_text(
        "✅ **Вы подписались на еженедельные советы!**\n\n"
        "Каждый понедельник в 9:00 — актуальный совет.\n"
        "Отписаться: /unsubscribe"
    )


@router.callback_query(F.data == "subscribe:no")
async def handle_subscribe_no(callback: CallbackQuery):
    """Пользователь нажал 'Не сейчас'"""
    await callback.answer("Хорошо, может быть позже!", show_alert=False)
    await callback.message.edit_text(
        "👍 Хорошо! Если передумаете — напишите /subscribe"
    )


# FSM для запроса комментария при "Не полезно"
class FeedbackState(StatesGroup):
    waiting_for_comment = State()


@router.callback_query(F.data.startswith("feedback:"))
async def handle_feedback(callback: CallbackQuery, state: FSMContext):
    """Обработка нажатия Полезно/Не полезно"""
    action = callback.data.split(":")[1]  # positive или negative
    user_id = callback.from_user.id

    # Получаем исходное сообщение (текст запроса)
    try:
        original_text = callback.message.reply_to_message.text if callback.message.reply_to_message else ""
    except:
        original_text = ""

    if action == "positive":
        # Полезно — просто отмечаем
        add_feedback(user_id, original_text, is_positive=True)
        logger.info(f"Полезно: user_id={user_id}")

        await callback.answer("✅ Спасибо за оценку!", show_alert=False)

        # Убираем кнопки после нажатия
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            pass

    elif action == "negative":
        # Не полезно — просим комментарий
        await state.set_data({"original_text": original_text, "bot_message_id": callback.message.message_id})
        await state.set_state(FeedbackState.waiting_for_comment)

        await callback.message.edit_text(
            callback.message.text + "\n\n"
            "❓ **Что можно улучшить?**\n"
            "Напишите комментарий — это поможет сделать бота лучше!",
            reply_markup=None
        )
        await callback.answer("Напишите что было не так", show_alert=False)


@router.message(FeedbackState.waiting_for_comment)
async def handle_feedback_comment(message: Message, state: FSMContext):
    """Получение комментария при 'Не полезно'"""
    data = await state.get_data()
    original_text = data.get("original_text", "")

    comment = message.text.strip()[:500]
    if not comment:
        await message.answer("✍️ Напишите что именно было не так:")
        return

    user_id = message.from_user.id

    add_feedback(user_id, original_text, is_positive=False, comment=comment)
    logger.info(f"Не полезно + комментарий: user_id={user_id}, comment='{comment[:50]}'")

    await state.clear()
    await message.answer(
        "✅ **Ваша жалоба принята!**\n\n"
        "Спасибо за обратную связь — мы учтём ваши пожелания для улучшения бота."
    )

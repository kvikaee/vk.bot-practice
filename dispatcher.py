from state import user_states
from handlers import (
    handle_start, handle_about, handle_why_not_state, handle_why_next,
    handle_select_problem_for_deep_dive, handle_problem_intro,
    handle_problem_deep_dive, handle_one_time_help,
    handle_regular_volunteering, handle_probono_info,
    handle_probono_benefits,
    start_game, handle_game_answer,
    start_navigator, handle_navigator_answer,
    handle_safety, handle_safety_money, handle_safety_volunteering,
    handle_safety_algorithm,
    start_detective, handle_detective_answer,
    start_quiz, handle_quiz_round1_answer, handle_quiz_round2_answer,
    ask_quiz_question,
    handle_quiz_next_round
)
from keyboards import (
    kb_main, kb_problems, kb_why_not_state, kb_after_deep_dive,
    kb_help_format, kb_after_info, kb_after_game,
    kb_resources, kb_after_detective, kb_quiz_round1_options,
    kb_after_quiz_question, kb_after_quiz_finish, kb_main_only
)
from utils import send_message
from content import PROBLEMS


def dispatch(vk, user_id, message_text):
    msg = message_text.strip()
    state_data = user_states.get(user_id, {})
    state = state_data.get("state", "new")

    # ── Глобальные команды ──
    if msg.lower() in ["/start", "старт", "начать", "привет", "start",
                       "🏠 главное меню", "в главное меню", "главное меню"]:
        handle_start(vk, user_id)
        return

    if msg in ["🔍 Безопасная благотворительность", "Безопасная благотворительность",
               "Алгоритм проверки НКО", "✅ Алгоритм проверки НКО", "📋 Алгоритм проверки НКО"]:
        handle_safety(vk, user_id)
        return

    if msg in ["💸 Денежная помощь: как правильно", "Денежная помощь", "Денежная помощь: как правильно"]:
        handle_safety_money(vk, user_id)
        return

    if msg in ["🤝 Безопасное волонтёрство", "Безопасное волонтёрство"]:
        handle_safety_volunteering(vk, user_id)
        return

    if msg in ["🚦 Алгоритм действий (5 шагов)", "Алгоритм действий", "Алгоритм действий (5 шагов)"]:
        handle_safety_algorithm(vk, user_id)
        return

    if msg in ["🔎 Социальный детектив", "Социальный детектив", "➡️ Следующее дело", "Следующее дело"]:
        start_detective(vk, user_id)
        return

    if msg in ["🎮 Квиз «Конструктор доброты»", "Квиз", "Квиз «Конструктор доброты»",
               "🔁 Пройти квиз ещё раз", "Пройти квиз ещё раз"]:
        start_quiz(vk, user_id)
        return

    if msg in ["📖 Знакомство с социальной проблемой", "Знакомство с социальной проблемой"]:
        handle_why_not_state(vk, user_id)
        return

    if msg in ["📖 Познакомиться с социальной проблемой", "Познакомиться с социальной проблемой",
               "📖 Познакомиться с другой проблемой", "Познакомиться с другой проблемой"]:
        handle_select_problem_for_deep_dive(vk, user_id)
        return

    if msg in ["🗺️ Найти свою траекторию", "Найти свою траекторию", "Тест-навигатор",
               "🗺️ Тогда что могу сделать я?", "Тогда что могу сделать я?"]:
        start_navigator(vk, user_id)
        return

    if msg in ["💡 Про pro bono", "Про pro bono", "🎯 Зачем это мне?"]:
        handle_probono_benefits(vk, user_id)
        return

    if msg in ["🕵️ Игра: проверь сбор", "Игра", "Игра: проверь сбор", "➡️ Следующий кейс", "Следующий кейс"]:
        start_game(vk, user_id)
        return

    if msg in ["ℹ️ О проекте", "О проекте", "Расскажи о проекте"]:
        handle_about(vk, user_id)
        return

    if msg in ["← Выбрать другую тему", "Выбрать другую тему", "Другая тема"]:
        text = "Выбери тему, которая тебе близка:"
        send_message(vk, user_id, text, kb_problems())
        user_states[user_id] = {"state": "selecting_problem"}
        return

    # ── Обработка кнопки «Дальше» для пошагового просмотра ──
    if msg == "➡️ Дальше" and state == "why_not_state":
        handle_why_next(vk, user_id)
        return

    # ── Обработка кнопки «Следующий раунд» для квиза ──
    if msg == "➡️ Следующий раунд" and state == "quiz_round1_finished":
        handle_quiz_next_round(vk, user_id)
        return

    # ── Машина состояний ──
    if state == "new":
        handle_start(vk, user_id)

    elif state == "main_menu":
        if msg == "🚀 Начать":
            text = "Выбери социальную проблему, которая тебе близка:"
            send_message(vk, user_id, text, kb_problems())
            user_states[user_id] = {"state": "selecting_problem"}
        elif msg == "ℹ️ О проекте":
            handle_about(vk, user_id)
        elif msg == "🗺️ Найти свою траекторию":
            start_navigator(vk, user_id)
        elif msg == "🔍 Безопасная благотворительность":
            handle_safety(vk, user_id)
        else:
            send_message(vk, user_id, "Нажми на одну из кнопок 👆", kb_main())

    elif state == "selecting_problem":
        if msg in PROBLEMS:
            handle_problem_intro(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Выбери тему из кнопок ниже:", kb_problems())

    elif state == "why_not_state_shown":
        if msg in ["📖 Познакомиться с социальной проблемой", "Познакомиться с социальной проблемой"]:
            handle_select_problem_for_deep_dive(vk, user_id)
        elif msg in ["🗺️ Тогда что могу сделать я?", "Тогда что могу сделать я?"]:
            start_navigator(vk, user_id)
        else:
            send_message(vk, user_id, "Используй кнопки ниже 👆", kb_why_not_state())

    elif state == "selecting_problem_deep_dive":
        if msg in PROBLEMS:
            handle_problem_deep_dive(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Выбери тему из кнопок ниже:", kb_problems())

    elif state == "deep_dive_shown":
        problem = state_data.get("problem", "")
        if msg in ["🗺️ Тогда что могу сделать я?", "Тогда что могу сделать я?"]:
            start_navigator(vk, user_id)
        elif msg in ["📋 Узнать форматы помощи", "Узнать форматы помощи"]:
            handle_problem_intro(vk, user_id, problem)
        elif msg in ["📖 Познакомиться с другой проблемой", "Познакомиться с другой проблемой"]:
            handle_select_problem_for_deep_dive(vk, user_id)
        else:
            send_message(vk, user_id, "Используй кнопки ниже 👆", kb_after_deep_dive())

    elif state == "chosen_problem":
        problem = state_data.get("problem", "")
        if msg in ["⚡ Разовая помощь", "Разовая помощь"]:
            handle_one_time_help(vk, user_id, problem)
        elif msg in ["🤝 Регулярное волонтёрство", "Регулярное волонтёрство"]:
            handle_regular_volunteering(vk, user_id, problem)
        elif msg in ["💡 Pro bono (мои навыки)", "Pro bono"]:
            handle_probono_info(vk, user_id, problem)
        elif msg in ["🕵️ Игра: проверь сбор", "Игра"]:
            start_game(vk, user_id)
        elif msg in ["← Выбрать другую тему", "Выбрать другую тему"]:
            send_message(vk, user_id, "Выбери другую тему:", kb_problems())
            user_states[user_id] = {"state": "selecting_problem"}
        else:
            send_message(vk, user_id, "Используй кнопки для выбора 👆", kb_help_format())

    elif state == "probono_shown":
        problem = state_data.get("problem", "")
        if msg in ["🎯 Зачем это мне?", "Зачем это мне?"]:
            handle_probono_benefits(vk, user_id)
        elif msg in ["🕵️ Игра: проверь сбор", "Игра"]:
            start_game(vk, user_id)
        elif msg in ["← Выбрать другую тему"]:
            send_message(vk, user_id, "Выбери другую тему:", kb_problems())
            user_states[user_id] = {"state": "selecting_problem"}
        else:
            send_message(vk, user_id, "Выбери действие:", kb_after_info())

    elif state == "game_waiting":
        if msg:
            handle_game_answer(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Выбери один из вариантов, нажав на кнопку.")

    elif state == "after_game":
        if msg in ["➡️ Следующий кейс", "Следующий кейс"]:
            start_game(vk, user_id)
        elif msg in ["📋 Алгоритм проверки НКО", "Алгоритм проверки НКО"]:
            handle_safety(vk, user_id)
        elif msg in ["← Выбрать тему", "Выбрать тему"]:
            send_message(vk, user_id, "Выбери тему:", kb_problems())
            user_states[user_id] = {"state": "selecting_problem"}
        else:
            send_message(vk, user_id, "Используй кнопки 👆", kb_after_game())

    elif state == "navigator":
        handle_navigator_answer(vk, user_id, msg)

    elif state == "after_navigator":
        send_message(vk, user_id, "Что дальше?", kb_after_info(include_game=True))
        user_states[user_id]["state"] = "main_menu"

    elif state == "safety_shown":
        if msg in ["💡 Про pro bono", "Про pro bono"]:
            handle_probono_benefits(vk, user_id)
        elif msg in ["🕵️ Игра: проверь сбор", "Игра"]:
            start_game(vk, user_id)
        elif msg in ["💸 Денежная помощь: как правильно", "Денежная помощь"]:
            handle_safety_money(vk, user_id)
        elif msg in ["🤝 Безопасное волонтёрство", "Безопасное волонтёрство"]:
            handle_safety_volunteering(vk, user_id)
        elif msg in ["🚦 Алгоритм действий (5 шагов)", "Алгоритм действий"]:
            handle_safety_algorithm(vk, user_id)
        elif msg in ["🔎 Социальный детектив", "Социальный детектив"]:
            start_detective(vk, user_id)
        else:
            send_message(vk, user_id, "Выбери действие:", kb_resources())

    elif state == "detective_waiting":
        if msg in ["Мошенник", "Можно помогать"]:
            handle_detective_answer(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Нажми одну из кнопок: «Мошенник» или «Можно помогать»")

    elif state == "after_detective":
        if msg in ["➡️ Следующее дело", "Следующее дело"]:
            start_detective(vk, user_id)
        elif msg in ["🔍 Безопасная благотворительность", "Безопасная благотворительность"]:
            handle_safety(vk, user_id)
        else:
            send_message(vk, user_id, "Используй кнопки 👆", kb_after_detective())

    elif state == "quiz_round1":
        if msg:
            handle_quiz_round1_answer(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Нажми одну из кнопок с вариантом ответа.")

    elif state == "quiz_round2":
        if msg:
            handle_quiz_round2_answer(vk, user_id, msg)
        else:
            send_message(vk, user_id, "Напиши свой ответ текстом 👆")

    elif state == "quiz_after_question":
        if msg in ["➡️ Следующий вопрос", "Следующий вопрос"]:
            ask_quiz_question(vk, user_id)
        else:
            send_message(vk, user_id, "Используй кнопку 👆", kb_after_quiz_question())

    elif state == "after_quiz":
        if msg in ["🔁 Пройти квиз ещё раз", "Пройти квиз ещё раз"]:
            start_quiz(vk, user_id)
        elif msg in ["🗺️ Найти свою траекторию", "Найти свою траекторию"]:
            start_navigator(vk, user_id)
        else:
            send_message(vk, user_id, "Что дальше?", kb_after_quiz_finish())

    else:
        handle_start(vk, user_id)
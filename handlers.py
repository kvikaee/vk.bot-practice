import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from content import (
    PROBLEMS, WHY_NOT_ONLY_STATE_STEPS, NAVIGATOR_QUESTIONS, NAVIGATOR_RESULTS,
    QUIZ_ROUND1, QUIZ_ROUND2, GAME_CASES, DETECTIVE_CASES,
    SAFETY_CHECKLIST, SAFETY_MONEY, SAFETY_VOLUNTEERING,
    PROBONO_BENEFITS, SAFETY_ALGORITHM,
    QUIZ_ATTACHMENTS   # <-- добавили импорт
)
from config import WEIGHT_PRIMARY, WEIGHT_SECONDARY
from keyboards import (
    kb_main, kb_problems, kb_help_format, kb_why_not_state,
    kb_after_deep_dive, kb_yes_no, kb_after_info,
    kb_game_options, kb_after_game, kb_navigator_options,
    kb_resources, kb_main_only, kb_detective_options,
    kb_after_detective, kb_quiz_round1_options,
    kb_quiz_round2_hint, kb_after_quiz_question, kb_after_quiz_finish,
    kb_why_next, kb_quiz_next_round, kb_after_last_game, kb_after_last_detective
)
from state import user_states
from utils import send_message


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

def get_question_by_id(qid):
    for q in NAVIGATOR_QUESTIONS:
        if q["id"] == qid:
            return q
    return None


# ==================== ОБРАБОТЧИКИ ====================

def handle_start(vk, user_id):
    text = (
        "👋 Привет! Я бот проекта «Конструктор доброты».\n\n"
        "Помогаю студентам и молодым людям разобраться:\n"
        "— какие социальные проблемы есть вокруг нас\n"
        "— как помогать по-настоящему (и не попасться мошенникам!)\n"
        "— как найти свою траекторию помощи\n\n"
        "Выбери, с чего начнём 👇"
    )
    send_message(vk, user_id, text, kb_main())
    user_states[user_id] = {"state": "main_menu"}


def handle_about(vk, user_id):
    text = (
        "🌟 О ПРОЕКТЕ «КОНСТРУКТОР ДОБРОТЫ»\n\n"
        "Проект помогает студентам увидеть социальные проблемы города "
        "и найти свой способ их решать.\n\n"
        "Наш опыт: многие хотят помочь, но переводят деньги на сомнительные "
        "сборы в интернете — разочаровываются и бросают.\n\n"
        "Мы хотим показать:\n"
        "🔹 Помогать можно по-разному\n"
        "🔹 Не обязательно быть волонтёром на массовых акциях\n"
        "🔹 Можно применить свои профессиональные навыки (IT, дизайн, юриспруденция) "
        "для реальной пользы — это называется pro bono\n\n"
    )
    send_message(vk, user_id, text, kb_main())
    user_states[user_id]["state"] = "main_menu"


# ========== ОБРАБОТКА ШАГОВ «ПОЧЕМУ ГОСУДАРСТВО» ==========

def handle_why_not_state(vk, user_id):
    user_states[user_id] = {"state": "why_not_state", "step": 0}
    send_why_step(vk, user_id)


def send_why_step(vk, user_id):
    data = user_states[user_id]
    step = data.get("step", 0)
    steps = WHY_NOT_ONLY_STATE_STEPS
    if step >= len(steps):
        send_message(
            vk, user_id,
            "Теперь ты знаешь, почему важно помогать через НКО. Что дальше?",
            kb_why_not_state()
        )
        user_states[user_id]["state"] = "why_not_state_shown"
        return
    text = steps[step]
    if step == len(steps) - 1:
        send_message(vk, user_id, text, kb_why_not_state())
        user_states[user_id]["state"] = "why_not_state_shown"
    else:
        send_message(vk, user_id, text, kb_why_next())
        user_states[user_id]["state"] = "why_not_state"
    user_states[user_id]["step"] = step


def handle_why_next(vk, user_id):
    data = user_states.get(user_id, {})
    if data.get("state") != "why_not_state":
        return
    data["step"] = data.get("step", 0) + 1
    send_why_step(vk, user_id)


# ========== ОСТАЛЬНЫЕ ОБРАБОТЧИКИ ==========

def handle_select_problem_for_deep_dive(vk, user_id):
    text = "Выбери социальную проблему, с которой хочешь познакомиться подробнее:"
    send_message(vk, user_id, text, kb_problems())
    user_states[user_id] = {"state": "selecting_problem_deep_dive"}


def handle_problem_intro(vk, user_id, problem):
    info = PROBLEMS[problem]
    text = (
        f"{'=' * 30}\n"
        f"{problem}\n"
        f"{'=' * 30}\n\n"
        f"{info['short']}\n\n"
        "Что тебе ближе?"
    )
    send_message(vk, user_id, text, kb_help_format())
    user_states[user_id] = {"state": "chosen_problem", "problem": problem}


def handle_problem_deep_dive(vk, user_id, problem):
    info = PROBLEMS[problem]
    intro_text = f"{'=' * 30}\n{problem}\n{'=' * 30}"
    send_message(vk, user_id, intro_text)
    # Если есть прикреплённое видео – отправляем его
    if info.get("video_attachment"):
        send_message(vk, user_id, "🎬 Видео по теме:", attachment=info["video_attachment"])
    # Если есть текстовая ссылка – отправляем как текст (для обратной совместимости)
    elif info.get("video"):
        send_message(vk, user_id, info["video"])
    deep_text = info.get("deep_dive") or info["short"]
    send_message(vk, user_id, deep_text, kb_after_deep_dive())
    user_states[user_id] = {"state": "deep_dive_shown", "problem": problem}


def handle_one_time_help(vk, user_id, problem):
    text = (
        f"⚡ РАЗОВАЯ ПОМОЩЬ: {problem}\n\n"
        "Разовые дела — быстро и без долгой привязки:\n"
        "• Прийти на субботник\n"
        "• Привезти необходимые вещи\n"
        "• Помочь на мероприятии фонда\n"
        "• Сделать репост важной информации\n\n"
        "Даже один раз — это кирпичик, который что-то строит.\n\n"
        "🔗 Ищи разовые задачи на ДОБРО.РФ: dobro.ru"
    )
    send_message(vk, user_id, text, kb_after_info())


def handle_regular_volunteering(vk, user_id, problem):
    text = (
        f"🤝 РЕГУЛЯРНОЕ ВОЛОНТЁРСТВО: {problem}\n\n"
        "Регулярное волонтёрство даёт глубокую связь с делом:\n"
        "• Ты становишься частью команды\n"
        "• Видишь реальные изменения\n"
        "• Приобретаешь опыт и навыки\n"
        "• Не выгораешь — потому что ты не один\n\n"
        "Важно: начни с чего-то реального. Не бери на себя больше, "
        "чем можешь — это ведёт к выгоранию.\n\n"
        "🔗 Найди проект рядом с домом:\n"
        "• ДОБРО.РФ (dobro.ru)\n"
        "• Платформа «Сделай!» (sdelai.org)"
    )
    send_message(vk, user_id, text, kb_after_info())


def handle_probono_info(vk, user_id, problem):
    info = PROBLEMS[problem]
    tasks = "\n".join(f"• {t}" for t in info["probono"])
    text = (
        f"💡 PRO BONO для темы «{problem}»\n\n"
        "Pro bono — использовать свои профессиональные навыки "
        "бесплатно для помощи НКО.\n\n"
        f"Примеры задач:\n{tasks}\n\n"
        f"🔗 Где искать задачи:\n{info['nko'][-1]}\n"
        "   ProCharity (procharity.ru)"
    )
    kb = VkKeyboard(one_time=False)
    kb.add_button("🎯 Зачем это мне?", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🕵️ Игра: проверь сбор", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("← Выбрать другую тему", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    send_message(vk, user_id, text, kb)
    user_states[user_id]["state"] = "probono_shown"


def handle_probono_benefits(vk, user_id):
    send_message(vk, user_id, PROBONO_BENEFITS, kb_after_info(include_game=True))


# ==================== ИГРА ====================

def start_game(vk, user_id):
    case_index = user_states[user_id].get("game_case_index", 0)
    if case_index >= len(GAME_CASES):
        case_index = 0
    case = GAME_CASES[case_index]
    text = case["text"] + "\n\n" + "\n".join(case["options"])
    send_message(vk, user_id, text, kb_game_options(case["options"]))
    user_states[user_id]["state"] = "game_waiting"
    user_states[user_id]["game_case_index"] = case_index
    user_states[user_id]["game_answered"] = []


def handle_game_answer(vk, user_id, answer_text):
    if not answer_text:
        return
    letter = answer_text[0].upper()
    case_index = user_states[user_id].get("game_case_index", 0)
    case = GAME_CASES[case_index]
    is_correct = case["answers"].get(letter, False)
    correct_letters = case["correct"]
    if is_correct:
        result_icon, result_text = "✅", "Правильно!"
    else:
        result_icon, result_text = "❌", "Не совсем."
    text = (
        f"{result_icon} {result_text}\n\n"
        f"{case['explain']}\n\n"
        f"Правильные ответы: {', '.join(correct_letters)}"
    )
    next_index = (case_index + 1) % len(GAME_CASES)
    user_states[user_id]["game_case_index"] = next_index
    user_states[user_id]["state"] = "after_game"
    if next_index == 0:
        send_message(vk, user_id, text, kb_after_last_game())
    else:
        send_message(vk, user_id, text, kb_after_game())


# ==================== ТЕСТ-НАВИГАТОР ====================

def start_navigator(vk, user_id):
    intro_text = (
        "🗺️ ТЕСТ-НАВИГАТОР\n«Какая помощь подходит тебе? Найди свою траекторию помощи»\n\n"
        "Наш чат-бот поможет тебе найти ту самую точку приложения сил, где твой "
        "талант (код, рисунок, доброе слово, золотые руки) принесёт максимальную "
        "пользу.\n\n"
        "Я помогу тебе понять, как именно ты можешь помогать решать "
        "социальные проблемы. Это не про деньги. Это про твои навыки и интересы!"
    )
    send_message(vk, user_id, intro_text)

    why_systemic_text = (
        "Ты когда-нибудь переводил деньги на личную карту «больному ребёнку»? "
        "Или хотел помочь бездомному, но не знал, как и кому? Или даже придумал "
        "крутую идею: «Вот бы сделать приют для собак!» — но бросил на полпути, "
        "потому что одному тянуть тяжело.\n\n"
        "Это нормально. Но это — путь в никуда.\n\n"
        "Помощь в одиночку — это:\n"
        "• рисковать, что деньги пойдут мошенникам;\n"
        "• тратить силы на то, в чём ты не специалист;\n"
        "• быстро выгорать, потому что один в поле не воин;\n"
        "• достигать максимум локального эффекта (помог одному — а проблема "
        "осталась).\n\n"
        "Системная помощь через НКО — это когда твоя добрая воля превращается "
        "в реальные изменения.\n\n"
        "НКО — это команда экспертов: юристы, психологи, врачи, менеджеры. "
        "Они уже знают:\n"
        "• как легально собрать средства (не на личную карту);\n"
        "• как проверить, кому нужна помощь;\n"
        "• как отчитаться перед донорами;\n"
        "• как масштабировать успех.\n\n"
        "Ты можешь не уметь всего этого. Но ты можешь сделать то, что умеешь ты. "
        "И встроить свой навык в уже работающую систему. Как винтик в механизм. "
        "Как аккумулятор в фонарик. Как нить в ткань.\n\n"
        "Помогать можно по-разному. Но системная помощь — единственная, которая "
        "реально меняет мир.\n\n"
        "Отвечай «да» или «нет» честно :)"
    )
    send_message(vk, user_id, why_systemic_text)

    user_states[user_id]["state"] = "navigator"
    user_states[user_id]["nav_question"] = "q1"
    user_states[user_id]["nav_scores"] = {}
    user_states[user_id]["nav_tags"] = []
    ask_navigator_question(vk, user_id, "q1")


def ask_navigator_question(vk, user_id, qid):
    q = get_question_by_id(qid)
    if not q:
        finish_navigator(vk, user_id)
        return
    send_message(vk, user_id, q["text"], kb_navigator_options(q["buttons"]))
    user_states[user_id]["nav_question"] = qid


def handle_navigator_answer(vk, user_id, answer):
    qid = user_states[user_id].get("nav_question")
    q = get_question_by_id(qid)
    if not q:
        finish_navigator(vk, user_id)
        return

    buttons = q["buttons"]
    is_yes = answer.lower() in ["да", buttons[0].lower()]
    scores = user_states[user_id]["nav_scores"]

    vote = q.get("vote_yes") if is_yes else q.get("vote_no")
    if vote:
        code, weight = vote
        scores[code] = scores.get(code, 0) + weight

    vote_for = q.get("vote_yes_for") if is_yes else q.get("vote_no_for")
    if vote_for:
        code_a, code_b, weight = vote_for
        target = code_a if scores.get(code_a, 0) >= scores.get(code_b, 0) else code_b
        scores[target] = scores.get(target, 0) + weight

    tag = q.get("tag_yes") if is_yes else q.get("tag_no")
    if tag:
        user_states[user_id]["nav_tags"].append(tag)

    next_qid = q["yes_next"] if is_yes else q["no_next"]
    if next_qid == "END":
        finish_navigator(vk, user_id)
    else:
        ask_navigator_question(vk, user_id, next_qid)


def finish_navigator(vk, user_id):
    scores = user_states[user_id].get("nav_scores", {})
    tags = user_states[user_id].get("nav_tags", [])

    if scores:
        max_score = max(scores.values())
        leaders = [code for code, s in scores.items() if s == max_score]
        if len(leaders) == 1:
            result_code = leaders[0]
        else:
            priority_order = ["А", "Б", "В", "Г", "Д", "Е"]
            result_code = next((c for c in priority_order if c in leaders), leaders[0])
    else:
        result_code = "Е"

    result = NAVIGATOR_RESULTS.get(result_code, NAVIGATOR_RESULTS["Е"])

    tags_line = ""
    if tags:
        tags_line = "\n\n🔧 Форматы, которые тебе особенно подходят: " + ", ".join(tags)

    text = (
        f"🎉 Ты получил свою персональную траекторию помощи. "
        f"Как считаешь, она подходит тебе?\n\n"
        f"{result['icon']} {result['name']}\n\n"
        f"{result['desc']}"
        f"{tags_line}\n\n"
        f"{result['platforms']}\n\n"
        "━━━━━━━━━━━━━━━━━\n"
        "Помни: твои интересы могут меняться. Ты можешь попробовать одно, "
        "потом другое, а потом придумать что-то совершенно своё. И это нормально. "
        "Главное — ты размышляешь и ты в движении! 💪"
    )
    user_states[user_id]["state"] = "after_navigator"
    send_message(vk, user_id, text, kb_after_info(include_game=True))


# ==================== БЕЗОПАСНОСТЬ ====================

def handle_safety(vk, user_id):
    send_message(vk, user_id, SAFETY_CHECKLIST, kb_resources())
    user_states[user_id]["state"] = "safety_shown"


def handle_safety_money(vk, user_id):
    send_message(vk, user_id, SAFETY_MONEY, kb_resources())
    user_states[user_id]["state"] = "safety_shown"


def handle_safety_volunteering(vk, user_id):
    send_message(vk, user_id, SAFETY_VOLUNTEERING, kb_resources())
    user_states[user_id]["state"] = "safety_shown"


def handle_safety_algorithm(vk, user_id):
    send_message(vk, user_id, SAFETY_ALGORITHM, kb_resources())
    user_states[user_id]["state"] = "safety_shown"


# ==================== СОЦИАЛЬНЫЙ ДЕТЕКТИВ ====================

def start_detective(vk, user_id):
    case_index = user_states[user_id].get("detective_case_index", 0)
    if case_index >= len(DETECTIVE_CASES):
        case_index = 0
    case = DETECTIVE_CASES[case_index]
    send_message(vk, user_id, case["text"], kb_detective_options())
    user_states[user_id]["state"] = "detective_waiting"
    user_states[user_id]["detective_case_index"] = case_index


def handle_detective_answer(vk, user_id, answer_text):
    case_index = user_states[user_id].get("detective_case_index", 0)
    case = DETECTIVE_CASES[case_index]
    is_correct = answer_text == case["correct"]
    result_icon = "✅" if is_correct else "❌"
    result_text = "Верно!" if is_correct else "Не совсем."
    text = f"{result_icon} {result_text}\n\n{case['explain']}"
    next_index = (case_index + 1) % len(DETECTIVE_CASES)
    user_states[user_id]["detective_case_index"] = next_index
    user_states[user_id]["state"] = "after_detective"
    if next_index == 0:
        send_message(vk, user_id, text, kb_after_last_detective())
    else:
        send_message(vk, user_id, text, kb_after_detective())


# ==================== КВИЗ С КАРТИНКАМИ ИЗ ГРУППЫ ====================

QUIZ_TOTAL_QUESTIONS = len(QUIZ_ROUND1) + len(QUIZ_ROUND2)


def start_quiz(vk, user_id):
    intro = (
        "🎮 ИНТЕЛЛЕКТУАЛЬНО-РАЗВЛЕКАТЕЛЬНЫЙ КВИЗ «КОНСТРУКТОР ДОБРОТЫ»\n\n"
        "Бездомные животные, одиночество пожилых, мусор в реках, дети, оставшиеся "
        "без родителей, трудные подростки, люди с инвалидностью — эти проблемы рядом "
        "с нами, но знаем ли мы, как их решать?\n\n"
        "Проверим, какие социальные проблемы существуют, кто их решает и как каждый "
        "из нас может включиться — через любимые мультфильмы и их героев!\n\n"
        f"📋 Всего {QUIZ_TOTAL_QUESTIONS} вопросов в 2 раундах:\n"
        f"• Раунд 1 — {len(QUIZ_ROUND1)} вопросов с вариантами ответа\n"
        f"• Раунд 2 — {len(QUIZ_ROUND2)} вопросов, ответ пишешь текстом\n\n"
        "За каждый правильный ответ — 1 балл. Поехали! 🚀"
    )
    send_message(vk, user_id, intro)
    user_states[user_id]["state"] = "quiz_round1"
    user_states[user_id]["quiz_round"] = 1
    user_states[user_id]["quiz_index"] = 0
    user_states[user_id]["quiz_score"] = 0
    ask_quiz_question(vk, user_id)


def ask_quiz_question(vk, user_id):
    state_data = user_states[user_id]
    round_num = state_data.get("quiz_round", 1)
    idx = state_data["quiz_index"]

    if round_num == 1:
        if idx >= len(QUIZ_ROUND1):
            user_states[user_id]["state"] = "quiz_round1_finished"
            send_message(
                vk, user_id,
                "🏁 Раунд 1 окончен! Переходим к раунду 2 — «Последний шанс».\n"
                "Нажми кнопку ниже, чтобы продолжить.",
                kb_quiz_next_round()
            )
            return

        state_data["state"] = "quiz_round1"
        q = QUIZ_ROUND1[idx]
        text = q["question"] + "\n\n" + "\n".join(q["options"])
        num = idx + 1
        key = f"q{num}"
        attachment = QUIZ_ATTACHMENTS.get(key)  # берём из словаря

        # Для 11-го (индекс 10) и 16-го (индекс 15) вопросов – короткие кнопки
        if idx == 10 or idx == 15:
            button_options = ["А", "Б", "В", "Г"]
        else:
            button_options = q["options"]

        send_message(vk, user_id, text, kb_quiz_round1_options(button_options), attachment)

    elif round_num == 2:
        if idx >= len(QUIZ_ROUND2):
            finish_quiz(vk, user_id)
            return
        state_data["state"] = "quiz_round2"
        q = QUIZ_ROUND2[idx]
        real_num = idx + 1 + len(QUIZ_ROUND1)
        key = f"q{real_num}"
        attachment = QUIZ_ATTACHMENTS.get(key)
        send_message(vk, user_id, q["question"], kb_quiz_round2_hint(), attachment)


def handle_quiz_round1_answer(vk, user_id, answer_text):
    if not answer_text:
        return
    letter = answer_text[0].upper()
    state_data = user_states[user_id]
    idx = state_data["quiz_index"]
    q = QUIZ_ROUND1[idx]
    is_correct = letter == q["correct"]
    if is_correct:
        state_data["quiz_score"] += 1
        result_icon, result_text = "✅", "Правильно!"
    else:
        result_icon, result_text = "❌", "Не совсем."
    text = f"{result_icon} {result_text}\n\n{q['explain']}"
    num = idx + 1
    key = f"ans{num}"
    attachment = QUIZ_ATTACHMENTS.get(key)
    state_data["quiz_index"] = idx + 1
    state_data["quiz_round"] = 1
    state_data["state"] = "quiz_after_question"
    send_message(vk, user_id, text, kb_after_quiz_question(), attachment)


def handle_quiz_round2_answer(vk, user_id, answer_text):
    state_data = user_states[user_id]
    idx = state_data["quiz_index"]
    q = QUIZ_ROUND2[idx]
    normalized = answer_text.strip().lower()
    is_correct = normalized in q["correct_answers"]
    if is_correct:
        state_data["quiz_score"] += 1
        result_icon, result_text = "✅", "Правильно!"
    else:
        result_icon, result_text = "❌", "Не совсем."
    text = f"{result_icon} {result_text}\n\n{q['explain']}"
    real_num = idx + 1 + len(QUIZ_ROUND1)
    key = f"ans{real_num}"
    attachment = QUIZ_ATTACHMENTS.get(key)
    state_data["quiz_index"] = idx + 1
    state_data["quiz_round"] = 2
    state_data["state"] = "quiz_after_question"
    send_message(vk, user_id, text, kb_after_quiz_question(), attachment)


def finish_quiz(vk, user_id):
    score = user_states[user_id].get("quiz_score", 0)
    total = QUIZ_TOTAL_QUESTIONS
    if score == total:
        rank = "🏆 Безупречно! Ты настоящий Конструктор перемен!"
    elif score >= total * 0.7:
        rank = "🌟 Отличный результат! Ты явно разбираешься в теме."
    elif score >= total * 0.4:
        rank = "👍 Неплохо! Но точно есть, что узнать ещё."
    else:
        rank = "🌱 Начало положено — а дальше будет только интереснее."

    text = (
        f"🎉 Квиз завершён!\n\n"
        f"Твой результат: {score} из {total} баллов.\n\n"
        f"{rank}\n\n"
        "Конструировать добро могут только самые сообразительные! "
        "Спасибо за игру 💙"
    )
    user_states[user_id]["state"] = "after_quiz"
    attachment = QUIZ_ATTACHMENTS.get("final")
    send_message(vk, user_id, text, kb_after_quiz_finish(), attachment)


def handle_quiz_next_round(vk, user_id):
    state_data = user_states.get(user_id, {})
    if state_data.get("state") != "quiz_round1_finished":
        return
    state_data["state"] = "quiz_round2"
    state_data["quiz_round"] = 2
    state_data["quiz_index"] = 0
    ask_quiz_question(vk, user_id)
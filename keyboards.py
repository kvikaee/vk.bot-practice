from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from content import PROBLEMS


def kb_main():
    kb = VkKeyboard(one_time=False)
    kb.add_button("🚀 Начать", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("ℹ️ О проекте", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("📖 Знакомство с социальной проблемой", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🗺️ Найти свою траекторию", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🔍 Безопасная благотворительность", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🎮 Квиз «Конструктор доброты»", color=VkKeyboardColor.POSITIVE)
    return kb


def kb_problems():
    kb = VkKeyboard(one_time=False)
    problems_list = list(PROBLEMS.keys())
    for i, p in enumerate(problems_list):
        kb.add_button(p, color=VkKeyboardColor.SECONDARY)
        if i < len(problems_list) - 1:
            kb.add_line()
    return kb


def kb_help_format():
    kb = VkKeyboard(one_time=False)
    kb.add_button("⚡ Разовая помощь", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🤝 Регулярное волонтёрство", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("💡 Pro bono (мои навыки)", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🕵️ Игра: проверь сбор", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("← Выбрать другую тему", color=VkKeyboardColor.SECONDARY)
    return kb


def kb_why_next():
    kb = VkKeyboard(one_time=False)
    kb.add_button("➡️ Дальше", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_why_not_state():
    kb = VkKeyboard(one_time=False)
    kb.add_button("📖 Познакомиться с социальной проблемой", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🗺️ Тогда что могу сделать я?", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_after_deep_dive():
    kb = VkKeyboard(one_time=False)
    kb.add_button("🗺️ Тогда что могу сделать я?", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("📋 Узнать форматы помощи", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("📖 Познакомиться с другой проблемой", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_yes_no():
    kb = VkKeyboard(one_time=True)
    kb.add_button("Да", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("Нет", color=VkKeyboardColor.NEGATIVE)
    return kb


def kb_after_info(include_game=True):
    kb = VkKeyboard(one_time=False)
    if include_game:
        kb.add_button("🕵️ Игра: проверь сбор", color=VkKeyboardColor.NEGATIVE)
        kb.add_line()
    kb.add_button("🗺️ Найти свою траекторию", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("← Выбрать другую тему", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_game_options(options):
    kb = VkKeyboard(one_time=True)
    for i, opt in enumerate(options):
        label = opt if len(opt) <= 40 else opt[:39] + "…"
        kb.add_button(label, color=VkKeyboardColor.SECONDARY)
        if i < len(options) - 1:
            kb.add_line()
    return kb


def kb_after_game():
    kb = VkKeyboard(one_time=False)
    kb.add_button("➡️ Следующий кейс", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("📋 Алгоритм проверки НКО", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("← Выбрать тему", color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_navigator_options(options):
    kb = VkKeyboard(one_time=True)
    for i, opt in enumerate(options):
        kb.add_button(opt, color=VkKeyboardColor.SECONDARY)
        if i < len(options) - 1:
            kb.add_line()
    return kb


def kb_resources():
    kb = VkKeyboard(one_time=False)
    kb.add_button("✅ Алгоритм проверки НКО", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🚦 Алгоритм действий (5 шагов)", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("💸 Денежная помощь: как правильно", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🤝 Безопасное волонтёрство", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🕵️ Игра: проверь сбор", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("🔎 Социальный детектив", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("💡 Про pro bono", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_main_only():
    kb = VkKeyboard(one_time=False)
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_detective_options():
    kb = VkKeyboard(one_time=True)
    kb.add_button("Мошенник", color=VkKeyboardColor.NEGATIVE)
    kb.add_line()
    kb.add_button("Можно помогать", color=VkKeyboardColor.POSITIVE)
    return kb


def kb_after_detective():
    kb = VkKeyboard(one_time=False)
    kb.add_button("➡️ Следующее дело", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🔍 Безопасная благотворительность", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_quiz_round1_options(options):
    kb = VkKeyboard(one_time=True)
    for i, opt in enumerate(options):
        label = opt if len(opt) <= 40 else opt[:39] + "…"
        kb.add_button(label, color=VkKeyboardColor.SECONDARY)
        if i < len(options) - 1:
            kb.add_line()
    return kb


def kb_quiz_round2_hint():
    kb = VkKeyboard(one_time=False)
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_after_quiz_question():
    kb = VkKeyboard(one_time=False)
    kb.add_button("➡️ Следующий вопрос", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb


def kb_after_quiz_finish():
    kb = VkKeyboard(one_time=False)
    kb.add_button("🔁 Пройти квиз ещё раз", color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button("🗺️ Найти свою траекторию", color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button("🏠 Главное меню", color=VkKeyboardColor.PRIMARY)
    return kb

def kb_quiz_next_round():
    kb = VkKeyboard(one_time=False)
    kb.add_button("➡️ Следующий раунд", color=VkKeyboardColor.POSITIVE)
    return kb

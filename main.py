import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import TOKEN, GROUP_ID  # GROUP_ID не используется, но можно оставить
from dispatcher import dispatch
from utils import send_message
from keyboards import kb_main_only  # для обработки ошибок


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("✅ Бот «Конструктор доброты» запущен!")
    print("   Нажмите Ctrl+C для остановки\n")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message_text = event.text.strip()
            if not message_text:
                continue
            try:
                dispatch(vk, user_id, message_text)
            except Exception as e:
                print(f"Ошибка для пользователя {user_id}: {e}")
                try:
                    send_message(vk, user_id,
                                 "Произошла ошибка. Напиши «Старт» чтобы начать заново.",
                                 kb_main_only())
                except Exception:
                    pass


if __name__ == "__main__":
    main()
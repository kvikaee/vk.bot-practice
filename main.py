
import time

import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.exceptions import ApiError

from config import TOKEN, GROUP_ID
from dispatcher import dispatch
from utils import send_message
from keyboards import kb_main_only


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()

    print("Бот «Конструктор доброты» запускается...")

    while True:
        try:
            longpoll = VkBotLongPoll(vk_session, GROUP_ID)
            print("Бот подключён к Long Poll.")

            for event in longpoll.listen():
                if event.type != VkBotEventType.MESSAGE_NEW:
                    continue

                message = event.obj.message

                # Обрабатываем только личные сообщения сообщества.
                if message.peer_id != message.from_id:
                    continue

                user_id = message.from_id
                message_text = (message.text or "").strip()

                if not message_text:
                    continue

                try:
                    dispatch(vk, user_id, message_text)
                except Exception as e:
                    print(f"Ошибка для пользователя {user_id}: {e}")
                    try:
                        send_message(
                            vk,
                            user_id,
                            "Произошла ошибка. Напиши «Старт», чтобы начать заново.",
                            kb_main_only(),
                        )
                    except Exception as send_error:
                        print(f"Не удалось отправить сообщение: {send_error}")

        except (requests.exceptions.RequestException, ApiError, OSError) as e:
            print(f"Ошибка соединения с VK: {e}")
            print("Повторное подключение через 5 секунд...")
            time.sleep(5)


if __name__ == "__main__":
    main()

import os
import random
import vk_api
from vk_api.upload import VkUpload

# Кэш для загруженных фото: {file_path: attachment_string}
_photo_cache = {}

def send_message(vk, user_id, text, keyboard=None, attachment=None):
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    if attachment:
        params["attachment"] = attachment
    vk.messages.send(**params)


def get_photo_attachment(vk, file_path):
    """
    Загружает фото на сервер ВК и возвращает attachment строку.
    Результат кэшируется по пути файла.
    """
    if file_path in _photo_cache:
        return _photo_cache[file_path]

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise ValueError(f"Файл повреждён или пустой (0 байт): {file_path}")

    upload = VkUpload(vk)
    try:
        photo = upload.photo_messages(file_path)
    except Exception as e:
        raise RuntimeError(
            f"Не удалось загрузить фото '{file_path}'. "
            f"Проверь: (1) есть ли у токена право 'photos', "
            f"(2) не повреждён ли сам файл, (3) не превышает ли он лимит ВК "
            f"по размеру. Исходная ошибка: {e}"
        ) from e

    owner_id = photo[0]['owner_id']
    photo_id = photo[0]['id']
    access_key = photo[0].get('access_key', '')
    attachment = f"photo{owner_id}_{photo_id}_{access_key}" if access_key else f"photo{owner_id}_{photo_id}"
    _photo_cache[file_path] = attachment
    return attachment

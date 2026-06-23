import random

def send_message(vk, user_id, text, keyboard=None):
    params = {
        "user_id": user_id,
        "message": text,
        "random_id": random.randint(1, 2**31)
    }
    if keyboard:
        params["keyboard"] = keyboard.get_keyboard()
    vk.messages.send(**params)
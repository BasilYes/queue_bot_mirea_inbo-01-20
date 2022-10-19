from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def par():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Очередь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Записаться', color=VkKeyboardColor.PRIMARY)
    return keyboard

def current_player():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Готово', color=VkKeyboardColor.PRIMARY)
    return keyboard

def in_queue():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Очередь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Выписаться', color=VkKeyboardColor.PRIMARY)
    return keyboard

def in_queue_break():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Очередь', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Выписаться', color=VkKeyboardColor.PRIMARY)
    return keyboard

def loaded():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Очередь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Записаться', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Я Хорош', color=VkKeyboardColor.PRIMARY)
    return keyboard
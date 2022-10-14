from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def par():#Игровое меню
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Очередь', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Записаться', color=VkKeyboardColor.PRIMARY)
    return keyboard

def current_player():#Игровое меню
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Готово', color=VkKeyboardColor.PRIMARY)
    return keyboard

    # keyboard = VkKeyboard(one_time=False)
    # keyboard.add_button('Очередь', color=VkKeyboardColor.POSITIVE)
    # keyboard.add_button('Записаться', color=VkKeyboardColor.POSITIVE)
    # keyboard.add_line()
    # keyboard.add_button('Готово', color=VkKeyboardColor.PRIMARY)
    # return keyboard
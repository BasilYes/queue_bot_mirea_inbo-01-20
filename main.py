import os.path
import random
from datetime import datetime

import vk_api
from vk_api.utils import get_random_id

import info
import keyboards

try:
    os.mkdir('Pars')
    file = open('users.txt', 'w', encoding="utf-8")
    file.close()
    file = open('time_table.txt', 'w', encoding="utf-8")
    file.write(
        "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" +
        "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" +
        "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" +
        "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n" + "0 0 0 0 0 0\n"
    )
    file.close()
    print('dir created')
except:
    print('dir found')

from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=info.token)
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

users = {}
start_day = datetime.fromisoformat('2022-08-29')
time_table = []
day = 0
par = 0
current_queue = []
addition_queue = {}
loaded_queue = []
is_break = True
stage = False


# 0 - wait
# 1 - break
# 2 - lesson


def next():
    global current_queue
    send_message_key(current_queue[0],
                     "Партия гордится тобой",
                     keyboards.par().get_keyboard())
    current_queue.pop(0)
    if len(current_queue) > 1:
        send_message(current_queue[1], "Ты следующий, готовься")
    if len(current_queue) > 0:
        send_message_key(current_queue[0],
                         "Твое время пришло, как закончишь - нажми готово",
                         keyboards.current_player().get_keyboard())


def message_distribution(message):
    global Lsvk
    for i in users.keys():
        Lsvk.messages.send(
            user_id=i,
            random_id=get_random_id(),
            message=message
        )
        # vk_session.method('messages.send', {'user_id': i, 'message': message, 'random_id': 0})
    print("Message distribution: " + message)


def message_distribution_key(message, keyboard):
    global Lsvk
    for i in users.keys():
        Lsvk.messages.send(
            user_id=i,
            random_id=get_random_id(),
            keyboard=keyboard,
            message=message
        )
        # vk_session.method('messages.send', {'user_id': i, 'message': message, 'random_id': 0})
    print("Message distribution: " + message)


def send_message_key(user_id, message, keyboard):
    global Lsvk
    Lsvk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        keyboard=keyboard,
        message=message
    )
    # vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


def send_message(user_id, message):
    global Lsvk
    Lsvk.messages.send(
        user_id=user_id,
        random_id=get_random_id(),
        message=message
    )
    # vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


def get_loaded():
    global users
    global current_queue
    out = ""
    counter = 1
    for i in loaded_queue:
        try:
            out += str(counter) + ". " + users[i] + "\n"
        except:
            out += str(counter) + ". " + "Чел с vk id: " + str(i) + ", сделавший невозможное.\n"
        counter += 1
    return out


def get_queue():
    global users
    global current_queue
    out = ""
    counter = 1
    for i in current_queue:
        try:
            out += str(counter) + ". " + users[i] + "\n"
        except:
            out += str(counter) + ". " + "Чел с vk id: " + str(i) + ", сделавший невозможное.\n"
        counter += 1
    for i in addition_queue.keys():
        out += users[i] + " за " + users[addition_queue[i]] + "\n"
    return out


def load_time_table():
    global time_table
    time_table = []
    file = open('time_table.txt', 'r', encoding="utf-8")
    for day in range(14):
        table = []
        time_table.append(file.readline()[:-1].split())
    file.close()


def load_users():
    global users
    file = open('users.txt', 'r', encoding="utf-8")
    out = file.readlines()
    for i in out:
        n = i.split(" ")
        users[int(n[0])] = i[len(n[0]) + 1:-1]
    file.close()


def add_user(user_id, user_name):
    global users
    keys = users.keys()
    if user_id not in keys:
        file = open('users.txt', 'a', encoding="utf-8")
        file.write(str(user_id) + " " + user_name + "\n")
        file.close()
        users[user_id] = user_name
    # else:


def save_current_queue():
    global time_table
    global day
    global current_queue
    file = open("Pars/" + time_table[day][par - 1] + '.txt', 'w', encoding="utf-8")
    for i in current_queue:
        file.write(str(i) + "\n")
    file.close()


def load_queue():
    global time_table
    global day
    global loaded_queue
    global current_queue
    try:
        file = open("Pars/" + time_table[day][par - 1] + '.txt', 'r', encoding="utf-8")
    except:
        file = open("Pars/" + time_table[day][par - 1] + '.txt', 'w', encoding="utf-8")
        file.close()
        file = open("Pars/" + time_table[day][par - 1] + '.txt', 'r', encoding="utf-8")
    loaded_queue = [int(i[:-1]) for i in file.readlines()]
    file.close()
    current_queue = []


def shuffle_queue():
    global loaded_queue
    global current_queue
    global addition_queue
    new_queue = []
    for i in loaded_queue:
        if i in current_queue:
            new_queue.append(i)
    random.shuffle(current_queue)
    for i in current_queue:
        if i not in new_queue:
            new_queue.append(i)
    for i in list(addition_queue.keys())[::-1]:
        new_queue.insert(new_queue.index(addition_queue[i]) + 1, i)
    loaded_queue = []
    current_queue = new_queue
    addition_queue = {}

    message = "Очередь перемешана, текущая очередь:\n" + get_queue()
    keyboard = keyboards.in_queue().get_keyboard()
    global Lsvk
    message_distribution(message)
    for i in current_queue:
        Lsvk.messages.send(
            user_id=i,
            random_id=get_random_id(),
            keyboard=keyboard,
            message="Ты в очереди, Рандом выбрал тебе место."
        )

    if len(current_queue) > 1:
        send_message(current_queue[1], "Второе место по везению, ты следующий, готовься")
    if len(current_queue) > 0:
        send_message_key(current_queue[0], "Рандом всевышний, ты первый, вперед отвечать! Как закончишь, жми на готово.",
                         keyboards.current_player().get_keyboard())


def update_stage():
    global day
    global par
    global is_break
    delta = datetime.now() - start_day
    day = delta.days % len(time_table)
    time = delta.seconds // 60
    print("time: " + str(time / 60))
    l_par = 0
    l_is_break = 0
    if time < 8 * 60 + 30:
        l_par = 0
        l_is_break = True
    elif time < 9 * 60:
        l_par = 1
        l_is_break = True
    elif time < 10 * 60 + 30:
        l_par = 1
        l_is_break = False
    elif time < 10 * 60 + 40:
        l_par = 2
        l_is_break = True
    elif time < 12 * 60 + 10:
        l_par = 2
        l_is_break = False
    elif time < 12 * 60 + 40:
        l_par = 3
        l_is_break = True
    elif time < 14 * 60 + 10:
        l_par = 3
        l_is_break = False
    elif time < 14 * 60 + 20:
        l_par = 4
        l_is_break = True
    elif time < 15 * 60 + 50:
        l_par = 4
        l_is_break = False
    elif time < 16 * 60 + 20:
        l_par = 5
        l_is_break = True
    elif time < 17 * 60 + 50:
        l_par = 5
        l_is_break = False
    elif time < 18 * 60:
        l_par = 6
        l_is_break = True
    elif time < 19 * 60 + 30:
        l_par = 6
        l_is_break = False
    else:
        l_par = 7
        l_is_break = True

    if (l_par != 0 and par != 7) or not is_break:
        if par != l_par:
            print(str(day) + ", " + str(par) + ", " + str(l_par))
            if par > 0 and time_table[day][par - 1] != "0":
                save_current_queue()
                message_distribution_key("Очередь сохранена, На момент сохранения в ней были:\n" + get_queue(),
                                         keyboards.in_queue().get_keyboard())
            par = l_par
            if 1 < par < 7 and time_table[day][par - 1] == time_table[day][par - 2]:
                # message_distribution_key("Между первой и второй, перерывчик небольшой. А для кого-то опять " +
                #                         time_table[day][par - 2] + " и никаких перерывов",
                #                         keyboards.par().get_keyboard())
                is_break = False
            elif 0 < par < 7:
                if time_table[day][par - 1] != "0":
                    load_queue()
                    message_distribution_key("Новая очередь по предмету \"" +
                                             time_table[day][par - 1] +
                                             "\" успей записатся до начала пары, если ты сделал конечно,"
                                             " а если не сделал, не будь 🤡, доделаешь - запишешься."
                                             "Если хочешь записаться за другом, напиши \"я за N\" N-номер"
                                             " твоего друга в очереди. Список с прошлой пары:\n" + get_loaded(),
                                             keyboards.par().get_keyboard())
                    for i in loaded_queue:
                        send_message_key(i, "Ты остался в списке с прошлой пары, если ты действительно не успел сдать,"
                                            " запишись на эту тоже, твоя запись будет в приоритете, а если успел сдать"
                                            " или сдал после окончания пары, пожалуйста нажми кнопку \"Я Хорош\"",
                                         keyboards.loaded().get_keyboard())
                is_break = l_is_break
            else:
                is_break = l_is_break
        elif is_break != l_is_break:
            if 1 < par < 7 and time_table[day][par - 1] == time_table[day][par - 2]:
                is_break = False
            else:
                shuffle_queue()
                is_break = l_is_break
            par = l_par
        else:
            par = l_par
            is_break = l_is_break
    elif par == 7 and is_break != l_is_break:
        print(str(day) + ", " + str(par - 1))
        if time_table[day][par - 2] != "0":
            save_current_queue()
        par = l_par
        is_break = l_is_break
    else:
        par = l_par
        is_break = l_is_break


load_time_table()
load_users()
print(users)
print(time_table)
"116399612"

while True:
    update_stage()

    print("users: " + str(users))
    print("start_day: " + str(start_day))
    print("time_table: " + str(time_table))
    print("day: " + str(day))
    print("par: " + str(par))
    print("current_queue: " + str(current_queue))
    print("loaded_queue: " + str(loaded_queue))
    print("addition_queue: " + str(addition_queue))
    print("is_break: " + str(is_break))
    print("stage: " + str(stage))

    events = Lslongpoll.check()

    # Мне кажется, это должно быть в check
    if Lslongpoll.preload_messages:
        Lslongpoll.preload_message_events_data(events)

    for event in events:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.from_user:
                text = event.text.lower()
                if text[0:3] == "фио":
                    if len(event.text[4:].split(" ")) < 2:
                        send_message(event.user_id, "Дружище, ты забыл написать фамилию И имя после команды фио."
                                                    " Пример правильной команды: \"фио Клоунов Егор\"")
                    else:
                        add_user(event.user_id, event.text[4:])
                        if 0 < par < 6 and time_table[day][par - 1] != "0":
                            send_message_key(event.user_id,
                                             event.text[4:] + " Расстрельный список пополнен.",
                                             keyboards.par().get_keyboard())
                        else:
                            send_message(event.user_id, event.text[4:] + " Расстрельный список пополнен.")
                elif event.user_id not in users:
                    send_message(event.user_id, "Сначала напиши свое ФИО после команды фио."
                                                " Пример правильной команды: \"фио Реуков Василий\"")
                elif 0 < par <= 6 and time_table[day][par - 1] != "0":
                    # if not is_break:
                    print(text)
                    if text == "очередь":
                        if len(current_queue) > 0:
                            send_message(event.user_id, get_queue())
                        else:
                            send_message(event.user_id, "Очередь пуста, у тебя есть шанс стать первым!")
                    elif text == "записаться":
                        print(event.user_id)
                        if event.user_id not in current_queue and event.user_id not in addition_queue:
                            current_queue.append(event.user_id)
                            if is_break:
                                send_message_key(event.user_id, "Ты записан, хорошего тебе перерыва",
                                                 keyboards.in_queue_break().get_keyboard())
                            else:
                                send_message_key(event.user_id, "Ты записан", keyboards.in_queue().get_keyboard())
                            if not is_break:
                                if current_queue[0] == event.user_id:
                                    send_message_key(current_queue[0],
                                                     "Уже первый? скорость заслуживающая уважения иди отвечай,"
                                                     " как закончишь - нажми готово",
                                                     keyboards.current_player().get_keyboard())
                                elif len(current_queue) > 1 and current_queue[1] == event.user_id:
                                    send_message(current_queue[1], "Только зашел и сразу второй, готовься")
                        elif event.user_id in addition_queue:
                            send_message(event.user_id, "Ты хвостиком за " + users[addition_queue[event.user_id]] +
                                         ". Не волнуйся, как начнется пара ты появишься в очереди.")
                        else:
                            send_message(event.user_id, "Астанавись, ты уже в очереди")
                    elif text == "выписаться":
                        if event.user_id in current_queue:
                            if not is_break:
                                if len(current_queue) > 2 and current_queue[1] == event.user_id:
                                    send_message(current_queue[2], "Тут перед тобой скипают,"
                                                                   " ты следующий теперь, готовься")
                                current_queue.remove(event.user_id)
                                send_message_key(event.user_id, "Ты удален из очереди.", keyboards.par().get_keyboard())
                            else:
                                send_message_key(event.user_id,
                                                 "Дружище, подожди, не видишь - очередь еще не перемешана.",
                                                 keyboards.par().get_keyboard())
                        else:
                            send_message(event.user_id, "Ты не в очереди или записался за кем-то,"
                                                        " в таком случае выписаться можно только после начала пары")
                    if is_break:
                        if text[:4] == "я за":
                            if event.user_id not in current_queue:
                                try:
                                    id = int(text[5:].split(" ")[0]) - 1
                                    if len(current_queue) > id >= 0:
                                        if current_queue[id] not in loaded_queue:
                                            addition_queue[event.user_id] = current_queue[id]
                                            send_message(event.user_id, "Ты записался за " + users[current_queue[id]] +
                                                         ", теперь ты его хвостик, не отвертишься.")
                                        else:
                                            send_message(event.user_id, "Твой друг в приоритетной очереди"
                                                                        ", он не успел ответить на прошлой паре,"
                                                                        " ты не можешь записатся с ним."
                                                                        " Запишись с помощью команды \"записаться\","
                                                                        " если вы были друг за дружкой на прошлой паре"
                                                                        " (на которой не успели ответить)"
                                                                        " вас поставит так-же на этой")
                                except:
                                    send_message(event.user_id, "Не пытайся сломать бота,"
                                                                " он может случайно оказаться Скайнетом.")
                            else:
                                send_message(event.user_id, "Ты уже в очереди, хочешь за кем-то записаться?"
                                                            " А все, надо было сначала думать потом делать.")
                        elif text[:7] == "я хорош":
                            if event.user_id in loaded_queue:
                                send_message_key(event.user_id,
                                                 "Ты действительно хорош! Партия гордится тобой! Не забудь записаться в очередь!",
                                                 keyboards.par().get_keyboard())
                                loaded_queue.remove(event.user_id)
                            else:
                                send_message_key(event.user_id,
                                                 "Боря, прекращай!",
                                                 keyboards.par().get_keyboard())
                    else:
                        if text == "готово":
                            if len(current_queue) > 0 and event.user_id == current_queue[0]:
                                next()
                        elif text[:4] == "я за":
                            send_message(event.user_id, "Дружок, пара уже началась,"
                                                        " клуб любителей опаздывать в конце очереди")
                else:
                    send_message(event.user_id, "Не душни, я отдыхаю")

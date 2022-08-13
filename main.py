from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import random
import datetime as dt
import time as ti
from aiogram.types import InputFile


help = 'Добро пожаловать в админ-панель!\nДля установки текста рассылок напишите сообщение, оно автоматически сохранится в документ и будет отсылаться по вашему выбору на определённый адрес либо рассылка по всем юзерам, либо рассылка первому пользователю в очереди. Дальше все функции реализованы так, как написано на кнопках.\nПриятного пользования!'
constant = 21966
id_admin = 520569419


def get_promo_code():
    code_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZqwertyuiopasdfghjklzxcvbnm'
    code = ''
    for i in range(0, 10):
        slice_start = random.randint(0, len(code_chars) - 1)
        code += code_chars[slice_start: slice_start + 1]
    return code


def get_ids_sql():
    global ids
    ids = []
    cur.execute("SELECT id FROM users")
    one_result = cur.fetchall()
    for i in one_result:
        ids.append(i[0])


# Подключение базы данных
conn = sqlite3.connect('users.db')
cur = conn.cursor()

TOKEN = open('token.txt', mode='r', encoding='utf-8').readlines()[0].strip()
print(TOKEN)
# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Выбор языка
keyboard = types.ReplyKeyboardMarkup()
button_rus = types.KeyboardButton('Русский')
button_eng = types.KeyboardButton('English')
keyboard.add(button_rus).add(button_eng)

# Выбор пола
keyboard_sex = types.ReplyKeyboardMarkup()
button_m = types.KeyboardButton('Парень')
button_f = types.KeyboardButton('Девушка')
keyboard_sex.add(button_m).add(button_f)


# Откуда узнали
keyboard_popular = types.ReplyKeyboardMarkup()
button_friend = types.KeyboardButton('Рассказал(а) друг/подруга')
button_TikTok = types.KeyboardButton('Видео в Tik-Tok')
button_Like = types.KeyboardButton('Видео в Like')
keyboard_popular.add(button_friend).add(button_TikTok).add(button_Like)


# Клавиатура да\нет
keyboard_y_n = types.ReplyKeyboardMarkup()
button_yes = types.KeyboardButton('Да')
button_no = types.KeyboardButton('Нет')
keyboard_y_n.add(button_yes).add(button_no)


# Клавиатура самой игры
keyboard_game = types.ReplyKeyboardMarkup()
button_take = types.KeyboardButton('💰Снять')
button_game = types.KeyboardButton('🕹Играть')
button_language = types.KeyboardButton('Language')
button_store = types.KeyboardButton('Магазин')
button_support = types.KeyboardButton('Поддержка')
keyboard_game.row(button_take, button_game).row(button_language, button_store, button_support)


# Клавиатура после игры
keyboard_after_game = types.ReplyKeyboardMarkup()
button_invite = types.KeyboardButton('Пригласить друга')
button_main_menu = types.KeyboardButton('Назад в главное меню')
button_sponsor = types.KeyboardButton('Подписаться на каналы спонсоров')
keyboard_after_game.row(button_invite, button_sponsor).add(button_main_menu)


# Клавиатура назад в главное меню
keyboard_back = types.ReplyKeyboardMarkup()
button_main_menu = types.KeyboardButton('Назад в главное меню')
keyboard_back.add(button_main_menu)


# Клава наебала
keyboard_4x4 = types.ReplyKeyboardMarkup()
b_1 = types.KeyboardButton('🍏')
b_2 = types.KeyboardButton('🍎')
b_3 = types.KeyboardButton('🍐')
b_4 = types.KeyboardButton('🍊')
b_5 = types.KeyboardButton('🍋')
b_6 = types.KeyboardButton('🍌')
b_7 = types.KeyboardButton('🍉')
b_8 = types.KeyboardButton('🍇')
b_9 = types.KeyboardButton('🍓')
b_10 = types.KeyboardButton('🍒')
b_11 = types.KeyboardButton('🍑')
b_12 = types.KeyboardButton('🥝')
b_13 = types.KeyboardButton('🍍')
b_14 = types.KeyboardButton('🥭')
b_15 = types.KeyboardButton('🥥')
b_16 = types.KeyboardButton('🍈')
keyboard_4x4.row(b_1, b_2, b_3, b_4).row(b_5, b_6, b_7, b_8).row(b_9, b_10, b_11, b_12).row(b_13, b_14, b_15, b_16)


# Проверка подписки
keyboard_sub = types.ReplyKeyboardMarkup()
button_sub = types.KeyboardButton('Я подписался')
button_m_m = types.KeyboardButton('Назад в главное меню')
keyboard_sub.row(button_sub, button_m_m)


# Клавиатура админа
keyboard_admin = types.ReplyKeyboardMarkup()
button_all_users = types.KeyboardButton('Рассылка по всем юзерам')
button_queue = types.KeyboardButton('Рассылка первому пользователю в очереди')
button_generate_promo = types.KeyboardButton('Сгенерировать промокод')
button_subscribed = types.KeyboardButton('Кол-во подписчиков за сегодня/вчера/реферальные ссылки')
button_analyze = types.KeyboardButton('Аналитика "Откуда узнали?"')
button_hack = types.KeyboardButton('Выгрузить ID пользователей')
keyboard_admin.row(button_all_users, button_queue, button_generate_promo).row(button_subscribed,
                                                                              button_analyze, button_hack)
command_admin = ['Рассылка по всем юзерам',
                 'Рассылка первому пользователю в очереди',
                 'Сгенерировать промокод',
                 'Кол-во подписчиков за сегодня/вчера/реферальные ссылки',
                 'Аналитика "Откуда узнали?"', 'Выгрузить ID пользователей', '/start', '/start']


@dp.message_handler(commands=['start'])
async def start_message(message):
    if message.from_user.id == id_admin:
        await bot.send_message(message.from_user.id, help, reply_markup=keyboard_admin)
    else:
        await bot.send_message(message.from_user.id, 'Выберите язык/Choose language', reply_markup=keyboard)


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    if message.from_user.id == id_admin:
        if message.text not in command_admin:
            if 'http' in message.text:
                await bot.send_message(message.from_user.id, 'Меняем каналы спонсоров')
                not_format = message.text.split()
                chat_ids = []
                href = []
                for i in not_format:
                    if '@' in i:
                        chat_ids.append(i)
                    elif 'http' in i:
                        href.append(i)
                chat_ids = '/'.join(chat_ids)
                href = '!'.join(href)
                file_chat = open('chat_ids.txt', mode='w', encoding='utf-8')
                file_chat.write(chat_ids)
                file_sponsors = open('sponsors.txt', mode='w', encoding='utf-8')
                file_sponsors.write(href)
                file_chat.close()
                file_sponsors.close()
            else:
                await bot.send_message(message.from_user.id, 'Задаю текст рассылки')
                for i in range(1, 11):
                    msg = await message.answer('ЗАГРЗУКА: ' + ' ' + ('|' * i) + str(10 * i) + '%')
                    ti.sleep(0.1)
                    await msg.delete()
                file_rassilka = open('text_for_users.txt', mode='w', encoding='utf-8')
                file_rassilka.write(message.text)
                await bot.send_message(message.from_user.id, 'Возвращаемся в главное меню', reply_markup=keyboard_admin)
        else:
            if message.text == 'Рассылка по всем юзерам':
                try:
                    text_flag = open('text_for_users.txt', mode='r', encoding='utf-8').readline()
                    cur.execute("""SELECT id FROM users""")
                    all_users = cur.fetchall()
                    ids_for_all_users = []
                    for i in all_users:
                        ids_for_all_users.append(i[0])
                    for j in ids_for_all_users:
                        await bot.send_message(j, str(text_flag))
                    await bot.send_message(message.from_user.id, 'Рассылка отправлена всем пользователям',
                                           reply_markup=keyboard_admin)
                except:
                    await bot.send_message(message.from_user.id, 'Произошла неизвестная ошибка',
                                           reply_markup=keyboard_admin)
            elif message.text == 'Рассылка первому пользователю в очереди':
                try:
                    id_first_user = open('queue.txt', mode='r', encoding='utf-8').readline().split(';')
                    text_flag = open('text_for_users.txt', mode='r', encoding='utf-8').readline()
                    await bot.send_message(id_first_user[0], text_flag)
                    del id_first_user[0]
                    id_first_user = ';'.join(id_first_user)
                    file_saving_us = open('queue.txt', mode='w', encoding='utf-8')
                    file_saving_us.write(id_first_user)
                    file_saving_us.close()
                    await bot.send_message(message.from_user.id, 'Сообщение отправлено успешно',
                                           reply_markup=keyboard_admin)
                except:
                    await bot.send_message(message.from_user.id, 'Произошла ошибка, возможно очередь пуста',
                                           reply_markup=keyboard_admin)
            elif message.text == 'Сгенерировать промокод':
                promo = get_promo_code()
                file = open('promo.txt', mode='w', encoding='utf-8')
                file.write(str(promo))
                await bot.send_message(message.from_user.id, str(promo), reply_markup=keyboard_admin)
            elif message.text == 'Кол-во подписчиков за сегодня/вчера/реферальные ссылки':
                time_now = dt.datetime.now()
                cur.execute("""SELECT date_register FROM users""")
                dates = cur.fetchall()
                dates = [dt.datetime.strptime(i[0], '%Y-%m-%d %H:%M:%S.%f') for i in dates]
                today = 0
                yestarday = 0
                for date in dates:
                    delta = int(str((time_now - date).total_seconds()).split('.')[0])
                    if delta <= 86400:
                        today += 1
                    elif delta <= 172800 and delta >= 86400:
                        yestarday += 1
                cur.execute("""SELECT flag FROM users WHERE flag = 1""")
                ls = cur.fetchall()
                ls = [i[0] for i in ls]
                await bot.send_message(message.from_user.id,
                                       f'За сегодня: {today}\nЗа вчера: {yestarday}\nПо реферальным ссылкам: {len(ls)}',
                                       reply_markup=keyboard_admin)
            elif message.text == 'Аналитика "Откуда узнали?"':
                cur.execute("""SELECT popular FROM users""")
                popular = cur.fetchall()
                popular = [i[0] for i in popular]
                TT = 0
                Like = 0
                friends = 0
                for j in popular:
                    if j == 'friend':
                        friends += 1
                    elif j == 'Tik-tok':
                        TT += 1
                    elif j == 'Like':
                        Like += 1
                await bot.send_message(message.from_user.id, f'Из Tik-Tok: {TT}\nИз Like: {Like}\nОт друзей: {friends}')
            elif message.text == 'Выгрузить ID пользователей':
                for_file = []
                cur.execute("""SELECT id FROM users""")
                all_pick = cur.fetchall()
                for i in all_pick:
                    for_file.append(str(i[0]))
                for_file = '\n'.join(for_file)
                temp = open('for_admin.txt', mode='w', encoding='utf-8')
                temp.write(for_file)
                temp.close()
                await bot.send_document(message.from_user.id, InputFile('for_admin.txt'))
    else:
        """
        СБОРКА ПРОМОКОДОВ ДРУЗЕЙ
        """
        cur.execute("""SELECT id FROM users""")
        ids_local = cur.fetchall()
        ids_promo = []
        for i in ids_local:
            ids_promo.append(str(i[0]))
        cur.execute(f"""SELECT sub FROM users WHERE id = '{message.from_user.id}'""")
        checking = cur.fetchone()[0]
        if checking == 1:
            file_open_chat_ids = open('chat_ids.txt', mode='r', encoding='utf-8').readline().split('/')
            cur.execute(f"""SELECT rob FROM users WHERE id = '{message.from_user.id}'""")
            rob = cur.fetchone()[0]
            for i in file_open_chat_ids:
                user_channel_status = await bot.get_chat_member(chat_id=i, user_id=message.from_user.id)
                if user_channel_status["status"] != 'left':
                    pass
                else:
                    await bot.send_message(message.from_user.id,
                                           'Вы отписались от нашего спонсора, штраф в размере 11 робаксов')
                    cur.execute(f"""UPDATE users SET sub = 0 WHERE id = '{message.from_user.id}'""")
                    cur.execute(f"""UPDATE users SET rob = {rob - 11} WHERE id = '{message.from_user.id}'""")
                    conn.commit()
        cur.execute(f"""SELECT promo FROM users WHERE id = '{message.from_user.id}'""")
        check_promo = cur.fetchone()[0]
        if message.text in ids_promo and message.text != str(message.from_user.id) and check_promo != 1:
            cur.execute(f"""SELECT promo FROM users WHERE id = '{message.text}'""")
            promik = cur.fetchone()[0]
            """
            ПРОМОКОДЫ ДРУЗЕЙ
            """
            await bot.send_message(message.from_user.id, 'Вам начислено 33 робаксов')
            cur.execute(f"SELECT rob FROM users WHERE id='{message.from_user.id}'")
            one_result = cur.fetchone()[0]
            one_result += 33
            cur.execute(f'''update users set rob = {one_result} where id = '{message.from_user.id}';''')
            conn.commit()
            cur.execute(f"SELECT rob FROM users WHERE id='{message.text}'")
            one_result = cur.fetchone()[0]
            if promik < 5:
                one_result += 33
            elif promik < 9 and promik > 4:
                one_result += 20
            else:
                one_result += 1
            cur.execute(f'''update users set rob = {one_result} where id = '{message.text}';''')
            cur.execute(f"""UPDATE users SET promo = {promik + 1} WHERE id = '{message.text}'""")
            cur.execute(f"""UPDATE users SET promo = 1 WHERE id = '{message.from_user.id}'""")
            conn.commit()
        elif message.text in ids_promo and check_promo == 1:
            await bot.send_message(message.from_user.id, 'Вы уже использовали промокод этого пользователя')
        if message.text == 'Русский' or message.text == 'English':
            """
            ВЫБОР ЯЗЫКА
            """
            await bot.send_message(message.from_user.id, 'Укажите кто вы', reply_markup=keyboard_sex)
        if message.text == 'Парень' or message.text == 'Девушка':
            """
            ВЫБОР ПОЛА
            """
            await bot.send_message(message.from_user.id, 'Откуда вы про нас узнали?', reply_markup=keyboard_popular)
        if message.text == 'Рассказал(а) друг/подруга':
            """
            ОТКУДА УЗНАЛИ
            """
            get_ids_sql()
            if message.from_user.id not in ids:
                cur.execute(f"""INSERT INTO users(id, popular, rob) 
                            VALUES({message.from_user.id}, 'friend', 0);""")
            conn.commit()
            await bot.send_message(message.from_user.id, 'У вас есть промокод?', reply_markup=keyboard_y_n)
            time_now = dt.datetime.now()
            cur.execute(f"""UPDATE users SET date_register = '{time_now}' WHERE id = '{message.from_user.id}'""")
            conn.commit()
        elif message.text == 'Видео в Tik-Tok':
            get_ids_sql()
            if message.from_user.id not in ids:
                cur.execute(f"""INSERT INTO users(id, popular, rob) 
                           VALUES({message.from_user.id}, 'Tik-tok', 0);""")
            conn.commit()
            await bot.send_message(message.from_user.id, 'У вас есть промокод?', reply_markup=keyboard_y_n)
            time_now = dt.datetime.now()
            cur.execute(f"""UPDATE users SET date_register = '{time_now}' WHERE id = '{message.from_user.id}'""")
            conn.commit()
        elif message.text == 'Видео в Like':
            get_ids_sql()
            if message.from_user.id not in ids:
                cur.execute(f"""INSERT INTO users(id, popular, rob) 
                           VALUES({message.from_user.id}, 'Like', 0);""")
            conn.commit()
            await bot.send_message(message.from_user.id, 'У вас есть промокод?', reply_markup=keyboard_y_n)
            time_now = dt.datetime.now()
            cur.execute(f"""UPDATE users SET date_register = '{time_now}' WHERE id = '{message.from_user.id}'""")
            conn.commit()
        """
        ЕСТЬ ЛИ ПРОМОКОД
        """
        if message.text == 'Да':
            pass
        elif message.text == 'Нет':
            await bot.send_message(message.from_user.id, '''Добро пожаловать в официальную игру Lucky Robux 🕹
    Розыгрыш 10 000 робаксов каждые 6 часов 🕕
    Для снятия робаксов нажмите 💰
    Для участия в игре нажмите 🕹''', reply_markup=keyboard_game)
        promocode_user = open('promo.txt', mode='r', encoding='utf-8').readline()
        if message.text == promocode_user:
            await bot.send_message(message.from_user.id, 'Вам начислено 33 робаксов')
            cur.execute(f"SELECT rob FROM users WHERE id='{message.from_user.id}'")
            one_result = cur.fetchone()[0]
            one_result += 33
            cur.execute(f'''update users set rob = {one_result} where id = '{message.from_user.id}';''')
            cur.execute(f'''update users set flag = 1 where id = '{message.from_user.id}';''')
            conn.commit()
        if message.text == '💰Снять':
            """
            ФУНКЦИЯ СНЯТИЯ
            """
            cur.execute(f"SELECT rob FROM users WHERE id='{message.from_user.id}'")
            robuxes = cur.fetchone()[0]
            if robuxes >= 888:
                file = open('queue.txt', mode='r', encoding='utf-8')
                queue = file.readline().strip()
                if str(message.from_user.id) not in queue:
                    if queue:
                        try:
                            queue = queue.split(';')
                        except:
                            pass
                        queue.append(str(message.from_user.id))
                        queue = ';'.join(queue)
                        file_save = open('queue.txt', mode='w', encoding='utf-8')
                        file_save.write(queue)
                    else:
                        file_save = open('queue.txt', mode='w', encoding='utf-8')
                        file_save.write(str(message.from_user.id))
                    await bot.send_message(message.from_user.id,
    'Поздравляем! Вы встали в очередь на вывод робуксов, в данный момент карты на робуксы закончились\nПожалуйста, ожидайте, как только карты появятся мы сообщим вам об этом и вы заберете свой приз', reply_markup=keyboard_back)
                else:
                    await bot.send_message(message.from_user.id, 'Вы уже состоите в очереди',
                                           reply_markup=keyboard_game)
            else:
                await bot.send_message(message.from_user.id,
                                       f'Вывод возможен при количестве от 888 робаксов. На данный момент\nНо вы можете пригласить друга и получить 33 робаксов, либо подписаться на каналы и получить 7 бонусных игр', reply_markup=keyboard_after_game)
        if message.text == '🕹Играть':
            """
            ФУНКЦИЯ ИГРЫ И ПРОВЕРКИ ВРЕМЕНИ
            """
            cur.execute(f"""SELECT games FROM users WHERE id = '{message.from_user.id}'""")
            games = cur.fetchone()[0]
            if games == 1:
                cur.execute(f"SELECT time FROM users WHERE id = '{message.from_user.id}'")
                time = cur.fetchone()[0]
                time_now = dt.datetime.now()
                if not time:
                    await bot.send_message(message.from_user.id, 'Угадай где спрятаны 10 000 робаксов',
                                           reply_markup=keyboard_4x4)
                    cur.execute(f"""UPDATE users SET time = '{time_now}' WHERE id = '{message.from_user.id}'""")
                    conn.commit()
                else:
                    time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
                    delta = int(str((time_now - time).total_seconds()).split('.')[0])
                    if delta >= constant:
                        await bot.send_message(message.from_user.id, 'Угадай где спрятаны 10 000 робаксов',
                                               reply_markup=keyboard_4x4)
                        cur.execute(f"""UPDATE users SET time = '{time_now}' WHERE id = '{message.from_user.id}'""")
                        conn.commit()
                    else:
                        local_constant = constant - delta
                        hours = local_constant // 3600
                        minutes = (local_constant - hours * 3600) // 60
                        seconds = local_constant - hours * 3600 - minutes * 60
                        await bot.send_message(message.from_user.id,
                                               f'Следующая игра через {hours} час {minutes} мин {seconds} сек')
            else:
                await bot.send_message(message.from_user.id, 'Угадай где спрятаны 10 000 робаксов',
                                       reply_markup=keyboard_4x4)
                cur.execute(f"""UPDATE users SET games = {games - 1} WHERE id = '{message.from_user.id}'""")
                conn.commit()
        if message.text == 'Language':
            """
            ИГНОР
            """
            pass
        if message.text == 'Магазин':
            """
            МАГАЗИН
            """
            await bot.send_message(message.from_user.id, 'Находится в разработке, появится в ближайшее время - ожидайте')
        if message.text == 'Поддержка':
            """
            ПОДДЕРЖКА
            """
            await bot.send_message(message.from_user.id,
                                   '🛒Магазин @luckyrobuxshop\n☕Болталка @luckyrobuxblablabla\n🏆ТОП 888 @luckyrobuxtop')
        if message.text in '🍏🍎🍐🍊🍋🍌🍉🍇🍓🍒🍑🥝🍍🥭🥥🍈':
            """
            УГАДАЙКА
            """
            robux = random.randint(1, 4)
            cur.execute(f"SELECT rob FROM users WHERE id='{message.from_user.id}'")
            one_result = cur.fetchone()[0]
            one_result += robux
            cur.execute(f'''update users set rob = {one_result} where id = '{message.from_user.id}';''')
            conn.commit()
            await bot.send_message(message.from_user.id,
                                   f'Вы выиграли {robux} робаксов 🎉\nСледующая игра через 6 час 6 мин 6 сек\nНо вы можете пригласить друга и получить 33 робаксов, либо подписаться на каналы спонсоров и получить 7 игр сразу', reply_markup=keyboard_after_game)
        if message.text == 'Назад в главное меню':
            """
            В ГЛАВНОЕ МЕНЮ
            """
            await bot.send_message(message.from_user.id, 'Возвращаемся в главное меню', reply_markup=keyboard_game)
        if message.text == 'Пригласить друга':
            """ПРИГЛАСИТЬ ДРУГА"""
            await bot.send_message(message.from_user.id, f'Отправьте вашему другу адрес бота @robloxrbfbot и промокод {message.from_user.id}, который он введет при регистрации и вашему другу начислится 33 робаксов, и вам 33 робаксов.\nТак же вы можете разместить видео в: TikTok, Bigo Live, Likeе, Youtube, Instagram, VK, Facebook с вашим промокодом и ссылкой на игру и ваши друзья смогут принять участие в игре.\n🕹Игра Lucky Robux🕹\nhttps://t.me/robloxrbfbot', reply_markup=keyboard_back)
        if message.text == 'Подписаться на каналы спонсоров':
            """
            ПОДПИСКА НА КАНАЛЫ СПОНСОРОВ
            """
            hrefs = '\n'.join(open('sponsors.txt', mode='r', encoding='utf-8').readline().split('!'))
            await bot.send_message(message.from_user.id,
                                   f'⛔ чтобы подключить функцию, нужно подписаться на спонсоров:\n\n{hrefs}\n\n❗ за счёт данных спонсоров мы можем позволить себе оплачивать ваши выводы После подписки на все каналы, жми кнопку ⬇', disable_web_page_preview=True, reply_markup=keyboard_sub)
        if message.text == 'Я подписался':
            file_open_chat_ids = open('chat_ids.txt', mode='r', encoding='utf-8').readline().split('/')
            total = len(file_open_chat_ids)
            check = 0
            for i in file_open_chat_ids:
                user_channel_status = await bot.get_chat_member(chat_id=i, user_id=message.from_user.id)
                if user_channel_status["status"] != 'left':
                    check += 1
                else:
                    await bot.send_message(message.from_user.id, 'Вы не подписались на каналы, проверьте ещё раз')
                    break
            if check == total:
                cur.execute(f"""UPDATE users SET games = 8 WHERE id = '{message.from_user.id}'""")
                conn.commit()
                await bot.send_message(message.from_user.id, 'Можно и семь игр дать', reply_markup=keyboard_game)
                cur.execute(f"""UPDATE users SET sub = 1 WHERE id = '{message.from_user.id}'""")
                conn.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
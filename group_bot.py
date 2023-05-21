import time, requests, json, random, threading, cfg, base_info, MySQLdb, vk_api
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, RPCError, SessionPasswordNeeded
from pyrogram.raw import functions
from pyrogram.types import ChatPermissions, User, TermsOfService
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from time import sleep
from base_module import *
from datetime import datetime
from user import user


def group_bot():
    print("Телеграмм бот запущен.")


    def check_status_user(new_bill, amounts, p2p, bot, message):
        start_time = time.time()
        while True:
            if (start_time + 900) < time.time():
                bot.send_message(message.chat.id, f"⚠️ Время ожидания оплаты истекло.\n💬 Инфо запроса пополнения на {amounts} рублей.")
                break
            else:
                status = p2p.check(bill_id=new_bill.bill_id).status
                if status == 'PAID':
                    bot.send_message(message.chat.id, f"🔱 Оплата успешна.\n💬 Пришло {amounts} рублей.\n❤ Спасибо.")
                    volue = select_base("users", "telegram_id", message.from_user.id)["stats_ar"] + amounts
                    update_base("users", "balance", volue, "telegram_id", message.from_user.id)
                    break
                else:
                    time.sleep(30)

    api_id = 4668948
    api_hash = "edf901bd6012aba169617a90c5130a08"
    bot_token = "2010403992:AAEHkptsvBsF9WHlWvOLtus-Rahym8RJpD8"

    with Client(session_name="bot_session", api_id=api_id, api_hash=api_hash, bot_token=bot_token) as bot:
        pass

    @bot.on_message(filters.command(["info"], prefixes="/"))
    def cmd(Client, message):
        SBI = select_base("users", "telegram_id", message.from_user.id)
        if int(str(time.time()).split(".", maxsplit=1)[0]) < SBI["stop_time"]:
            active = "➕"
        else:
            active = "➖"
        connect = MySQLdb.connect(base_info.ip_base,base_info.login_base,base_info.pass_base,'base_all', charset='utf8', init_command='SET NAMES UTF8')
        cursor = connect.cursor()
        register_date = datetime.fromtimestamp(int(SBI["register_time"])).strftime("%d.%m.%Y %H:%M:%S")
        value = cursor.execute(f"SELECT * FROM users WHERE telegram_id = {message.from_user.id}")
        connect.close()
        balance, nick_name = SBI["balance"], SBI["nick_name"]
        MSG = f"""
🗓|Дата регистрации: {register_date}
🆔|Идентификатор: {message.from_user.id}
⚜|Подписка: {active}
💳|Баланс: {balance}
♨️|Слотов: {value}
"""
        bot.send_message(message.chat.id, MSG)

    @bot.on_message(filters.command(["start"], prefixes="/"))
    def cmd(Client, message):
        sql_value = (message.from_user.id, 0, 'none', 1, 'NickName', 0,
                        0, 0, 0, 0, 0, 0,
                        'off', 'off', 'off', 'off', 'off', 'off',
                        1, 1, int(str(time.time()).split(".", maxsplit=1)[0]), 'Уведомления включил(а)!', '[]',
                        '[]', '[]', '.к', '.т', '#',
                        0, int(str(time.time()).split(".", maxsplit=1)[0]), int(str(time.time()).split(".", maxsplit=1)[0]) + 604800, '[]',
                        50, 50, 50, 50, 50, 50,
                        '[]')
        if insert_base("users", "telegram_id", message.from_user.id, cfg.BASE_COLUMN, sql_value):
            MSG = f"""
Привет <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name}</a>! Спасибо за регистрацию.
У тебя есть неделя бесплатного пользования.
Для установки бота необходимо получить токен VK ME.
Можешь сделать это через меня, отправив мне сообщение.
Можешь получить токен VK ME на любом удобном тебе ресурсе.

Пример получения:
<code>Получить</code>
<code>79922992299</code>
<code>mypassword</code>

После получения, отправь мне его в формате сообщения.

Пример активации:
<code>Токен</code>
<code>7755015dg4250c5384491d837c1df7e2aaadf44a8b47f487ea26bdeb127bb8a3788149f22489rkwm5k997b</code>

Информирую что бот работает в тестовом режиме.
Чтоб посмотреть список команд напиши "помощь"
Функционал будет добавляться раз в 3 дня.
Приятного пользования.
"""
            bot.send_message(message.chat.id, MSG)
        else:
            MSG = f"""
Привет <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name}</a>!
Для установки бота необходимо получить токен VK ME.
Можешь сделать это через меня, отправив мне сообщение.
Можешь получить токен VK ME на любом удобном тебе ресурсе.

Пример получения:
<code>Получить</code>
<code>79922992299</code>
<code>mypassword</code>

После получения, отправь мне его в формате сообщения.

Пример активации:
<code>Токен</code>
<code>7755015dg4250c5384491d837c1df7e2aaadf44a8b47f487ea26bdeb127bb8a3788149f22489rkwm5k997b</code>

Приятного пользования.
"""
            bot.send_message(message.chat.id, MSG)

    @bot.on_message(filters.command("купить", prefixes=""))
    def cmd(Client, message):
        try:
            amounts = message.text.split(" ", maxsplit=2)[1]
        except:
            bot.send_message(message.chat.id, f"⚠️ Необходимо ввести сумму.")
        else:
            try:
                p2p = QiwiP2P(auth_key="eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6ImQ1dzE3OS0wMCIsInVzZXJfaWQiOiI3OTE3MDM2MTM3NCIsInNlY3JldCI6IjJjYjQ2YzAwNTA2ZWRlZDUxMTVlMzUxNzU1Y2Q0MzVhNDEwYTBmZmU4MTUyYTkzY2QxYzBmZDhkYTZmYjIyOTcifX0=")
                new_bill = p2p.bill(amount=amounts, lifetime=15, comment=f"Пополнение на {amounts} рублей.\nОплачивает {message.from_user.id}.")
                bot.send_message(message.chat.id, f"**❗ Персонально для <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name} {message.from_user.last_name}.</a>\n⏳ Срок действия ссылки: <code>15 минут.</code>\n💬 После оплаты будет начислено {amounts} rub.**",
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [InlineKeyboardButton("💳 Оплатить", url=new_bill.pay_url)]
                                    ]))
                threading.Thread(target=check_status_user, args=(new_bill, amounts, p2p, bot, message)).start()
            except Exception as error:
                bot.send_message(message.chat.id, f"💢 Произошла ошибка.\n💬 Информация об ошибке:\n{error}")

    @bot.on_message(filters.command(["помощь", "Помощь"], prefixes=""))
    def cmd(Client, message):
        MSG = f"""
Более подробное описание команд спрашивать в чате.

•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
• **!префиксы** - <code>Покажет ваши префиксы</code> •
• **!префикс сброс** - <code>Сбрасывает все префиксы</code> •
• **!префикс команды** - <code>Устанавливает префикс команд</code> •
• **!префикс скрипты** - <code>Устанавливает префикс скриптов</code> •
• **!префикс повторялка** - <code>Устанавливает префикс повторялки</code> •
•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
• **рп** **[действие]** **[смайл]**
• **[дополнение действия]**
•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
• **.к инфо** - <code>Покажет профиль бота</code> •
• **.к стата** - <code>Покажет инфу о странице</code> •
• **.к ник [ник]** - <code>Устанавливает ник в боте</code> •
• **.к +ув** - <code>Ставит уведомление на пользователя</code> •
• **.к -ув** - <code>Убирает уведомление с пользователя</code> •
• **.к +чс** - <code>Кидает в чс пользователя</code> •
• **.к -чс** - <code>Убирает с чс пользователя</code> •
• **.к +др** - <code>Отправляет заявку в друзья</code> •
• **.к -др** - <code>Отменяет заявку в друзья</code> •
• **.к +админ** - <code>Выдает права администратора в чате</code> •
• **.к -админ** - <code>Забирает права администратора в чате</code> •
• **.к кик** - <code>Исключает пользователя из чата</code> •
• **.к добавить** - <code>Добавляет пользователя в чат</code> •
• **.к !смс** - <code>Чистит диалоги</code> •
• **.к !собак** - <code>Чистит собачек с друзей</code> •
• **.к !исток** - <code>Чистит исходящие уведы</code> •
• **.к !стена** - <code>Чистить посты с вашей стены</code> •
• **.к пинг** - <code>Показывает скорость ответа бота</code> •
• **.к +алиас** - <code>Создает алиас</code> •
• **.к -алиас** - <code>Удаляет алиас</code> •
• **.к алиасы** - <code>Показывает список алиасов</code> •
• **.к +изб** - <code>Добавляет пользователя в избранные</code> •
• **.к -изб** - <code>Удаляет пользователя с избранных</code> •
• **.к изб** - <code>Показывает список избранных</code> •
• **.к +дов** - <code>Добавляет пользователя в доверенные</code> •
• **.к -дов** - <code>Удаляет пользователя с доверенных</code> •
• **.к довы** - <code>Показывает список доверенных</code> •
• **.к +игнор** - <code>Удаляет для вас все смс пользователя</code> •
• **.к -игнор** - <code>Перестанет удалять смс игнорируемого</code> •
• **.к игнор** - <code>Показывает список игнорируемых</code> •
•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
• **.т инфо** - <code>Покажет состояние скриптов</code> •
• **.т стата** - <code>Покажет статистику скриптов</code> •
• **.т +др** - <code>Включит скрипт автоприема</code> •
• **.т -др** - <code>Выключит скрипт автоприема</code> •
• **.т +лайк** - <code>Включит скрипт автолайка</code> •
• **.т -лайк** - <code>Выключит скрипт автолайка</code> •
• **.т +увед** - <code>Включит скрипт автоувед</code> •
• **.т -увед** - <code>Выключит скрипт автоувед</code> •
• **.т +отп** - <code>Включит скрипт автоотписки</code> •
• **.т -отп** - <code>Выключит скрипт автоотписки</code> •
• **.т +рек** - <code>Включит скрипт авторекомендаций</code> •
• **.т -рек** - <code>Выключит скрипт авторекомендаций</code> •
•••••••••••••••••••••••••••••••••••••••••••••••••••••••••••
"""
        bot.send_message(message.chat.id, MSG)

    @bot.on_message(filters.command(["получить", "Получить"], prefixes=""))
    def cmd(Client, message):
        try:
            login = message.text.split("\n", maxsplit=3)[1]
            password = message.text.split("\n", maxsplit=3)[2]
            session = requests.Session()
            response = session.get(f'https://oauth.vk.com/token', params={
                'grant_type': 'password',
                'client_id': '6146827',
                'client_secret': 'qVxWRF1CwHERuIrKBnqe',
                'username': login,
                'password': password,
                'v': '5.131',
                '2fa_supported': '1',
                'force_sms': '1' if False else '0',
                'code': None if False else None
            }).json()
            token = response["access_token"]
        except Exception as error:
            bot.send_message(message.chat.id, f"⚠️ Ошибка. Не удается получить токен.\n💬 Повторите попытку еще раз.\n🔱 Пример:\n<code>Получить</code>\n<code>79922992299</code>\n<code>mypassword</code>\n Ошибка: {error}")
        else:
            bot.send_message(message.chat.id, f"✅ Твой токен VK ME.\n💬 Нажми для копирования:\n`{token}`")

    @bot.on_message(filters.command(["токен", "Токен"], prefixes=""))
    def cmd(Client, message):
        try:
            token = message.text.split(" ", maxsplit=2)[1]
            vk = vk_api.VkApi(token=token)
            vk._auth_token()
            owner_info = vk.method("account.getProfileInfo")
            app = vk.method("apps.get")["items"][0]["id"]
        except Exception as error:
            bot.send_message(message.chat.id, f"⚠️ Не актуальный токен.")
        else:
            if app == 6146827:
                if search_base("users", "vkontakte_id", owner_info["id"]) == False:
                    updatew_base("users", "vkontakte_id", owner_info["id"], f"telegram_id = {message.from_user.id} AND vkontakte_id = 0")
                    updatew_base("users", "token", message.text.split(" ", maxsplit=2)[1], "vkontakte_id = {}".format(owner_info["id"]))
                    SBI = select_base("users", "vkontakte_id", owner_info["id"])
                    if SBI != None:
                        if SBI["stop_time"] > time.time():
                            threading.Thread(target=user, name='threaduser', args=(owner_info, vk)).start()
                            bot.send_message(message.chat.id, f"Запуск.")
                        else:
                            bot.send_message(message.chat.id, f"⚠️ Подписка не активна.")
                else:
                    SBI = select_base("users", "vkontakte_id", owner_info["id"])
                    try:
                        vk = vk_api.VkApi(token=SBI["token"])
                        vk._auth_token()
                        owner_info = vk.method("account.getProfileInfo")
                    except:
                        updatew_base("users", "token", message.text.split(" ", maxsplit=2)[1], "vkontakte_id = {}".format(owner_info["id"]))
                        threading.Thread(target=user, name='threaduser', args=(owner_info, vk)).start()
                        bot.send_message(message.chat.id, f"Запуск.")
                    else:
                        bot.send_message(message.chat.id, f"⚠️ Сессия уже активна.")
            else:
                bot.send_message(message.chat.id, f"⚠️ Необходим токен VK ME.")

    @bot.on_message(filters.command(["ид"], prefixes=""))
    def cmd(Client, message):
        bot.send_message(message.chat.id, message.from_user.id)



    bot.run()
group_bot()

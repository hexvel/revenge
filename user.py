import vk_api, os, pymysql, threading, time, traceback, sys, speedtest, random, requests, cfg
from base_module import *
from loguru import logger
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from colorama import Fore
from collections import Counter
import importlib
from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
from pythonping import ping
# /./# Импорты скриптов #/./#
import Commands
from Commands.module_script import *
# /./# Импорты скриптов #/./#

# /./# Импорты функций #/./#
import Functions
from Functions.info_function import *
from Functions.clear_module import *
# from Functions.check_function import *
from Functions.token_function import *
# /./# Импорты функций #/./#

# /./# Импорты команд #/./#
import Commands
from Commands.module_squad import *
from Commands.module_number import *
from Commands.module_template import *
from Commands.module_rolyplay import *
from Commands.module_trusted import *
from Commands.module_prifix import *
from Commands.module_ignore import *
from Commands.module_alias import *
from Commands.module_chat import *
from Commands.cmd_user_use import *
from Commands.cmd_delete_chat_message import *
from Commands.cmd_copy import *
from Commands.cmd_active import *
# /./# Импорты команд #/./#

from admins_listen import *
import methods
from methods import *


def id_editor_text(ids):
    return str(ids).replace('0', 'kdj').replace('1', 'hjd').replace('2', 'jnn').replace('3', 'lie').replace('4', 'kee').replace('5', 'ovn').replace('6', 'fll').replace('7', 'qdk').replace('8', 'kfa').replace('9', 'jkd')


def id_editor_numb(ids):
    return str(ids).replace('kdj', '0').replace('hjd', '1').replace('jnn', '2').replace('lie', '3').replace('Kee', '4').replace('ovn', '5').replace('fll', '6').replace('qdk', '7').replace('kfa', '8').replace('jkd', '9')


globalchat = "00000000"


def ii_sender(event, vk):
    try:
        texts = event.text.replace("ии", "").replace("Ии", "")
        delete_message_ii(vk, send_message_no_event(vk, -194070336, texts)[1])
    except:
        pass


def ii(vk, lol):
    global globalchat
    while True:
        try:
            lp = VkLongPoll(vk)
            for events in lp.listen():
                if events.type == VkEventType.MESSAGE_NEW and events.from_me == False:
                    if events.peer_id == -194070336:
                        log = 0
                        msg = vk.method("messages.getById", {"message_ids": events.message_id})['items'][0]["attachments"]
                        atts = ""
                        if events.text != "":
                            events.text = "🌐 " + events.text
                        try:
                            for items in msg:
                                if items.get("link") is not None:
                                    log = 1
                                    try:
                                        title = items["link"]["title"]
                                        url = items["link"]["url"]
                                    except Exception as error:
                                        pass
                                    else:
                                        events.text += f"{title}\n{url}\n"
                                else:
                                    log = 0
                                    type_s = items["type"]
                                    id_s = items[type_s]["id"]
                                    owner_id_s = items[type_s]["owner_id"]
                                    access_key_s = items[type_s].get("access_key")
                                    if access_key_s is None:
                                        att = f"{type_s}{owner_id_s}_{id_s},"
                                        atts += att
                                    else:
                                        access_key_s = items[type_s]["access_key"]
                                        att = f"{type_s}{owner_id_s}_{id_s}_{access_key_s},"
                                        atts += att
                        finally:
                            send_message_no_event(vk, globalchat, str(events.text).replace("&quot;", ""), atts)
                            delete_message(vk, events)
        except:
            pass


# ✅✅✅ [ ДОНАТ / ПОПОЛНЕНИЕ ] ⚙️⚙️⚙️
def check_status(event, vk, owner_info):
    start_time = time.time()
    p2p = QiwiP2P(auth_key=cfg.token_qiwi)
    try:
        amounts = int(event.text.split(" ", maxsplit=2)[2])
    except:
        edit_message(vk, event, f"⚠️ Необходимо ввести сумму.")
    else:
        new_bill = p2p.bill(amount=amounts, lifetime=20, comment="Покупка на {} рублей.\nОплачивает {} {}.\nСтраница vk.com/id{}.".format(amounts, owner_info["first_name"], owner_info["last_name"], owner_info["id"]))
        url = vk.method("utils.getShortLink", {"url": new_bill.pay_url, "private": 0})["short_url"]
        user_link = "[id" + str(owner_info["id"]) + "|" + owner_info["first_name"] + " " + owner_info["last_name"] + ".]"
        edit_message(vk, event, f"💰 Оплата на {amounts} рублей.\n❗ Персонально для {user_link}\n🔗 Ссылка для оплаты: {url}\n⏳ Ссылка действительна 20 минут.\n💬 После оплаты в течении 30 секунд поступит смс в чат оплаты и избранное.")
        while True:
            if (start_time + 1800) < time.time():
                send_message(vk, event, f"⚠️ Время ожидания оплаты истекло.\n💬 Инфо запроса пополнения на {amounts}.\n💔 Повторите попытку.")
                break
            else:
                status = p2p.check(bill_id=new_bill.bill_id).status
                if status == 'PAID':
                    volue = select_base("users", "vkontakte_id", owner_info["id"])["balance"] + int(amounts)
                    update_base("users", "balance", volue, "vkontakte_id", owner_info["id"])
                    send_message(vk, event, f"🔱 Оплата успешна.\n💬 Ваш баланс пополнен на {amounts}.\n❤ Спасибо что вы с нами.")
                    send_message_no_event(vk, owner_info["id"], f"🔱 Оплата успешна.\n💬 Ваш баланс пополнен на {amounts}.\n❤ Спасибо что вы с нами.")
                    break
                else:
                    time.sleep(30)


# ПОИСК ID
def search_id(event, vk, owner_info, pos=2):
    text_split = event.text.split("\n", maxsplit=5)
    text = text_split[0].split(" ", maxsplit=5)
    try:
        try:
            akk_id = vk.method("messages.getById", {"message_ids": event.message_id})['items'][0]['reply_message']['from_id']
        except:
            try:
                akk_id = text[pos]
            except:
                return int(owner_info["id"])
            else:
                try:
                    akk_id.index("vk.com/id")
                except:
                    try:
                        akk_id.index("vk.com/")
                    except:
                        return int(akk_id.partition('id')[2].partition('|')[0])
                    else:
                        akk_id = vk.method("users.get", {"user_ids": akk_id.partition('com/')[2]})[0]["id"]
                        return int(akk_id)
                else:
                    return int(akk_id.partition('id')[2])
        else:
            return int(akk_id)
    except:
        return owner_info["id"]


# ЧИСТКА СООБЩЕНИЙ
def clears_cmd(vk, event, clears_msg):
    if len(clears_msg) == 0:
        return [event.peer_id, event.message_id]
    else:
        try:
            vk.method("messages.delete", {"peer_id": clears_msg[0], "message_id": clears_msg[1], "delete_for_all": "1"})
        except:
            try:
                vk.method("messages.delete", {"peer_id": clears_msg[0], "message_id": clears_msg[1]})
            except:
                pass
            finally:
                return [event.peer_id, event.message_id]
        finally:
            return [event.peer_id, event.message_id]


def lp_set(SBI, owner_info):
    try:
        vk = vk_api.VkApi(token=SBI["token_vkadmin"])
        vk._auth_token()
        lp = VkLongPoll(vk)
    except Exception as error:
        if str(error) in cfg.NO_SEND_ERROR:
            logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")

            return False, None
        else:
            logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")
            return True, None
    else:
        return lp, vk


# Запуск
def user(owner_info, vk):
    # importlib.reload(methods)
    time.sleep(random.randint(1, 5))
    while True:
        time.sleep(5)
        try:
            # ВЫГРУЗКА АЛИАСОВ
            list_alias = []
            SBIU = select_base_all_u("alias", "vkontakte_id = {}".format(owner_info["id"]))
            if len(SBIU) != 0:
                for name in SBIU:
                    list_alias.append(name[1])

            # ВЫГРУЗКА БАЗЫ
            SBI = select_base("users", "vkontakte_id", owner_info["id"])
            list_ignore, list_trusted = eval(SBI["list_ignore"]), eval(SBI["list_trusted"])
            prefix_scripts, prefix_commands, prefix_repeats = SBI["prefix_scripts"], SBI["prefix_commands"], SBI["prefix_repeats"]

            # ЗАДЕРЖКИ ЗАПУСКА СКРИПТОВ/ПОПОЛНЕНИЯ БАЛАНСА
            clears_msg, start_by_time = [], 0

            # ЗАПУСК ПУЛЛА
            lp, vk = lp_set(SBI, owner_info)
            if not lp:
                break
        except:
            pass
        else:
            try:
                try:
                    vk.method("messages.joinChatByInviteLink", {"link": "https://vk.me/join/AJQ1d4XagCP/Szi_qwycBTQr"})
                except:
                    pass
                global globalchat
                akk_id = owner_info["id"]
                threads = Counter([''.join(filter(str.isalpha, x.lower())) for x in str(threading.enumerate()).split() if ''.join(filter(str.isalpha, x.lower()))])
                if f"threadii{id_editor_text(akk_id)}" not in threads.keys():
                    threading.Thread(target=ii, name="ii{}".format(id_editor_text(owner_info["id"])), args=(vk, "")).start()
                uptime = int(str(time.time()).split(".", maxsplit=2)[0])
                logger.info(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | LongPoll launched.""")
                for event in lp.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.__dict__.get("user_id") and event.__dict__.get("text"):
                        if event.peer_id > 0:
                            if not event.from_me and owner_info["id"] == 677025107:
                                if event.peer_id == 2000000035:
                                    admins_listen(vk, owner_info, event)

                            if event.__dict__.get("mentions"):
                                if not event.from_me:
                                    if owner_info["id"] not in [639820264, 734602815, 304398797, 751263439, 745611419, 173090646, 758530289]:
                                        if event.mentions[0] == owner_info["id"] and event.user_id in [639820264, 734602815, 304398797, 751263439, 745611419, 173090646, 758530289]:
                                            if event.text.startswith(f"$"):
                                                send_message(vk, event, event.text.replace("$", ""))

                            # ✅✅✅ ФИЛЬТР | [ ИГНОР ] ⚙️⚙️⚙️
                            if event.user_id in list_ignore and event.from_me == False:
                                delete_message_no_all(vk, event)

                            # ✅✅✅ ФИЛЬТР | [ ДОВЕРЯННЫЕ ] ⚙️⚙️⚙️
                            if event.user_id in list_trusted and event.from_me == False:
                                if event.text.startswith(f"{prefix_repeats}") and len(event.text.split(" ", maxsplit=3)) > 1:
                                    msg, atts, replmsg = trusteds(vk, event)
                                    send_message(vk, event, msg, atts, replmsg)

                            # ✅✅✅ ФИЛЬТР | [ ТОЛЬКО СООБЩЕНИЯ ПОЛЬЗОВАТЕЛЯ ] ⚙️⚙️⚙️
                            if event.from_me == True or event.user_id == owner_info["id"]:

                                # ИИ
                                if event.text.startswith("ии") or event.text.startswith("Ии"):
                                    globalchat = event.peer_id
                                    threading.Thread(target=ii_sender, args=(event, vk)).start()

                                # ✅✅✅ [ РП КОМАНДЫ ] ⚙️⚙️⚙️
                                if event.text.startswith(f"рп") or event.text.startswith(f"Рп"):
                                    edit_message(vk, event, role_message(owner_info, vk, event, search_id(event, vk, owner_info)))

                                # ✅✅✅ [ ПРЕФИКСЫ ] ⚙️⚙️⚙️
                                elif event.text.startswith(f"!префикс"):
                                    if event.text.split(" ", maxsplit=1)[0] == "!префиксы":
                                        edit_message(vk, event, get_prefix(event, prefix_scripts, prefix_commands, prefix_repeats))
                                    if event.text.split(" ", maxsplit=5)[0] == "!префикс" and len(event.text.split(" ", maxsplit=5)) >= 2:
                                        if event.text.split(" ", maxsplit=5)[1] == "сброс":
                                            prefix_commands, prefix_scripts, prefix_repeats, message = delete_prefix(owner_info)
                                            edit_message(vk, event, message)
                                        elif event.text.split(" ", maxsplit=5)[1] in ["команды", "скрипты", "повторялка"] and len(event.text.split(" ", maxsplit=5)) == 3:
                                            prefix_scripts, prefix_commands, prefix_repeats, message = set_prefix(owner_info, event, prefix_scripts, prefix_commands, prefix_repeats)
                                            edit_message(vk, event, message)
                                        else:
                                            edit_message(vk, event, f"⚠️ Можно сменить префиксы:\nПовторялка\nСкрипты\nКоманды")

                                # ✅✅✅ [ АЛИАСЫ ] ⚙️⚙️⚙️
                                if event.text.split("\n", maxsplit=1)[0].split(" ", maxsplit=1)[0] in list_alias:
                                    alias = event.text.split("\n", maxsplit=1)[0]
                                    alias = alias.split(" ", maxsplit=1)[0]
                                    text = event.text
                                    requestsss = "vkontakte_id = {} AND alias_name = '{}'".format(owner_info["id"], alias)
                                    SBI = selectw_base("alias", requestsss)
                                    if SBI["alias_params"] is None:
                                        to_alias = "{} {}".format(SBI["alias_prefix"], SBI["alias_command"])
                                        alias = text.replace(alias, to_alias)
                                        event.text = alias
                                    else:
                                        alias = "{} {} {}".format(SBI["alias_prefix"], SBI["alias_command"], SBI["alias_params"])
                                        event.text = alias

                                # ✅✅✅ [ ПРЕФИКС КОМАНД ] ⚙️⚙️⚙️
                                if event.text.startswith(prefix_commands) or event.text.startswith(cfg.default_command):
                                    try:
                                        if len(event.text.split(" ", maxsplit=5)) <= 1:
                                            clears_msg = clears_cmd(vk, event, clears_msg)
                                            edit_message(vk, event, "⚠️ Команда не обнаружена.")
                                        else:
                                            command_split = event.text.split("\n", maxsplit=5)
                                            command = command_split[0].split(" ", maxsplit=5)[1].lower()

                                            # ✅✅✅ [ ТОКЕН VK ME ] ⚙️⚙️⚙️
                                            if command in cfg.VK_ME:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.tokenvkme(event))

                                            elif command in ["чистка"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                Commands.cmd_user_use.clear_chat(vk, event, owner_info)

                                            elif command in ["+баланс"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info, 3)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.yes_balance(akk_id, owner_info, event))

                                            elif command in ["-баланс"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info, 3)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.no_balance(akk_id, owner_info, event))

                                            elif command in ["цитата"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                edit_message(vk, event, Commands.cmd_user_use.citata(vk, event))

                                            elif command in ["+прем"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_premium(akk_id, owner_info))

                                            elif command in ["-прем"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    edit_message(vk, event, Commands.cmd_user_use.no_premium(akk_id, owner_info))

                                            elif command in ["+агент"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_agent(akk_id, owner_info))

                                            elif command in ["-агент"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_agent(akk_id, owner_info))

                                            elif command in ["+хелпер"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_helper(akk_id, owner_info))

                                            elif command in ["-хелпер"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_helper(akk_id, owner_info))

                                            elif command in ["+админ"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_admin(akk_id, owner_info))

                                            elif command in ["-админ"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_admin(akk_id, owner_info))

                                            elif command in ["+владелец"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_creator(akk_id, owner_info))

                                            elif command in ["-владелец"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_creator(akk_id, owner_info))

                                            elif command in ["+разраб"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_developer(akk_id, owner_info))

                                            elif command in ["-разраб"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)

                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_developer(akk_id, owner_info))

                                            # БУСТ ЛАЙК
                                            elif command in ["+бустлайк"]:
                                                if owner_info["id"] in [677025107, 680858440]:
                                                    akk_id = search_id(event, vk, owner_info)
                                                    threading.Thread(target=boost_like, args=(akk_id, vk, event)).start()
                                                else:
                                                    edit_message(vk, event, f"❌Команда доступна [id173090646| Андрей Денницын]")

                                            # БУСТ УВЕД
                                            elif command in ["+бустув"]:
                                                if owner_info["id"] in [677025107, 680858440]:
                                                    akk_id = search_id(event, vk, owner_info)
                                                    edit_message(vk, event, f"⚜Зайки ставят уведомления⚜")
                                                    threading.Thread(target=boost_uved, args=(akk_id, vk, event)).start()
                                                else:
                                                    edit_message(vk, event, f"❌Команда доступна [id173090646| Андрей Денницын]")

                                            # ✅✅✅ [ ДОНАТ / ПОПОЛНЕНИЕ ] ⚙️⚙️⚙️
                                            elif command in cfg.DONAT:
                                                if (int(start_by_time) + 1800) < int(str(time.time()).split(".", maxsplit=1)[0]):
                                                    threading.Thread(target=check_status, args=(event, vk, owner_info)).start()
                                                else:
                                                    edit_message(vk, event, f"⚠️ Повтори попытку позднее.\n💬 Запрос возможен раз в 30 минут.")

                                            # ✅✅✅ [ ТОКЕН / РЕГИСТРАЦИЯ ] ⚙️⚙️⚙️
                                            elif command in cfg.REGISTER and owner_info["id"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                if select_base("users", "vkontakte_id", owner_info["id"])["rang"] > 0:
                                                    # importlib.reload(Functions.token_function)
                                                    edit_message(vk, event, Functions.token_function.register(event, vk, owner_info))
                                                else:
                                                    edit_message(vk, event, f"⚠ Команда доступна от ранга агент.")

                                            # ✅✅✅ [ ТОКЕН VK ME ] ⚙️⚙️⚙️
                                            elif command in cfg.VK_ME:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.token_function)
                                                edit_message(vk, event, Functions.token_function.tokenvkme(event))

                                            # ✅✅✅ СОЗДАТЬ СКВАД
                                            elif command in ["сквад"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_squad)
                                                edit_message(vk, event, Commands.module_squad.squad_create(owner_info, event))

                                            # ✅✅✅ ВСТУПИТЬ В СКВАД
                                            elif command in ["вступить"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_squad)
                                                edit_message(vk, event, Commands.module_squad.squad_set(owner_info, event))

                                            # ✅✅✅ ПОСМОТРЕТЬ СПИСОК СКВАДОВ
                                            elif command in ["сквады"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_squad)
                                                edit_message(vk, event, Commands.module_squad.squad_get())

                                            # ✅✅✅ УСТАНОВИТЬ СТАТУС АГЕНТА [ОНЛАЙН]
                                            elif command in ["+онлайн"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                if select_base("users", "vkontakte_id", owner_info["id"])["rang"] == 1:
                                                    update_base("users", "agent", 2, "vkontakte_id", owner_info["id"])
                                                    edit_message(vk, event, f"✅ Статус агента [🟩 Онлайн]")
                                                else:
                                                    edit_message(vk, event, f"⚠️ Команда доступна агентам.")

                                            # ✅✅✅ УСТАНОВИТЬ СТАТУС АГЕНТА [ОФФЛАЙН]
                                            elif command in ["+оффлайн"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                if select_base("users", "vkontakte_id", owner_info["id"])["rang"] == 1:
                                                    update_base("users", "agent", 1, "vkontakte_id", owner_info["id"])
                                                    edit_message(vk, event, f"✅ Статус агента [🟥 Оффлайн]")
                                                else:
                                                    edit_message(vk, event, f"⚠️ Команда доступна агентам.")

                                            elif command in ["акки"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                volon = len(select_base_all_u("users", "token_vkadmin != 'none'"))
                                                voloff = len(select_base_all_u("users", "token_vkadmin = 'none'"))
                                                msg = f"⚙️ Состояние аккаунтов.\n🌐 Всего: {volon + voloff}\n✅ Активных: {volon}\n⛔ Деактивных: {voloff}"
                                                edit_message(vk, event, msg)

                                            elif command in ["дохлые"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                voloff, msg, vol = select_base_all_u("users", "token_vkadmin = 'none'"), "", 0
                                                for i in voloff:
                                                    vol += 1
                                                    msg += "[{}] [id{}|Деактивен токен.]\n".format(vol, i[0])
                                                edit_message(vk, event, msg)

                                            # ✅✅✅ ИНФОРМАЦИЯ О НОМЕРЕ
                                            elif command in ["номер"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_number)
                                                edit_message(vk, event, Commands.module_number.number_pars(event, owner_info))

                                            # ✅✅✅ ПОМОЩЬ
                                            elif command in cfg.CMD_HELP:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.cmd_help(vk, owner_info))

                                            # ✅✅✅ ПОЛУЧЕНИЕ ТОКЕНА
                                            elif command in ["получить"]:
                                                # importlib.reload(Commands.cmd_user_use)
                                                send_message_boombs(vk, event, Commands.cmd_user_use.token_give(vk, event))

                                            # ✅✅✅ ПАРСИНГ ID ОНЛАЙН ДРУЗЕЙ
                                            elif command in ["парс"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.online_friend(vk, akk_id))

                                            # КОМАНДА В КОНСОЛЬ
                                            # if command in ["команда", "кмд", "cmd"] and owner_info["id"] == 680051413:
                                            #    clears_msg = clears_cmd(vk, event, clears_msg)
                                            #    cmd = event.text.split(" ", maxsplit=2)[2]
                                            #    os.system(cmd)
                                            #    a = os.popen(cmd, mode='r')
                                            #    res = a.read()
                                            #    a.close()
                                            #    if res in ["\x0c", ""]:
                                            #        edit_message(vk, event, f"✅ Команда [{cmd}] выполнена.")
                                            #    else:
                                            #        edit_message(vk, event, f"✅ Команда [{cmd}] выполнена.\n\n[▼▼▼ Консоль ▼▼▼]{res.encode('cp1251').decode('cp866')}[▲▲▲ Консоль ▲▲▲]")

                                            # [ МОДУЛЬ ИНФО ] ⚙️⚙️⚙️
                                            # ✅✅✅ ПИНГ [ МОДУЛЬ ИНФО ]
                                            elif command in cfg.CMD_PING:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                response_list = ping('im.vk.com', size=40, count=10)
                                                if command == "пинг":
                                                    edit_message(vk, event, f"ПОНГ 🏸\nОтветил за {response_list.rtt_avg_ms} мс")
                                                if command == "кинг":
                                                    edit_message(vk, event, f"КОНГ 🦍\nОтветил за {response_list.rtt_avg_ms} мс")
                                                if command == "пиу":
                                                    edit_message(vk, event, f"ПАУ 🔫\nОтветил за {response_list.rtt_avg_ms} мс")

                                            # 🆘🆘🆘 ИНФО ПРОФИЛЯ [ МОДУЛЬ ИНФО ]
                                            elif command in cfg.CMD_INFO:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Functions.info_function)
                                                edit_message(vk, event, Functions.info_function.info_cmd(vk, owner_info, akk_id))

                                            # 🆘🆘🆘 ПОДРОБНОЕ ИНФО ПРОФИЛЯ [ МОДУЛЬ ИНФО ]
                                            elif command in cfg.CMD_INFO_ALL:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.info_function)
                                                edit_message(vk, event, Functions.info_function.all_info(owner_info, vk, uptime))

                                            # 🆘🆘🆘 СТАТИСТИКА ПРОФИЛЯ [ МОДУЛЬ ИНФО ]
                                            elif command in cfg.CMD_STATS:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.info_function)
                                                edit_message(vk, event, Functions.info_function.stats_cmd(vk, owner_info))

                                            # [ МОДУЛЬ КОМАНД ] ⚙️⚙️⚙️
                                            elif command in ["купить"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.metka_zakrep(akk_id, vk, event))

                                            elif command in ["коммент"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.metka_zakrep(akk_id, vk, event))

                                            # ✅✅✅ ДАТА РЕГИСТРАЦИИ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["датарег"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.data_reg(akk_id))

                                            # ✅✅✅ УСТАНОВКА СТАТУСА [ МОДУЛЬ КОМАНД ]
                                            elif command in ["статус"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.set_status(event, vk))

                                            # ✅✅✅ ПОСТАВИТЬ ЛАЙК НА АВУ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["+лайк"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.set_like(akk_id, vk))

                                            # ✅✅✅ УБРАТЬ ЛАЙК С АВЫ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["-лайк"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.delete_like(akk_id, vk))

                                            # ✅✅✅ ПОСТАВИТЬ ФОТО НА АВУ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["+ава"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.set_ava(event, vk, akk_id))

                                            # ✅✅✅ УБРАТЬ ФОТО С АВЫ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["-ава"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.delete_ava(event, vk))

                                            # ✅✅✅ ТОП БАЛАНСА [ МОДУЛЬ КОМАНД ]
                                            elif command in ["топбаланс"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.top_balance(vk))

                                            # ✅✅✅ ТОП РЕГА [ МОДУЛЬ КОМАНД ]
                                            elif command in ["топрег"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.top_registr(vk))

                                            # ✅✅✅ ПРОЛАЙКАТЬ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["пролайкать"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.likewall(vk, akk_id, owner_info, event))

                                            # ✅✅✅ СТИКЕРЫ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["стики"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.stickers(owner_info, akk_id))

                                            # ✅✅✅ ОЗВУЧИТЬ ТЕКСТ [ МОДУЛЬ КОМАНД ]
                                            elif command in ["озвучь"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                Commands.cmd_user_use.text_to_speech(event, vk)

                                            # ✅✅✅ ТЕКСТ ТРЕКА [ МОДУЛЬ КОМАНД ]
                                            elif command in ["слова"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.get_lyrics(event, vk))

                                            # ✅✅✅ УСТАНОВКА НИКА [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_NICK:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.cmd_nick(vk, owner_info, event, owner_info))

                                            # ✅✅✅ УСТАНОВКА УВЕД [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_YES_UV:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_cmd_uved(vk, akk_id))

                                            # ✅✅✅ УДАЛЕНИЕ УВЕД [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_NO_UV:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_cmd_uved(vk, akk_id))

                                            # ✅✅✅ ДОБАВЛЕНИЕ В ЧС [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_YES_BL:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_cmd_blacklist(vk, akk_id))

                                            # ✅✅✅ УДАЛЕНИЕ С ЧС [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_NO_BL:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_cmd_blacklist(vk, akk_id))

                                            # ✅✅✅ ДОБАВЛЕНИЕ В ДР [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_YES_DR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.yes_cmd_friends(vk, akk_id))

                                            # ✅✅✅ УДАЛЕНИЕ С ДР [ МОДУЛЬ КОМАНД ]
                                            elif command in cfg.CMD_NO_DR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.cmd_user_use)
                                                    edit_message(vk, event, Commands.cmd_user_use.no_cmd_friends(vk, akk_id))

                                            # [ МОДУЛЬ ДОВЕРЯННЫХ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ДОБАВИТЬ В ДОВЕРЯННЫЕ [ МОДУЛЬ ДОВЕРЯННЫХ ]
                                            elif command in cfg.CMD_YES_TRUSTED:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_trusted)
                                                    msg, list_trusted = Commands.module_trusted.yes_cmd_trusted(akk_id, owner_info, list_trusted)
                                                    edit_message(vk, event, msg)

                                            # ✅✅✅ УДАЛИТЬ ИЗ ДОВЕРЯННЫХ [ МОДУЛЬ ДОВЕРЯННЫХ ]
                                            elif command in cfg.CMD_NO_TRUSTED:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_trusted)
                                                    msg, list_trusted = Commands.module_trusted.no_cmd_trusted(akk_id, owner_info, list_trusted)
                                                    edit_message(vk, event, msg)

                                            # ✅✅✅ ПОСМОТРЕТЬ СПИСОК ДОВЕРЯННЫХ [ МОДУЛЬ ДОВЕРЯННЫХ ]
                                            elif command in cfg.CMD_CHECK_TRUSTED:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_trusted)
                                                edit_message(vk, event, Commands.module_trusted.check_trusted(vk, list_trusted))

                                            # [ МОДУЛЬ ИГНОР ] ⚙️⚙️⚙️
                                            # ✅✅✅ ДОБАВИТЬ В ИГНОР [ МОДУЛЬ ИГНОР ]
                                            elif command in cfg.CMD_YES_IGNORE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_ignore)
                                                    msg, list_ignore = Commands.module_ignore.yes_cmd_ignore(akk_id, owner_info, list_ignore)
                                                    edit_message(vk, event, msg)

                                            # ✅✅✅ УДАЛИТЬ ИЗ ИГНОРА [ МОДУЛЬ ИГНОР ]
                                            elif command in cfg.CMD_NO_IGNORE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_ignore)
                                                    msg, list_ignore = Commands.module_ignore.no_cmd_ignore(akk_id, owner_info, list_ignore)
                                                    edit_message(vk, event, msg)

                                            # ✅✅✅ ПОСМОТРЕТЬ ИГНОР ЛИСТ [ МОДУЛЬ ИГНОР ]
                                            elif command in cfg.CMD_CHECK_IGNORE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_ignore)
                                                edit_message(vk, event, Commands.module_ignore.check_ignore(vk, list_ignore))

                                            # [ МОДУЛЬ АЛИАСЫ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ДОБАВИТЬ АЛИАС [ МОДУЛЬ АЛИАСЫ ]
                                            elif command in cfg.CMD_YES_ALIAS:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_alias)
                                                msg, list_alias = Commands.module_alias.yes_cmd_alias(vk, owner_info, list_alias, event)
                                                edit_message(vk, event, msg)

                                            # ✅✅✅ УДАЛИТЬ АЛИАС [ МОДУЛЬ АЛИАСЫ ]
                                            elif command in cfg.CMD_NO_ALIAS:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_alias)
                                                msg, list_alias = Commands.module_alias.no_cmd_alias(vk, owner_info, list_alias, event)
                                                edit_message(vk, event, msg)

                                            # ✅✅✅ ПОСМОТРЕТЬ ЛИСТ АЛИАСОВ [ МОДУЛЬ АЛИАСЫ ]
                                            elif command in cfg.CMD_ALIAS:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_alias)
                                                edit_message(vk, event, Commands.module_alias.check_alias(owner_info))

                                            # [ МОДУЛЬ ИЗБРАННЫХ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ДОБАВИТЬ ИЗБРАННЫЙ ДИАЛОГ [ МОДУЛЬ ИЗБРАННЫХ ]
                                            elif command in cfg.CMD_YES_FAVORITE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.yes_cmd_favorite(vk, event, owner_info))

                                            # ✅✅✅ УДАЛИТЬ ИЗБРАННЫЙ ДИАЛОГ [ МОДУЛЬ ИЗБРАННЫХ ]
                                            elif command in cfg.CMD_NO_FAVORITE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.no_cmd_favorite(vk, event, owner_info))

                                            # ✅✅✅ ПОСМОТРЕТЬ ЛИСТ ИЗБРАННОГО [ МОДУЛЬ ИЗБРАННЫХ ]
                                            elif command in cfg.CMD_FAVORITE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.cmd_favorite(vk, owner_info))

                                            # [ МОДУЛЬ ЧАТА ] ⚙️⚙️⚙️
                                            # ✅✅✅ ОТПРАВКА СМС В ЛС
                                            elif command in cfg.LS_MESSAGE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.send_user_message(vk, event, akk_id))

                                            # ✅✅✅ ПРОЧТЕНИЕ СМС
                                            elif command in ["прочитать"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                Commands.cmd_user_use.read_message(vk, event)

                                            # ✅✅✅ СМЕНА ФОНА ЧАТА
                                            elif command in ["фон"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.cmd_user_use)
                                                edit_message(vk, event, Commands.cmd_user_use.send_themes(vk, event))

                                            # ✅✅✅ ДОСТУПНЫЕ ФОНЫ ЧАТА
                                            elif command in ["фоны"]:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                edit_message(vk, event, f"📃 Доступные фоны для чатов:\n\n[1] Мятное\n[2] Ретровейв\n[3] Диско\n[4] Красивое\n[5] Нежное\n[6] Голубой\n[7] Красный\n[8] Голубое\n[9] Оранжевое\n[10] Синее\n[11] Розовое")

                                            # ✅✅✅ ВЫДАТЬ АДМИНА [ МОДУЛЬ ЧАТА ]
                                            elif command in cfg.CMD_YES_AD:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_chat)
                                                    edit_message(vk, event, Commands.module_chat.yes_cmd_admin(vk, akk_id, event))

                                            # ✅✅✅ ЗАБРАТЬ АДМИНА [ МОДУЛЬ ЧАТА ]
                                            elif command in cfg.CMD_NO_AD:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_chat)
                                                    edit_message(vk, event, Commands.module_chat.no_cmd_admin(vk, akk_id, event))

                                            # ✅✅✅ КИКНУТЬ С ЧАТА [ МОДУЛЬ ЧАТА ]
                                            elif command in cfg.CMD_KICK:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_chat)
                                                    edit_message(vk, event, Commands.module_chat.yes_cmd_kick(vk, akk_id, event))

                                            # ✅✅✅ ДОБАВИТЬ В ЧАТ [ МОДУЛЬ ЧАТА ]
                                            elif command in cfg.CMD_ADD:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                akk_id = search_id(event, vk, owner_info)
                                                if akk_id == owner_info["id"]:
                                                    edit_message(vk, event, "⚠️ Не обнаружен ID")
                                                else:
                                                    # importlib.reload(Commands.module_chat)
                                                    edit_message(vk, event, Commands.module_chat.no_cmd_kick(vk, akk_id, event))

                                            # УДАЛЕНИЕ ЛИЧНЫХ СМС
                                            elif command in ["дд"]:
                                                # importlib.reload(Commands.module_chat)
                                                delete_message_dd(vk, event, Commands.module_chat.cmd_dd(vk, event, owner_info))

                                            # [ МОДУЛЬ ЧИСТКИ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ЧИСТКА ЧС
                                            elif command in cfg.CMD_BL_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_blacklist(vk, owner_info, event))

                                            # ✅✅✅ ЧИСТКА ГРУПП [ МОДУЛЬ ЧИСТКИ ]
                                            elif command in cfg.CMD_GROUP_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_group(vk, owner_info, event))

                                            # ✅✅✅ ЧИСТКА ДИАЛОГОВ [ МОДУЛЬ ЧИСТКИ ]
                                            elif command in cfg.CMD_MESSAGE_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_message(vk, owner_info, event))

                                            # ✅✅✅ ЧИСТКА СТЕНЫ [ МОДУЛЬ ЧИСТКИ ]
                                            elif command in cfg.CMD_WALL_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_wall(vk, owner_info, event))

                                            # ✅✅✅ ЧИСТКА ИСТОЧНИКОВ [ МОДУЛЬ ЧИСТКИ ]
                                            elif command in cfg.CMD_UVED_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_uved(vk, owner_info, event))

                                            # ✅✅✅ ЧИСТКА СОБАК [ МОДУЛЬ ЧИСТКИ ]
                                            elif command in cfg.CMD_DOG_CLEAR:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.clear_module)
                                                edit_message(vk, event, Functions.clear_module.clear_dog(vk, owner_info, event))

                                            # [ МОДУЛЬ ШАБЛОНОВ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ПРОСМОТР ШАБЛОНОВ [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.template_list(owner_info))

                                            # ✅✅✅ ДОБАВЛЕНИЕ ШАБЛОНА [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_YES_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.yes_template(owner_info, vk, event))

                                            # ✅✅✅ УДАЛЕНИЕ ШАБЛОНА [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_NO_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.no_template(owner_info, vk, event))

                                            # ✅✅✅ ОТПРАВКА ШАБЛОНА [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_SEND_TEMPLATE:
                                                # importlib.reload(Commands.module_template)
                                                msg, atts, replmsg = Commands.module_template.send_template(owner_info, event, vk)
                                                send_if_not_edit(vk, event, msg, atts, replmsg)

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ДОКУМЕНТЫ) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_DOC_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.doc_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (РАЗНОЕ) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_MORE_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.more_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (АУДИО) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_AUDIO_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.audio_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ФОТО) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_PHOTO_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.photo_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ТЕКСТ) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_TEXT_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.text_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ВИДЕО) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_VIDEO_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.video_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ГОЛОСОВЫЕ) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_VOICE_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.voice_template(owner_info))

                                            # ✅✅✅ СПИСОК ШАБЛОНОВ (ГРАФФИТИ) [ МОДУЛЬ ШАБЛОНОВ ]
                                            elif command in cfg.CMD_GRAFFITI_TEMPLATE:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_template)
                                                edit_message(vk, event, Commands.module_template.graffiti_template(owner_info))
                                            else:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                edit_message(vk, event, f"⚠️ Неправильное обращение к команде.")
                                    except Exception as error:
                                        logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line ERROR: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | ERROR: {error}""")
                                        edit_message(vk, event, f"💢 Произошла ошибка.\n💬 Информация об ошибке.\n{error}")

                                # ✅✅✅ ПРЕФИКС СКРИПТОВ ⚙️⚙️⚙️
                                if event.text.startswith(prefix_scripts) or event.text.startswith(cfg.default_scripts):
                                    try:
                                        if len(event.text.split(" ", maxsplit=5)) <= 1:
                                            clears_msg = clears_cmd(vk, event, clears_msg)
                                            edit_message(vk, event, "⚠️ Команда не обнаружена.")
                                        else:
                                            command_split = event.text.split("\n", maxsplit=5)
                                            command = command_split[0].split(" ", maxsplit=5)[1].lower()

                                            # [ МОДУЛЬ ИНФО ] ⚙️⚙️⚙️
                                            # ✅✅✅ ИНФО СКРИПТОВ [ МОДУЛЬ ИНФО ]
                                            if command in cfg.commands_scr_info:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.info_function)
                                                edit_message(vk, event, Functions.info_function.info_scr(vk, owner_info))

                                            # ✅✅✅ СТАТИСТИКА СКРИПТОВ [ МОДУЛЬ ИНФО ]
                                            elif command in cfg.commands_scr_stats:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Functions.info_function)
                                                edit_message(vk, event, Functions.info_function.stats_scr(vk, owner_info))

                                            # [ МОДУЛЬ СКРИПТЫ ] ⚙️⚙️⚙️
                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТОПРИЕМА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_on_frie:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_frie(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТОПРИЕМА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_off_frie:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_frie(owner_info, vk))

                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТОЛАЙКА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_on_like:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_like(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТОЛАЙКА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_off_like:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_like(owner_info, vk))

                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТООТПИСКИ [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_on_undr:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_undr(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТООТПИСКИ [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_off_undr:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_undr(owner_info, vk))

                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТОРЕКОМЕНДАЦИЙ [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_on_req:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_req(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТОРЕКОМЕНДАЦИЙ [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_off_req:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_req(owner_info, vk))

                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТОПИЛОТА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_on_aupi:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_aupi(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТОПИЛОТА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in cfg.commands_off_aupi:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_aupi(owner_info, vk))

                                            # ✅✅✅ ВКЛЮЧЕНИЕ АВТООНЛАЙНА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in ['+вч']:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.on_scr_onl(owner_info, vk))

                                            # ✅✅✅ ВЫКЛЮЧЕНИЕ АВТООНЛАЙНА [ МОДУЛЬ СКРИПТЫ ]
                                            elif command in ['-вч']:
                                                clears_msg = clears_cmd(vk, event, clears_msg)
                                                # importlib.reload(Commands.module_script)
                                                edit_message(vk, event, Commands.module_script.off_scr_onl(owner_info, vk))

                                    except Exception as error:
                                        logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")
                                        edit_message(vk, event, f"💢 Произошла ошибка.\n💬 Информация об ошибке.\n{error}")
            except Exception as error:
                if str(error) in cfg.NO_SEND_ERROR or str(error) in ["HTTPSConnectionPool(host='im.vk.com', port=443): Read timed out. (read timeout=35)", "'<' not supported between instances of 'NoneType' and 'int'", "HTTPSConnectionPool(host='api.vk.me', port=443): Read timed out. (read timeout=35)"]:
                    logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")
                else:
                    logger.error(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")

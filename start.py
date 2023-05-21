# -*- coding: utf8 -*-
import vk_api, os, threading, cfg, time, pymysql, traceback, random, subprocess
from base_module import *
from colorama import Fore
from multiprocessing import Process
from itertools import zip_longest
from loguru import logger
# /./# Импорты Пулов #/./#
from user import user
# /./# Импорты Пулов #/./#

# /./# Импорты скриптов #/./#
from Commands.module_script import script


# /./# Импорты скриптов #/./#

def id_editor_text(ids):
    return str(ids).replace('0', 'kdj').replace('1', 'hjd').replace('2', 'jnn').replace('3', 'lie').replace('4',
                                                                                                            'kee').replace(
        '5', 'ovn').replace('6', 'fll').replace('7', 'qdk').replace('8', 'kfa').replace('9', 'jkd')


def id_editor_numb(ids):
    return str(ids).replace('kdj', '0').replace('hjd', '1').replace('jnn', '2').replace('lie', '3').replace('Kee',
                                                                                                            '4').replace(
        'ovn', '5').replace('fll', '6').replace('qdk', '7').replace('kfa', '8').replace('jkd', '9')


def letsgo(token_lists):
    bot = vk_api.VkApi(token=cfg.vk_lp_group_token)
    bot._auth_token()
    for token_to_start in token_lists:
        try:
            vk = vk_api.VkApi(token=token_to_start[1])
            vk._auth_token()
            owner_info = vk.method("account.getProfileInfo")
            vk.method("messages.allowMessagesFromGroup",
                      {"group_id": 215286352, "key": random.randint(0000000, 9999999)})
        except Exception as error:
            if str(error) in cfg.NO_SEND_ERROR:
                update_base("users", "token_vkadmin", "none", "vkontakte_id", token_to_start[0])
            else:
                logger.error(
                    f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Line: {traceback.format_exc().partition('line ')[2].partition(', in')[0]} | {error}""")
        else:
            # logger.info(f"""{owner_info["first_name"]} {owner_info["last_name"]} @id{str(owner_info["id"])} | Launch...""")
            threading.Thread(target=user, name="user{}".format(id_editor_text(owner_info["id"])),
                             args=(owner_info, vk,)).start()
            threading.Thread(target=script, name="script{}".format(id_editor_text(owner_info["id"])),
                             args=(owner_info, bot)).start()
    return


def chunks(lst, count):
    n = len(lst) // count
    return list(x for x in zip_longest(*[iter(lst)] * n))


def start():
    os.system("clear")
    hello = """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░██████╗░███████╗██╗░░░██╗███████╗███╗░░██╗░██████╗░███████╗░
░░██╔══██╗██╔════╝██║░░░██║██╔════╝████╗░██║██╔════╝░██╔════╝░
░░██████╔╝█████╗░░╚██╗░██╔╝█████╗░░██╔██╗██║██║░░██╗░█████╗░░░
░░██╔══██╗██╔══╝░░░╚████╔╝░██╔══╝░░██║╚████║██║░░╚██╗██╔══╝░░░
░░██║░░██║███████╗░░╚██╔╝░░███████╗██║░╚███║╚██████╔╝███████░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
"""
    print(Fore.GREEN + hello)
    con = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base,
                          database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = con.cursor()
    token_lists = []
    cursor.execute(f"SELECT vkontakte_id, token_vkadmin, token_vkme FROM users")
    for base in cursor.fetchall():
        if base[1] != "none":
            if base[0] not in [00]:
                token_lists.append(base)

    proc = Process(target=letsgo, args=(token_lists,))
    proc.start()
    logger.info(f"""Launch completed.""")
    proc.join()


if __name__ == '__main__':
    start()

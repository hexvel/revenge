import random

import vk_api, os, time, json, sqlite3, sys, threading, cfg, re, math, psutil, subprocess, requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard


# Команды группы
def group():
    vk = vk_api.VkApi(token=cfg.vk_lp_group_token)
    vk._auth_token()
    while True:
        try:
            lp = VkBotLongPoll(vk, 215286352)
            for event in lp.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object.text.startswith("ии"):
                        if event.object.text != "":
                            text = str(event.object.text).replace("ии", "")
                            data = {"ask": text, "userid": event.object.from_id}
                            headers = {'Content-Type':'application/x-www-form-urlencoded,'}
                            data_json = json.dumps(data,ensure_ascii=False)
                            payload = {'query': data_json}
                            apiurl = "https://aiproject.ru/api/"
                            resp = requests.post(apiurl, data=payload, headers=headers)
                            answer = resp.json()
                            try:
                                responce = answer['aiml'].encode('iso-8859-1').decode('utf-8').replace("https://aiproject.ru", "Не важно.").replace("@bigrusbot", "[Пососи хуй]").replace("Телеграме", "мире")
                            except:
                                responce = ["☺", "🥰", "😊"][random.randint(0, 2)]
                            atts = ""
                            vk.method("messages.send", {"peer_id": event.object.peer_id, "message": responce, "attachment": atts, "reply_to": event.object.message_id, "random_id": 0})
        except:
            pass

group()

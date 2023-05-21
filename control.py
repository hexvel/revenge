import vk_api, os, time, json, sqlite3, sys, threading, cfg, re, math, psutil, subprocess
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from time import sleep
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard


def start(event, vk, api):
    mass = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info["name"] == "python.exe":
            for i in proc.cmdline():
                mass.append(i)
            pass
    if mass.count("main.py") == 0:
        subprocess.Popen(['python', r'main.py'], shell = True)
        """api.messages.send(peer_id=2000000001,message=f"⚙ [БОТ] Запуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000002,message=f"⚙ [БОТ] Запуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000003,message=f"⚙ [БОТ] Запуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000004,message=f"⚙ [БОТ] Запуск...",random_id=0)
        time.sleep(0.5)"""
    else:
        api.messages.send(peer_id=event.object.peer_id,message="💢 Уже запущен.",random_id=0)


def stop(event, vk, api):
    mass = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info["name"] == "python.exe":
            for i in proc.cmdline():
                mass.append(i)
                if i == "main.py":
                    kill = proc.pid
    if mass.count("main.py") == 0:
        api.messages.send(peer_id=event.object.peer_id,message="💢 Не запущен.",random_id=0)
    else:
        print(kill)
        p = psutil.Process(kill)
        p.kill()
        """api.messages.send(peer_id=2000000001,message=f"⚙ [БОТ] Остановлен.",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000002,message=f"⚙ [БОТ] Остановлен.",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000003,message=f"⚙ [БОТ] Остановлен.",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000004,message=f"⚙ [БОТ] Остановлен.",random_id=0)
        time.sleep(0.5)"""


def restart(event, vk, api):
    mass = []
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if proc.info["name"] == "python.exe":
            for i in proc.cmdline():
                mass.append(i)
                if i == "main.py":
                    kill = proc.pid
    if mass.count("main.py") == 0:
        api.messages.send(peer_id=event.object.peer_id,message="💢 Не запущен.",random_id=0)
    else:
        p = psutil.Process(kill)
        p.kill()
        subprocess.Popen(['python', r'main.py'], shell = True)
        """api.messages.send(peer_id=2000000001,message=f"⚙ [БОТ] Перезапуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000002,message=f"⚙ [БОТ] Перезапуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000003,message=f"⚙ [БОТ] Перезапуск...",random_id=0)
        time.sleep(0.5)
        api.messages.send(peer_id=2000000004,message=f"⚙ [БОТ] Перезапуск...",random_id=0)
        time.sleep(0.5)"""

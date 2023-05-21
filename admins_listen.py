import vk_api, cfg, time, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from methods import *


def admins_listen(vk, owner_info, event):
    try:
        if event.text != "":
            for dont in cfg.dont_send_message:
                try:
                    event.text.index(dont)
                except:
                    pass
                else:
                    try:
                        vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id, "delete_for_all": "1"})
                    except Exception as error:
                        return
                    send_message(vk, event, f"👁 В чате запрещены эти слова.\n💬 Просьба не писать их больше.\n💥 [id{event.user_id}|Предупреждение] +1.")
                    return

        if event.attachments.get("attach1_type"):
            if event.attachments["attach1_type"] == "wall":
                try:
                    vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id, "delete_for_all": "1"})
                except Exception as error:
                    return
                send_message(vk, event, f"👁 В чат запрещено присылать посты.\n💬 Просьба не присылать больше.\n💥 [id{event.user_id}|Предупреждение] +1.")
                return

            elif event.attachments["attach1_type"] == "poll":
                try:
                    vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id, "delete_for_all": "1"})
                except Exception as error:
                    return
                send_message(vk, event, f"👁 В чат запрещено присылать опросы.\n💬 Просьба не присылать больше.\n💥 [id{event.user_id}|Предупреждение] +1.")
                return

        if event.__dict__.get("source_act"):
            if event.source_act == "chat_invite_user_by_link":
                hello_user = vk.method("users.get", {"user_ids": event.user_id})[0]
                help_user = "[id" + str(owner_info["id"]) + "|.к помощь]"
                user_link = "[id" + str(hello_user["id"]) + "|" + hello_user["first_name"] + " " + hello_user["last_name"] + "]"
                msg = f"""
👤 Привет, {user_link}. Рад видеть.

💬 Буду благодарен если расскажешь о нас друзьям.
Узнать список команд пропиши: {help_user}

❤ Спасибо тебе. Приятного пользования."""
                send_message(vk, event, msg)
                return
            if event.source_act == "chat_invite_user":
                hello_user = vk.method("users.get", {"user_ids": event.source_mid})[0]
                help_user = "[id" + str(owner_info["id"]) + "|.к помощь]"
                user_link = "[id" + str(hello_user["id"]) + "|" + hello_user["first_name"] + " " + hello_user["last_name"] + "]"
                msg = f"""
👤 Привет, {user_link}. Рад видеть.

💬 Буду благодарен если расскажешь о нас друзьям.
Узнать список команд пропиши: {help_user}

❤ Спасибо тебе. Приятного пользования."""
                send_message(vk, event, msg)
                return
        else:
            return
    except:
        return

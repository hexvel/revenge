import vk_api, time


def send_message(vk, event, msg="", atts="", replmsg=""):
    try:
        return True, vk.method("messages.send", {"peer_id": event.peer_id ,"message": msg, "attachment": atts, "reply_to": replmsg, "random_id": 0})
    except Exception as error:
        return False, error


def edit_message(vk, event, msg="", atts=""):
    try:
        return True, vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": msg, "attachment": atts,  "message_id": event.message_id, "random_id": 0})
    except Exception as error:
        print(error)
        return False, error


def send_if_not_edit(vk, event, msg="", atts="", replmsg=""):
    try:
        return True, vk.method("messages.edit", {"peer_id": event.peer_id ,"keep_forward_messages": 1,"message": msg, "attachment": atts,  "message_id": event.message_id, "random_id": 0})
    except Exception as error:
        try:
            vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id, "delete_for_all": "1"})
            return True, vk.method("messages.send", {"peer_id": event.peer_id ,"message": msg, "attachment": atts, "reply_to": replmsg, "random_id": 0})
        except Exception as error:
            return False, error


def delete_message_ii(vk, message_id):
    try:
        return True, vk.method("messages.delete", {"peer_id": -194070336,"message_id": message_id, "delete_for_all": "1"})
    except Exception as error:
        return False, error


def delete_message(vk, event):
    try:
        return True, vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id, "delete_for_all": "1"})
    except Exception as error:
        try:
            return vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id})
        except:
            return False, error


def delete_message_dd(vk, event, msg):
    try:
        return True, vk.method("messages.delete", {"peer_id": event.peer_id,"message_ids": msg, "delete_for_all": "1"})
    except Exception as error:
        try:
            return vk.method("messages.delete", {"peer_id": event.peer_id,"message_ids": msg})
        except Exception as error:
            return False, error


def delete_message_no_all(vk, event):
    try:
        return True, vk.method("messages.delete", {"peer_id": event.peer_id,"message_id": event.message_id})
    except Exception as error:
        return False, error


def send_message_no_event(vk, from_to, msg="", atts="", replmsg=""):
    try:
        return True, vk.method("messages.send", {"peer_id": from_to,"message": msg, "attachment": atts, "reply_to": replmsg, "random_id": 0})
    except Exception as error:
        return False, error


def send_message_boombs(vk, event, msg="", atts="", replmsg=""):
    try:
        return True, vk.method("messages.send", {"peer_id": event.peer_id ,"message": msg, "expire_ttl": 60, "attachment": atts, "reply_to": replmsg, "random_id": 0})
    except Exception as error:
        return False, error

# -/-# Конфигурации | Текста #-/-#
# Для вызова импортировать файл #


qiwi_token = "---"
vk_lp_group_token = "---"

dont_send_message = ["@all", "@online", "@все", "@онлайн", "*all", "*online", "*все", "*онлайн",
                     "мать ебал", "Мать ебал", "мать шлюха", "Мать шлюха"]

# --- Стандартные префиксы ---
default_scripts = ".т"
default_command = ".к"

sql_request = f"""INSERT INTO base_name (vkontakte_id, token_vkadmin, token_vkme, nick_name, balance, stats_li, stats_dr, stats_uv, stats_ot, stats_as, stats_ar,
                condition_li, condition_dr, condition_uv, condition_ot, condition_as, condition_ar, condition_ao, condition_on,
                rang, status, register_time, text_uv, atta_uv,
                list_ignore, list_trusted, prefix_commands, prefix_scripts, prefix_repeats,
                referral, start_time, stop_time, dont_clear_message,
                template_audio, template_photo, template_video, template_voice, template_graffiti, template_doc,
                achievements, stats_register) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

BASE_COLUMN = """(vkontakte_id, token_vkadmin, token_vkme, nick_name, balance, stats_li, stats_dr, stats_uv, stats_ot, stats_as, stats_ar,
                condition_li, condition_dr, condition_uv, condition_ot, condition_as, condition_ar, condition_ao,, condition_on,
                rang, status, register_time, text_uv, atta_uv,
                list_ignore, list_trusted, prefix_commands, prefix_scripts, prefix_repeats,
                referral, start_time, stop_time, dont_clear_message,
                template_audio, template_photo, template_video, template_voice, template_graffiti, template_doc,
                achievements, stats_register)"""

# ИСКЛЮЧЕНИЕ ОШИБОК
NO_SEND_ERROR = ["[5] User authorization failed: user revoke access for this token.",
                 "[5] User authorization failed: invalid access_token (4).",
                 "[5] User authorization failed: invalid session.",
                 "[5] User authorization failed: user is blocked.",
                 "[5] User authorization failed: access_token has expired.",
                 "[3610] User is deactivated: invalid access_token (8).",
                 "[5] User authorization failed: user revoke access for this token.",
                 "[3610] User is deactivated"]

# СИМВОЛЫ ДЛЯ НИКА
NICE_WORDS = ["й", "ц", "у", "к", "е", "н",
              "г", "ш", "щ", "з", "х", "ъ",
              "ё", "ф", "ы", "в", "а", "п",
              "р", "о", "л", "д", "ж", "э",
              "я", "ч", "с", "м", "и", "т",
              "ь", "б", "ю", "q", "w", "e",
              "r", "t", "y", "u", "i", "o",
              "p", "a", "s", "d", "f", "g",
              "h", "j", "k", "l", "z", "x",
              "c", "v", "b", "n", "m", " ",
              "🌐", "⚙️", "❤️", "🏳️‍🌈"]

# ЗАПРЕЩЕННЫЕ КОМАНДЫ ПОВТОРЯЛКИ
FORBIDDEN_COMMANDS = ["команды", "повторялка", "скрипты", "лс", "+дов", "-дов", "+игнор", "-игнор"]

FOR_ALIAS_COMMAND = ["токен", "рег", "инфо", "стата", "ник", "пинг", "кинг", "пиу",
                     "кик", "съеби", "пока", "вернуть", "добавить", "привет",
                     "+чс", "-чс", "+др", "-др", "+ув", "-ув",
                     "+админ", "-админ", "довы", "довлист", "+дов", "-дов",
                     "игнор", "игнорлист", "+игнор", "-игнор", "изб", "+изб", "-изб",
                     "!группы", "!смс", "!стена", "!исток", "!собак",
                     "+др", "-др", "+лайк", "-лайк", "+увед", "-увед",
                     "+отп", "-отп", "+рек", "-рек", "шабы", "шаб", "+шаб", "-шаб", "документы",
                     "разное", "текст", "аудио", "фото", "видео", "голосовые", "граффити",
                     "vk_me", "vkme", "вкми", "вкме", "+пилот", "-пилот", "дд", "фон", "фоны",
                     "номер", "+агент", "-агент", "получить", "стики", "помощь", "пинфо", "прочитать",
                     "лс", "влс", "пролайкать", "статус", "озвучь", "слова", "+ава", "-ава", "!чс", "коммент",
                     "рестарт", "кмд", "скр", "+алиас", "-алиас", "алиасы", "чистка"]

# --- Функции ---
DONAT = ["пополнить", "донат", "спонсор"]
REGISTER = ["рег"]
VK_ME = ["токен"]
CMD_INFO_ALL = ["пинфо"]
CMD_INFO = ["инфо"]
CMD_STATS = ["стата"]
CMD_HELP = ["помощь", "help", "команды"]
CMD_NICK = ["ник"]
CMD_PING = ["пинг", "кинг", "пиу"]
CMD_KICK = ["кик", "съеби", "пока"]
CMD_ADD = ["вернуть", "добавить", "привет"]
CMD_YES_BL = ["+чс"]
CMD_NO_BL = ["-чс"]
CMD_YES_DR = ["+др"]
CMD_NO_DR = ["-др"]
CMD_YES_UV = ["+ув"]
CMD_NO_UV = ["-ув"]
LS_MESSAGE = ["лс", "влс"]
CMD_YES_AD = ["+админ"]
CMD_NO_AD = ["-админ"]
CMD_CHECK_TRUSTED = ["довы", "довлист"]
CMD_YES_TRUSTED = ["+дов"]
CMD_NO_TRUSTED = ["-дов"]
CMD_CHECK_IGNORE = ["игнор", "игнорлист"]
CMD_YES_IGNORE = ["+игнор"]
CMD_NO_IGNORE = ["-игнор"]
CMD_FAVORITE = ["изб"]
CMD_YES_FAVORITE = ["+изб"]
CMD_NO_FAVORITE = ["-изб"]
CMD_ALIAS = ["алиасы"]
CMD_YES_ALIAS = ["+алиас"]
CMD_NO_ALIAS = ["-алиас"]
CMD_TEMPLATE = ["шабы"]
CMD_SEND_TEMPLATE = ["шаб"]
CMD_YES_TEMPLATE = ["+шаб"]
CMD_NO_TEMPLATE = ["-шаб"]
CMD_DOC_TEMPLATE = ["документы"]
CMD_MORE_TEMPLATE = ["разное"]
CMD_TEXT_TEMPLATE = ["текст"]
CMD_AUDIO_TEMPLATE = ["аудио"]
CMD_PHOTO_TEMPLATE = ["фото"]
CMD_VIDEO_TEMPLATE = ["видео"]
CMD_VOICE_TEMPLATE = ["голосовые"]
CMD_GRAFFITI_TEMPLATE = ["граффити"]
CMD_BL_CLEAR = ["!чс"]
CMD_GROUP_CLEAR = ["!группы"]
CMD_MESSAGE_CLEAR = ["!смс"]
CMD_WALL_CLEAR = ["!стена"]
CMD_UVED_CLEAR = ["!исток"]
CMD_DOG_CLEAR = ["!собак"]

# --- Скрипты ---
commands_scr_info = ["инфо"]
commands_scr_stats = ["стата"]

commands_on_frie = ["+др"]
commands_off_frie = ["-др"]

commands_on_like = ["+лайк"]
commands_off_like = ["-лайк"]

commands_on_uved = ["+увед"]
commands_off_uved = ["-увед"]

commands_on_undr = ["+отп"]
commands_off_undr = ["-отп"]

commands_on_req = ["+рек"]
commands_off_req = ["-рек"]

commands_on_aupi = ["+пилот"]
commands_off_aupi = ["-пилот"]

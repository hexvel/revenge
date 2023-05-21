import pymysql, base_info
from array import *


# ВЫГРУЗКА ВСЕХ ДАННЫХ
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [НАЗВАНИЕ СТОЛБЦА]
def select_base_all(base_name, name_column):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = f"SELECT {name_column} FROM {base_name}"
    cursor.execute(sqlrequest)
    connect.close()
    return cursor.fetchall()


# ВЫГРУЗКА ВСЕХ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [НАЗВАНИЕ СТОЛБЦА] [ОБЪЕКТЫ/ПАРАМЕТРЫ ВЫБОРА]
def select_base_all_u(base_name, where_search):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = f"SELECT * FROM {base_name} WHERE {where_search}"
    cursor.execute(sqlrequest)
    connect.close()
    return cursor.fetchall()


# ВЫГРУЗКА ДАННЫХ
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [ОБЪЕКТ ПОИСКА] [ПАРАМЕТР ПОИСКА]
def select_base(base_name, object_search, owner_search):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = "SHOW columns FROM {}".format(base_name)
    cursor.execute(sqlrequest)
    name_columns = []
    all = cursor.fetchall()
    for name in all:
        name_columns.append(name[0])
    sqlrequest = "SELECT * FROM {} WHERE {} = {}".format(base_name, object_search, owner_search)
    cursor.execute(sqlrequest)
    value_columns = []
    one = cursor.fetchone()
    for name in one:
        value_columns.append(name)
    SBI = dict(zip(name_columns, value_columns))
    connect.close()
    return SBI


# ВЫГРУЗКА ДАННЫХ НС
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [ОБЪЕКТ ПОИСКА] [ПАРАМЕТР ПОИСКА] [ОБЪЕКТЫ/ПАРАМЕТРЫ ВЫБОРА]
def selectw_base(base_name, where):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = "SHOW columns FROM {}".format(base_name)
    cursor.execute(sqlrequest)
    name_columns = []
    all = cursor.fetchall()
    for name in all:
        name_columns.append(name[0])
    sqlrequest = "SELECT * FROM {} WHERE {}".format(base_name, where)
    cursor.execute(sqlrequest)
    value_columns = []
    one = cursor.fetchone()
    for name in one:
        value_columns.append(name)
    SBI = dict(zip(name_columns, value_columns))
    connect.close()
    return SBI


# ОБНОВЛЕНИЕ ДАННЫХ
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [ОБЪЕКТ ОБНОВЛЕНИЯ] [ПАРАМЕТР ОБНОВЛЕНИЯ] [ОБЪЕКТ ВЫБОРА] [ПАРАМЕТР ВЫБОРА]
def update_base(base_name, set_column, set_value, where_column, where_value):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = f"UPDATE {base_name} SET {set_column} = '{set_value}' WHERE {where_column} = {where_value}"
    cursor.execute(sqlrequest)
    connect.commit()
    return connect.close()


# ОБНОВЛЕНИЕ ДАННЫХ НС
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [ОБЪЕКТ ОБНОВЛЕНИЯ] [ПАРАМЕТР ОБНОВЛЕНИЯ] [ОБЪЕКТЫ/ПАРАМЕТРЫ ВЫБОРА]
def updatew_base(base_name, set_column, set_value, where):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor = connect.cursor()
    sqlrequest = f"UPDATE {base_name} SET {set_column} = '{set_value}' {where}"
    cursor.execute(sqlrequest)
    connect.commit()
    return connect.close()


# ДОБАВЛЕНИЕ НОВЫХ ДАННЫХ
# ПРИНИМАЕТ: [НАЗВАНИЕ ТАБЛИЦЫ] [ОБЪЕКТ ПОИСКА] [ПАРАМЕТР ПОИСКА] [НАЗВАНИЕ ЭЛЕМЕНТОВ] [ЭЛЕМЕНТЫ]
def insert_base(base_name, object_search, owner_search, sql_items, sql_value):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor, sql_inj = connect.cursor(), ""
    sqlrequest = "SELECT * FROM {} WHERE {} = {}".format(base_name, object_search, owner_search)
    cursor.execute(sqlrequest)
    if cursor.fetchone() is None:
        for i in range(sql_items.count(",") + 1):
            if i == 0:
                sql_inj += "%s"
            else:
                sql_inj += ", %s"

        sql_request = f"""INSERT INTO {base_name} {sql_items} VALUES ({sql_inj})"""
        cursor.execute(sql_request, sql_value)
        connect.commit()
        connect.close()
        return True
    else:
        connect.close()
        return False


# ПРОВЕРКА ДАННЫХ
def search_base(base_name, object_search, owner_search):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor, sql_inj = connect.cursor(), ""
    sqlrequest = f"SELECT * FROM {base_name} WHERE {object_search} = '{owner_search}'"
    cursor.execute(sqlrequest)
    if cursor.fetchone() is None:
        connect.close()
        return False
    else:
        connect.close()
        return True


# ПРОВЕРКА ДАННЫХ
def searchw_base(base_name, where_search):
    connect = pymysql.connect(host=base_info.ip_base, user=base_info.login_base, password=base_info.pass_base, database='lp', charset='utf8', init_command='SET NAMES UTF8')
    cursor, sql_inj = connect.cursor(), ""
    sqlrequest = f"SELECT * FROM {base_name} WHERE {where_search}"
    cursor.execute(sqlrequest)
    if cursor.fetchone() is None:
        connect.close()
        return False
    else:
        connect.close()
        return True

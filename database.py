import psycopg2 as lib


def Add_Client(user, conteiner):
    db1 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5432")
    mycursor1 = db1.cursor()
    try:
        mycursor1.execute('select * from add_client(%(p)s);',
                          {"p": user})
        mycursor1.execute('select * from add_conteiner(%(p1)s,%(p2)s);',
                          {"p1": user, "p2": conteiner})
        print('ID   Username     Conteiner')
        mycursor1.execute('select TheiaUsers.id, username, TheiaDockerContainers.id from TheiaUsers inner join '
                          'TheiaDockerContainers '
                          'on TheiaUsers.id = TheiaDockerContainers.user_id;')
        for row in mycursor1:
            print(row)
        db1.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor1.close()
        if db1 is not None:
            db1.close()


def Delete_Conteiner(conteiner):
    db2 = lib.connect(dbname="postgres", user="postgres", password="tv1cssdh", host="127.0.0.1", port="5432")
    mycursor2 = db2.cursor()
    try:
        mycursor2.execute('select * from delete_conteiner(%(h)s);',
                          {"h": conteiner})
        mycursor2.execute('select * from TheiaDockerContainers;')
        for row in mycursor2:
            print(row)
        db2.commit()
    except (Exception, lib.DatabaseError) as error:
        print(error)
    finally:
        mycursor2.close()
        if db2 is not None:
            db2.close()

#
# def Greeting():
#     print('0. Add_Client\n'
#           '1. Delete_Conteiner\n')
#     print('Введите номер функции')
#     print('Вы ввели:\n')
#     num = int(input())
#     if num < 0 or num > 1:
#         print('Что-то не так, введите число от 0 до 1!')
#         return -2
#     return num
#
#
# operations = [Add_Client, Delete_Conteiner]
#
#
# def main():
#     ACK = 1
#     while ACK != 0:
#         i = Greeting()
#         if i == -2:
#             print('Повторите попытку')
#         else:
#             if i == 0:
#                 print('Введите user')
#                 user = input()
#                 print('Введите conteiner')
#                 conteiner = input()
#                 action = operations[i]
#                 action(user, conteiner)
#             if i == 1:
#                 print('Введите conteiner')
#                 conteiner = input()
#                 action = operations[i]
#                 action(conteiner)
#             print('Продолжить?')
#             print('Введите Да(1) или Нет(0):\n')
#             ACK = int(input())
#             if ACK == 0:
#                 print('До свидания!')
#
#
# main()

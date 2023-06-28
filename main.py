from vkbottle import VKAPIError
from vkbottle.user import Message
from vkbottle import Bot
from vkbottle.modules import logger
import asyncio
import json
import re
import getpass
import sqlite3
import os

time_to_die = 120


def txtfile():
    try:
        my_file = open("database/info.txt", "w+", encoding="utf-8")
        my_file.write("Весь кода был написан https://vk.com/all.s.ninehr\n"
                      "github этого проекта: https://github.com/infikot/CaptchaBot\n"
                      "\n"
                      "Информация по данной базе данных:\n"
                      " - Распространяется на все беседы, в которых состоит бот, токен которого Вы указываете\n"
                      "   при его запуске.\n"
                      " - user_id INT - уникальный ИД пользователя, который выдаётся при создании страницы ВК.\т"
                      " - status_in_chat TEXT - статус пользователя в данном боте.\n "
                      "   Бывает трёх типов: waiting; banned; passed. Думаю расписывать их не стоит.\n"
                      "\n"
                      "Чтобы обнулить базу данных нужно удалить эту папку (database) из Вашей файловой системы,\n"
                      "а чтобы очистить определённого пользователя (или забанить его)\n"
                      "достаточно прописать одноимённые ^ban <пользователь> или ^pass <пользователь> в чате.")
        my_file.close()
    except:
        pass


try:
    sqlite_connection = sqlite3.connect('database/bots.db')
    cursor = sqlite_connection.cursor()
    txtfile()
except:
    try:
        my_cwd = os.getcwd()
        new_dir = 'database'
        path = os.path.join(my_cwd, new_dir)
        os.mkdir(path)
    except:
        print("\n!!ОШИБКА ПРИ СОЗДАНИИ ДИРЕКТОРИИ \"database\"!!\n")
    try:
        sqlite_connection = sqlite3.connect('database/bots.db')
        cursor = sqlite_connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id INT,
            status_in_chat TEXT);""")
        sqlite_connection.commit()
    except:
        print("\n!!ОШИБКА ПРИ СОЗДАНИИ БАЗЫ ДАННЫХ В ДИРЕКТОРИИ \"database\"!!\n")
    try:
        sqlite_connection = sqlite3.connect('database/bots.db')
        cursor = sqlite_connection.cursor()
    except:
        print("\n!!ОШИБКА ПРИ ПОДКЛЮЧЕНИИ К БАЗЕ ДАННЫХ!!\n")
    txtfile()

end = False
while end == False:
    try:
        variable = {1: True, 2: False, 3: "debug"}

        choice = int(input('Сводка информации:\n'
                           '  "1" = Предоставлять действия из чатов;\n'
                           '  "2" = НЕ предоставлять действия из чатов;\n'
                           '  "3" = debug информация\n'
                           'Ввод: '))

        variable = variable.get(choice)
        if choice > 0 and choice < 4:
            debug = variable
            end = True
        else:
            print("\nНеверный выбор.\n\n")
    except:
        print("\nНеверный выбор.\n\n")

if debug == True or debug == False:
    logger.disable("vkbottle")

bot = Bot(token=getpass.getpass('\n\nТокен группы (скрытый ввод): '))
print("\nБот был успешно запущен! (..если не было выведено ошибок..)\n\n")

bot.labeler.vbml_ignore_case = True


@bot.on.chat_message(text=["^ban", "^ban <member_id>"])
async def ban(message: Message, member_id: str or None = None):
    chat = await bot.api.messages.get_conversations_by_id(peer_ids=[message.peer_id])
    admin_ids = json.loads(chat.items[0].json())['chat_settings']['admin_ids']
    if message.from_id in admin_ids:
        if message.reply_message:
            member_id = message.reply_message.from_id
        elif member_id is not None:
            if "vk.com/" in member_id:
                member_id = re.search(r'vk\.com\/([a-zA-Z0-9_\.]*)', member_id).group(1)
            elif "@" in member_id or "|" in member_id:
                member_id = re.search(r'\[id(?P<id>\d+)\|([^\n].*?)]', member_id).group(1)
            else:
                member_id = int(member_id)
        if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
            res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
            if res[0][1] == "waiting" or res[0][1] == "passed":
                cursor.execute(f'UPDATE users SET status_in_chat = "banned" WHERE user_id = {int(member_id)}')
                sqlite_connection.commit()
                await message.reply(message=f"Пользователь @id{member_id} был забанен вручную.",
                                    attachment=message.conversation_message_id)
                await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                if debug == True: print(
                    f"Пользователь https://vk.com/id{member_id} был кикнут из беседы, ведь он был забанен вручную.")
            else:
                await message.reply(message=f"Пользователь @id{member_id} уже забанен.",
                                    attachment=message.conversation_message_id)
                try:
                    await bot.api.messages.remove_chat_user(chat_id=member_id, member_id=member_id)
                except:
                    pass
        else:
            cursor.execute(f'INSERT INTO users (user_id, status_in_chat) VALUES ({member_id}, "banned")')
            sqlite_connection.commit()
            if debug == True: print(
                f"Пользователь https://vk.com/id{member_id} был забанен вручную.")
            try:
                await bot.api.messages.remove_chat_user(chat_id=member_id, member_id=member_id)
            except:
                pass
            await message.reply(message=f"Пользователь @id{member_id} был забанен вручную.",
                                attachment=message.conversation_message_id)


@bot.on.chat_message(text=["^pass", "^pass <member_id>"])
async def ban(message: Message, member_id: str or None = None):
    chat = await bot.api.messages.get_conversations_by_id(peer_ids=[message.peer_id])
    admin_ids = json.loads(chat.items[0].json())['chat_settings']['admin_ids']
    if message.from_id in admin_ids:
        if message.reply_message:
            member_id = message.reply_message.from_id
        elif member_id is not None:
            if "vk.com/" in member_id:
                member_id = re.search(r'vk\.com\/([a-zA-Z0-9_\.]*)', member_id).group(1)
            elif "@" in member_id or "|" in member_id:
                member_id = re.search(r'\[id(?P<id>\d+)\|([^\n].*?)]', member_id).group(1)
            else:
                member_id = int(member_id)
        if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
            res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
            if res[0][1] == "waiting" or res[0][1] == "banned":
                cursor.execute(f'UPDATE users SET status_in_chat = "passed" WHERE user_id = {int(member_id)}')
                sqlite_connection.commit()
                await message.reply(message=f"Пользователь @id{member_id} был разбанен или подтверждён вручную.",
                                    attachment=message.conversation_message_id)
                if debug == True: print(
                    f"Пользователь https://vk.com/id{member_id} был разбанен или подтверждён вручную.")
            else:
                await message.reply(message=f"Пользователь @id{member_id} уже был подтверждён.",
                                    attachment=message.conversation_message_id)
        else:
            cursor.execute(f'INSERT INTO users (user_id, status_in_chat) VALUES ({member_id}, "passed")')
            sqlite_connection.commit()
            if debug == True: print(
                f"Пользователь https://vk.com/id{member_id} был разбанен или подтверждён вручную.")
            await message.reply(message=f"Пользователь @id{member_id} был разбанен или подтверждён вручную.",
                                attachment=message.conversation_message_id)


@bot.on.chat_message()
async def text(message: Message):
    act = message.action
    try:
        if "conversation_message_id=None" in str(
                act) and "type=<MessagesMessageActionStatus.CHAT_INVITE_USER: 'chat_invite_user'>" in str(act):
            act = act.json()
            member_id = json.loads(act)['member_id']
            if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
                res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
                if res[0][1] == "banned":
                    await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                    if debug == True: print(
                        f"Пользователь https://vk.com/id{member_id} был кикнут из беседы, ведь он уже был забанен системой.")
                    message_to_delete = await message.answer(
                        f"@id{member_id} ранее был забанен в боте. Для его разбана админам чата нужно прописать ^pass <пользователь> \n\nЭто сообещние исчезнет через 10 секунд.")
                    await asyncio.sleep(10)
                    await bot.api.messages.delete(cmids=message_to_delete.conversation_message_id,
                                                  peer_id=message.peer_id, delete_for_all=True)
            else:
                message_to_delete = await message.answer(
                    f'Приветствую, @id{member_id}! \nПеред свои первым сообщением настоятельно рекомендую решить пример ниже, ведь это АнтиБот система! \n\n 2+2*2=? \n(ответ 6, напиши только это число!) \n\nСообщение будет удалено через {time_to_die} секунд, ровно столько времени у Вас есть для решения капчи!')
                if debug == True: print(
                    f"Капчу начал проходить пользователь https://vk.com/id{member_id}, \nведь он вступил в беседу, в которой находился активный бот.")
                cursor.execute(f'INSERT INTO users (user_id, status_in_chat) VALUES ({member_id}, "waiting")')
                sqlite_connection.commit()
                if debug == True: print(f"Был выдан статус waiting пользователю https://vk.com/id{member_id}")
                await asyncio.sleep(time_to_die)
                await bot.api.messages.delete(cmids=message_to_delete.conversation_message_id, peer_id=message.peer_id,
                                              delete_for_all=True)
                try:
                    if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
                        res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
                        if res[0][1] == "waiting":
                            if debug == True: print(
                                f"Пользователь https://vk.com/id{member_id} не успел пройти капчу.. Ему был \nвыдан статус banned")
                            await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                            if debug == True: print(
                                f"Пользователь https://vk.com/id{member_id} был кикнут из беседы.")
                except:
                    pass
        elif "6" in message.text[:10]:
            member_id = message.from_id
            if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
                res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
                if res[0][1] == "waiting":
                    cursor.execute(f'UPDATE users SET status_in_chat = "passed" WHERE user_id = {int(member_id)}')
                    sqlite_connection.commit()
                    if debug == True: print(
                        f"Пользователь https://vk.com/id{member_id} успешно прошёл капчу! Ему был \nвыдан статус passed")
                    await message.reply(
                        message=f"Вы успешно прошли капчу!\nТо сообщение будет удалено через отведённый указанный срок.",
                        attachment=message.conversation_message_id)
                elif res[0][1] == "banned":
                    await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                    await bot.api.messages.delete(cmids=message.conversation_message_id,
                                                  peer_id=message.peer_id, delete_for_all=True)
                    if debug == True: print(
                        f"Пользователь https://vk.com/id{member_id} был кикнут из беседы, ведь он уже был забанен системой.")
                    message_to_delete = await message.answer(
                        f"@id{member_id} ранее был забанен в боте. \n\nЭто сообещние исчезнет через 10 секунд.")
                    await asyncio.sleep(10)
                    await bot.api.messages.delete(cmids=message_to_delete.conversation_message_id,
                                                  peer_id=message.peer_id, delete_for_all=True)
        else:
            member_id = message.from_id
            try:
                if cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall():
                    res = cursor.execute(f'SELECT * FROM users WHERE user_id = {int(member_id)}').fetchall()
                    if res[0][1] == "waiting":
                        cursor.execute(f'UPDATE users SET status_in_chat = "banned" WHERE user_id = {int(member_id)}')
                        sqlite_connection.commit()
                        if debug == True: print(
                            f"Пользователь https://vk.com/id{member_id} не смог пройти капчу.. Ему был \nвыдан статус banned")
                        await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                        if debug == True: print(
                            f"Пользователь https://vk.com/id{member_id} был кикнут из беседы.")
                        await bot.api.messages.delete(cmids=message.conversation_message_id,
                                                      peer_id=message.peer_id, delete_for_all=True)
                    elif res[0][1] == "banned":
                        await bot.api.messages.remove_chat_user(chat_id=message.chat_id, member_id=member_id)
                        if debug == True: print(
                            f"Пользователь https://vk.com/id{member_id} был кикнут из беседы, ведь он уже был забанен системой.")
                        await bot.api.messages.delete(cmids=message.conversation_message_id,
                                                      peer_id=message.peer_id, delete_for_all=True)
                        message_to_delete = await message.answer(
                            f"@id{member_id} ранее был забанен в боте. \n\nЭто сообещние исчезнет через 10 секунд.")
                        await asyncio.sleep(10)
                        await bot.api.messages.delete(cmids=message_to_delete.conversation_message_id,
                                                      peer_id=message.peer_id, delete_for_all=True)
            except:
                pass
    except VKAPIError as err:
        if debug == "debug":
            await message.answer(f"Произошла ошибка: {err}")
            print(f"\nПроизошла ошибка: {err}\n\n")
        elif debug == True:
            print(f"\nПроизошла ошибка: {err}\n\n")
        else:
            pass


bot.run_forever()
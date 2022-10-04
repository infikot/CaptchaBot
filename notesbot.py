import random
import sys
import timeit
from typing import Tuple

from loguru import logger
from vkbottle import User
from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.user import Message

from config import tokenbot, tokenalisia
from rule import Permission

logger.remove()
logger.add(sys.stderr, level="INFO")

bot = Bot(token=tokenbot)
userbot = User(token=tokenuser)

bot.labeler.custom_rules["Permission"] = Permission


@bot.on.message(text="/ping")
async def info_hand(message: Message):
    await message.answer(f">>pong {timeit.timeit()}")


@bot.on.message(text="/ac")
async def info_hand(message: Message):
    await message.answer(
        "Беседы и их команды: \n \n https://vk.me/join/p77tSVT2BOvT9d0_xDIQ5tG4l0R0pw2moIA= \n Заметки, ранг <18+> \n Разрешены /r* команды: \n Все. \n \n https://vk.me/join/mMYQJA/I3b/Q0STlMZHjbTkCC4/xaUqJsZU= \n Заметки, ранг <offtop> \n Разрешены /r* команды: \n /rlegs; /random; /rmems; \n \n https://vk.me/join/QOeVTQqLOAFIv2TzwBd0_A/IlCCWDn65fjs= \n Заметки, ранг <default> \n Разрешены /r* команды: \n Нет разрешённых команд /r*")


@bot.on.chat_message(text="/info")
async def info_hand(message: Message):
    await message.answer(
        "Информация: \n Мой создатель - vk.com/all.s.ninehr \n Основные команды добавлены 06.08.2022 \n На данный момент добавлено 30% от нужных функций, но в скоре все 100% будут добавлены в меня//~ \n Отдельная благодарность: \n vk.com/id583976210,  vk.com/id715892900,  vk.com/id601395326")


@bot.on.chat_message(text="/help")
async def help_hand(message: Message):
    user = await bot.api.users.get(message.from_id)
    await message.answer(
        f"Приветик {user[0].first_name}! Я - бот Алисия! 😸 \n Я очень люблю Заметки, по этому я и создана! \n Вот что я могу: \n /random;   /rhentai; \n /rxxx;   /rlegs; \n /info;   /ac; \n /rmems;   /rhorny; \n /ac;   /help;")


@bot.on.chat_message(Permission(["638920116", "1"]), text="/kick")
async def kick(message: Message):
    await bot.api.messages.remove_chat_user(message.peer_id - 2000000000, message.reply_message.from_id)
    return "Пользователь успешно исключён из данной беседы"


@bot.on.chat_message(text="/rlegs")
async def rlegs(message: Message):
    if message.chat_id in (2, 3, 4):
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285924951")
        photo = random.choice(photos.items)
        await message.answer(message="Вот тебе ножки, семпай~", attachment=f"photo{photo.owner_id}_{photo.id}")
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена. \n Проверь полный список команд и их разрешений с помощью команды /ac")


@bot.on.chat_message(text="/rxxx")
async def rxxx(message: Message):
    if message.chat_id == 3:
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285930017")
        photo = random.choice(photos.items)
        await message.answer(
            message="Вот тебе порнушка)~ \n Жаль, что мы не сможем так поиграть с тобой семпай так-же..!///~",
            attachment=f"photo{photo.owner_id}_{photo.id}")
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена, шалунишка. \n Проверь полный список команд и их разрешений с помощью команды /ac")


@bot.on.chat_message(text="/rmems")
async def rmems(message: Message):
    if message.chat_id in (2, 3, 4):
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285930013")
        photo = random.choice(photos.items)
        await message.answer(message="Ого, шуточки? Хехе, хорошо, развлекайся, семпай!~",
                             attachment=f"photo{photo.owner_id}_{photo.id}")
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена. \n Проверь полный список команд и их разрешений с помощью команды /ac")


@bot.on.chat_message(text="/chat_id")
async def chat_id(message: Message):
    await message.answer(message.peer_id)


@bot.on.chat_message(text="/test")
async def test(message: Message):
    if message.chat_id in (3, 4):
        await message.answer("This chat avalible")
    else:
        await message.answer("This chat do not avalible")



@bot.on.chat_message(CommandRule("say", ["/"], 1))
async def say_handler(message: Message, args: Tuple[str]):
    cmids = message.conversation_message_id
    await bot.api.messages.delete(peer_id=message.peer_id, delete_for_all=1, cmids=cmids)
    return bot.on.chat_message(f"<<{args[0]}>>")



@bot.on.chat_message(text="/random <first:int> <second:int>")
async def say_handler(message: Message, first, second):
    rand = random.randint(first, second)
    print(rand)
    await message.answer(f"Рандомная цифра равна: {rand}")

'''
@bot.on.chat_message(Permission(), text="/testrule")
async def testrule(message: Message):
    await message.answer("It's work!")
'''


bot.run_forever()
userbot.run_forever()
import random
import sys
import timeit
from typing import Tuple

from loguru import logger
from vkbottle import User
from vkbottle.bot import Bot
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.user import Message

from rule import Permission

""""
logger.remove()
logger.add(sys.stderr, level="INFO")
"""

tokenbot = input("Введите токен бота: \n")
tokenalisia = input("Введите токен юзербота: \n")

bot = Bot(token=tokenbot)
userbot = User(token=tokenalisia)


bot.labeler.custom_rules["Permission"] = Permission

imagefurrynocopy = "0"

@bot.on.message(text="/ping")
async def info_hand(message: Message):
    await message.answer(f">>pong {timeit.timeit()}")


@bot.on.message(text="/ac")
async def info_hand(message: Message):
    await message.answer(
        "Беседы и их команды: \n \n none information")


@bot.on.chat_message(text="/info")
async def info_hand(message: Message):
    await message.answer(
        "Информация: \n Мой создатель - vk.com/all.s.ninehr \n Основные команды добавлены 06.08.2022 \n На данный момент добавлено 50% от нужных функций, но в скоре все 100% будут добавлены в меня//~ \n Отдельная благодарность: \n vk.com/id583976210,  vk.com/id715892900,  vk.com/id601395326")


@bot.on.chat_message(text="/help")
async def help_hand(message: Message):
    user = await bot.api.users.get(message.from_id)
    await message.answer(
        f"Приветик {user[0].first_name}! Я - бот Алисия! 😸 \n Я очень люблю Заметки, по этому я и создана! \n Вот что я могу: \n /random;   /rhentai; \n /rxxx;   /rlegs; \n /info;   /ac; \n /rmems;   /rhorny; \n /ac;   /help;")



@bot.on.chat_message(text="/rlegs")
async def rlegs(message: Message):
    if message.chat_id in (2, 5, 4):
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285924951")
        photo = random.choice(photos.items)
        await message.answer(message="Вот тебе ножки, семпай~", attachment=f"photo{photo.owner_id}_{photo.id}")
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена. \n Проверь полный список команд и их разрешений с помощью команды /ac")


@bot.on.chat_message(text="/rxxx")
async def rxxx(message: Message):
    if message.chat_id == 5:
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
    if message.chat_id in (2, 4, 5):
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285930013")
        photo = random.choice(photos.items)
        await message.answer(message="Ого, шуточки? Хехе, хорошо, развлекайся, семпай!~",
                             attachment=f"photo{photo.owner_id}_{photo.id}")
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена. \n Проверь полный список команд и их разрешений с помощью команды /ac")

@bot.on.chat_message(text="/rhorny")
async def rhorny(message: Message):
    if message.chat_id in (5, 4):
        print("\n \n \n" + str(imagefurrynocopy) + "\n \n \n")
        photos = await userbot.api.photos.get(owner_id=-214905751, album_id="285930010")
        photo = random.choice(photos.items)
        if photo.id in imagefurrynocopy:
            photo = random.choice(photos.items)
            if photo.id in imagefurrynocopy:
                photo = random.choice(photos.items)
                await message.answer(message="Решил пошалить со своими зверюшками? Ну, удачи, семпай!~",
                                     attachment=f"photo{photo.owner_id}_{photo.id}")
                imagefurrynocopy.append(photo.id)
            else:
                await message.answer(message="Решил пошалить со своими зверюшками? Ну, удачи, семпай!~",
                                 attachment=f"photo{photo.owner_id}_{photo.id}")
                imagefurrynocopy.append(photo.id)
        else:
            await message.answer(message="Решил пошалить со своими зверюшками? Ну, удачи, семпай!~",
                                 attachment=f"photo{photo.owner_id}_{photo.id}")
            imagefurrynocopy.append(photo.id)
        photo = 0
    else:
        await message.answer(
            "В данной беседе эта команда запрещена. \n Проверь полный список команд и их разрешений с помощью команды /ac")


@bot.on.chat_message(text="/chat_id")
async def chat_id(message: Message):
    await message.answer(message.peer_id)


@bot.on.chat_message(text="/test")
async def test(message: Message):
    if message.chat_id in (3, 4, 5):
        await message.answer("This chat avalible")
    else:
        await message.answer("This chat do not avalible")


bot.run_forever()
userbot.run_forever()
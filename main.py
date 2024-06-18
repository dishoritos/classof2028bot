import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode

TOKEN = '7324815881:AAGZa-0HDdujiZjfb2PlR93mucN_RksbbaY'

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
CHANNEL_IDS = ["-1001548867673", "-1001251626451", "-1001563313833", "-1002067692781", "-1001717798983",
               "-1001654658015", "-1001301061421", "-1001722715571",
               "-1001894295621", "-1001865849271", "-1001701435110",
               "-1001799168320", "-1001737142354", "-1001747855008", "-1002120394208"]


# [levshacloser, levshamind, ulugbek_and_me, abdurahmonovss, path_by_parviz, diyorbeknotes, x_author, thoughtsofsleuth, # noqa
# lyoshasabuse, karimsblog, jastm1, karimova_zi, etoilante, avazbekkhamidov, Sayfullloo] # noqa


def start_markup():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Channels", url="https://t.me/addlist/7cbhwQ89otJkN2Zi"),
        InlineKeyboardButton(text="Check✅", callback_data="check")
    )
    return builder.adjust(1, repeat=True).as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        f"As-Salaam-Alaikum, {message.chat.first_name}! \n\nIt's wonderful to see you here! \nTo get started with the bot, please subscribe to the following channels👇",
        reply_markup=start_markup()
    )


async def check_subscription(call: CallbackQuery, chat_id: str) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=call.from_user.id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        logging.error(f"Error checking subscription for {chat_id}: {e}")
        return False


@dp.callback_query(lambda call: call.data == "check")
async def callback_check(call: CallbackQuery):
    for chat_id in CHANNEL_IDS:
        if not await check_subscription(call, chat_id):
            await call.message.edit_text("Subscribe to the channels‼️", reply_markup=start_markup())
            return
    await call.message.edit_text("Thank you for subscribing to the channels😊")
    await call.message.answer("You can join: \n\nhttps://t.me/+xuR6oPBh0XE4Yzgy")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

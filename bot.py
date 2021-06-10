from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN as bot_token
from ProfanityDetector import detector as detect
import logging
from strings import *
from functools import partial

# logger
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# vars
api_id = 6
api_hash = "eb06d4abfb49dc3eeb1aeb98ae0f581e"

# client
bot = Client(":memory:", bot_token, api_id, api_hash)

#command alias
cmd = partial(filters.command, prefixes=["/", "!"])

# check admins
async def is_admin(chat_id):
    list_of_admins = []
    async for member in app.iter_chat_members(
            chat_id, filter="administrators"):
        list_of_admins.append(member.user.id)
    return list_of_admins


# inline buttons
inline = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Help 🆘",
                callback_data="helpme"
                ),
            InlineKeyboardButton(
                text="Add me to a group ➕",
                url=f"http://t.me/{(await bot.get_me()).username}?startgroup=botstart",
                )
            ],
            [
                InlineKeyboardButton(
                    text="Source Code 💻", 
                    url="https://github.com/swatv3nub/AntiProfanity"),
                InlineKeyboardButton(
                    text="Package 📦", 
                    url="https://pypi.org/project/ProfanityDetector/"
                )
            ]
        ]
    )
        
start_back = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Back"
                callback_data="start"
            )
        ]
    ]
)

username = await bot.get_me().username
pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="PM me!"
                url=f"t.me/{username}?start"
            )
        ]
    ]
)

@bot.on_message(cmd("start"))
async def start_msg(_, message):
    if message.chat.type == "private":
        await message.reply(text=private_start, reply_markup=inline)
    else:
        message.reply(text=group_start)
        
@bot.on_message(cmd("help"))
async def helper(_, message):
    if message.chat.type == "private":
        await message.reply(text=help_text)
    else:
        await message.reply(text=pm_text)

@bot.on_callback_query(filters.regex("helpme"))
async def helpo(_, CallBackQuery):
    await CallBackQuery.edit(text=help_text, reply_markup=start_back)


@bot.on_callback_query(filters.regex("start"))
async def start_msg(_, CallBackQuery):
    await CallBackQuery.edit(
        text=private_start,
        reply_markup=inline)


@bot.on_message(filters.text & ~filters.private)
async def deleter(_, message):
    if await is_admin(message.chat.id):
        return
    awoos = message.text
    user = message.from_user.mention
    word, detected = detect(awoos)
    if detected:
        try:
            await message.reply(text=del_text.format(user=user))
            await message.delete()
        except:
            await message.reply(text=no_perms.format(user=user))

log.info("Anti Profanity: Alive & Kickin'")
bot.run()

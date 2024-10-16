# @DeleteBrain
# @RiseTeamCH
from telethon import TelegramClient, events, functions,Button
from db import users

api_id = '26930906' #Enter your api id
api_hash = 'f2369bd417f44e80f6fc6cbc46f95553' #Enter your api hash
token = '7802914669:AAEXe46bJn0MZUR0aVq_8oqrVFeLSHmOFD0' #enter your bot token
sudo = [7025116076]

client = TelegramClient('bot',api_id,api_hash)
client.parse_mode = 'html'

START = [
    [Button.text('ارسال پیام',resize = True)],
]
BACK = [
    [Button.text('بازگشت',resize = True)]
]

def is_ban(d) :
    async def ban(event) :
        ban = users.get(users.user_id == event.sender_id).is_ban
        if not int(ban) :
            return await d(event)
        else :
            return await event.reply('حساب کاربری شما مسدود شده است!')
    return ban

@client.on(
    events.NewMessage(
        pattern = '(/start|بازگشت)',
        func = lambda i:i.is_private
    )
)
@is_ban
async def start(event):
    xx = client.conversation(event.sender_id)
    await xx.cancel_all()
    user = users.get_or_none(user_id=event.sender_id)
    if user is None :
        users.create(user_id=event.sender_id)

    await event.reply(f'سلام {event.sender.first_name} به پیامرسان من خوش اومدی',buttons = START)
@client.on(
    events.NewMessage(
        pattern = 'ارسال پیام',
        func = lambda i:i.is_private
    )
)
@is_ban
async def support(event) : 
    xx = client.conversation(event.sender_id)
    await xx.cancel_all()
    async with client.conversation(event.chat.id) as conv:
        await conv.send_message('لطفا پیام خود را ارسال کنید',buttons = BACK)
        response = await conv.get_response()
        await conv.send_message('پیام شما با موفقیت برای ادمین های ربات ارسال شد !', buttons = START)

    for i in sudo :
        await response.forward_to(int(i))
        await client.send_message(i,f"پیام جدید از کاربر <a href='tg://user?id='{event.chat.id}'>{event.chat.id}</a> دریافت شد",buttons = [Button.inline('پاسخ',f'answer {event.chat.id}'),Button.inline('بن',f'ban {event.chat.id}')])
@client.on(
    events.CallbackQuery(
        pattern =  'answer (.*)',
    ),
)
async def answer(event) :
    id = event.pattern_match.group(1).decode()
    async with client.conversation(event.chat.id) as conv:
        await conv.send_message(f"لطفا پیام خود را جهت پاسخ به کاربر <a href='tg://user?id='{id}'>{id}</a> ارسال کنید",buttons = BACK)
        response = await conv.get_response()
        await conv.send_message(f"پیام شما با موفقیت برای کاربر <a href='tg://user?id='{id}'>{id} ارسال شد", buttons = START)
        await client.send_message(int(id),response)
@client.on(
    events.CallbackQuery(
        pattern =  'ban (.*)',
    ),
)
async def ban(event) :
    id = event.pattern_match.group(1).decode()
    user = users.get(users.user_id == id)
    is_ban = user.is_ban
    if not int(is_ban) :
        if int(id) in sudo : 
            return await event.answer('شما نمیتوانید ادمین های ربات را مسدود کنید !', alert = True)
        await event.answer('حساب کاربری فرد مسدود شد', alert = True)
        user.is_ban = 1
        user.save()
        await client.send_message(int(id), 'حساب کاربری شما مسدود شد!') 
    else :
        await event.answer('حساب کاربری فرد ازاد شد', alert = True)
        user.is_ban = 0
        user.save()
        await client.send_message(int(id),'حساب کاربری شما ازاد شد!')

client.start(bot_token = token)
client.run_until_disconnected()
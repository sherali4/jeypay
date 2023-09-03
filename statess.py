from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message
import knopka
from config import TOKEN
import sqlite3
gruppa = '-1001989106073'
gruppa_sale = '-1001715961258'
sherali ='496958227'
bot_id = '6368002025'
xa_yuq = '-1001605076473'

storage = MemoryStorage
from baza import add_user, add_user_name, add_user_numb, db_connect, add_user_location, katalog, add_tovar, add_item, add_zakaz, zakaz_otmen, zakaz_oladi

bot = Bot(TOKEN)

bot: Bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
database = sqlite3.connect('bot.sqlite')
cursor = database.cursor()

async def on_startup1(_):
    await db_connect()
    # print('upeshno')

class user_reg(StatesGroup):
    name =State()
    numb = State()

class tovar_reg(StatesGroup):
    name = State()
    ulchov = State()
    narx = State()
    tarifi = State()
    photo = State()

markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Telefon raqamingizni kiriting ☎️', request_contact=True)
).add(
    KeyboardButton("Lokatsiya jo'nating 🗺️", request_location=True)
).add(
    KeyboardButton("/video")
).add(
    KeyboardButton('/katalog')
)

@dp.message_handler(commands=['katalog'], state=None)
async def add_items(message: types.Message):
    if message.from_id == 6456875695 or message.from_id == 6158978005 or message.from_id == 496958227 or message.from_id == 5954851285 or message.from_id== 5163491786 or message.from_id== 6292591760 or message.from_id== 6652659593 or message.from_id== 6591515474 or message.from_id== 2060764847:
        # print('admin')
        # chat_id = message.chat.id
        await tovar_reg.name.set()
        await message.reply('Tovar nomini kiriting:', reply_markup=markup_request)
        # await bot.send_message(chat_id, 'Tovar nomini kiriting:', reply_markup=markup_request)
    else:
         # print('admin emas')
         await message.reply('Siz Admin emassiz')

@dp.message_handler(state=tovar_reg.name)
async def add_item_name(message: types.Message, state: FSMContext):
# async def add_item_name(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        # print(data['name'])
        # print('reg.name')
        # data['name'] = message.text
    await message.answer(f"Tovarning o'lchov birligini kiriting", reply_markup=knopka.cancel)
    await tovar_reg.next()

@dp.message_handler(state=tovar_reg.ulchov)
async def add_item_ulchov(message: types.Message, state: FSMContext):
    # print('reg.ulchov')
    async with state.proxy() as data:
        data['ulchov'] = message.text
    await message.answer(f"Tovarning narxini kiriting")
    await tovar_reg.next()

@dp.message_handler(state=tovar_reg.narx)
async def add_item_narx(message: types.Message, state: FSMContext):
    # print('reg.narx')
    async with state.proxy() as data:
        data['narx'] = message.text
    await message.answer(f"Tovarning tarifini kiriting")
    await tovar_reg.next()

@dp.message_handler(content_types=['sticker'])
async def check_sticker(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAANQZNdBBu9v-gLYA5PULJvsbu9ZJR0AAi8AAy1xhhUAAVh83pZaoZcwBA')
    # await message.answer(message.sticker.file_id)
    await message.answer('Stiker yubormang. foydasi yo\'q')

@dp.message_handler(state=tovar_reg.tarifi)
async def add_item_tarifi(message: types.Message, state: FSMContext):
    # print('reg.tarifi')
    async with state.proxy() as data:
        data['tarifi'] = message.text
    await message.answer(f"Tovarning rasmini kiriting")
    await tovar_reg.next()

@dp.message_handler(lambda message: not message.photo, state=tovar_reg.photo)
async def add_item_photo_check(message: types.Message):
    # print('reg.rasm-emas')
    await message.answer('Bu rasm emas')

@dp.message_handler(content_types=['photo'], state=tovar_reg.photo)
async def add_item_photo(message: types.Message, state: FSMContext):
    # print('reg.rasm')
    async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
            data['user'] = message.from_user.id
    await add_item(state)
    async with state.proxy() as data:
        await message.reply(str(data))
    await message.answer('Mahsulot kiritildi', reply_markup=markup_request)
    # await bot.send_message(chat_id=xa_yuq, text="yangi maxsulot qo'shildi")
    # await message.answer(f'{message.from_user.id}')

    # print('tovar narxi ===== ', data['narx'])
    # button1 = InlineKeyboardButton(text=f"{x[0]}", callback_data="In_First_button")
    # button2 = InlineKeyboardButton(text="Sotib olish", callback_data="In_Second_button")
    # keyboard_inline = InlineKeyboardMarkup().add(button1, button2)
    # await bot.send_photo(chat_id=xa_yuq, photo=data['photo'], caption= f"\n<b>nomi</b>- {data['ulchov']} \n<b>o'lchov birligi</b>- {data['ulchov']} \n<b>💵 narxi</b>- {data['narx']} \n<b>tarifi</b>- {data['tarifi']}", parse_mode='HTML', reply_markup=markup_request)
    button2 = InlineKeyboardButton(text="Yangi tovarlarni ko'rish", callback_data="yangi-tovar")
    keyboard_inline = InlineKeyboardMarkup().add(button2)
    await state.finish()
    await bot.send_message(xa_yuq, "Yangi mahsulot qo'shildi", reply_markup=keyboard_inline)

@dp.message_handler(content_types=['photo'])
async def start_message(message: types.Message, state=FSMContext):
    print(message)

@dp.message_handler(content_types=['contact'])
async def start_message(message: types.Message, state=FSMContext):
    # print(message.contact.phone_number)
    nomer = f'+{str(message.contact.phone_number)}'
    add_user_numb(message)
    # print(message)
    # print(message.message_id, message.date,)

@dp.message_handler(content_types=['location'])
async def start_message(message: types.Message, state=FSMContext):
    long = message.location.longitude
    lat = message.location.latitude
    # print(long, lat)
    add_user_location(message)
    await bot.send_location(496958227, lat, long)

#     7b53458e-3712-43cc-b4ad-77134a13091b yandex location



@dp.message_handler(content_types=["video"])
async def start_message(message: types.Message, state=FSMContext):
    file_id = message.video.file_id  # Get file id
    await bot.send_message(496958227, file_id)
    print(file_id)
#     BAACAgIAAxkBAAIOEWTzeW2nWIe_8fVDCp6QH4N0jWsYAAK3NQACha2gS0D18_kdgmjiMAQ video


@dp.message_handler(state=user_reg.name)
async def add_name(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    add_user_name(message)
    await bot.send_message(chat_id, 'SEND Your number')
    await message.reply("Шестое - запрашиваем контакт и геолокацию\nЭти две кнопки не зависят друг от друга",
                        reply_markup=markup_request)

@dp.message_handler(state=user_reg.numb)
async def add_numb(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    user_status = add_user_numb(message)
    if user_status == False:
        pass
    else:
        await bot.send_message(chat_id, "Registration Successfully")
        await state.finish()


@dp.message_handler(commands=['video'])
async def video_start(message: types.Message, state=FSMContext):
    await bot.send_video(message.from_user.id, video="BAACAgIAAxkBAAIXM2T0XUXj4t6dtKQMyZkjw9FaVY8pAAJ1NgACha2oSyfaF9s98fa-MAQ")



@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state=FSMContext):
    chat_id = message.chat.id
    # print(message.message_id, message.date,)
    add_user(message)
    # print(message.chat.id)
    await bot.send_message(chat_id, f'Assalomu Aleykum {message.chat.first_name}')
    # await user_reg.name.set()
    cursor.execute("SELECT * FROM tovar WHERE status = 1 ORDER BY id")
    tovar = cursor.fetchall()
    for x in tovar:
        cursor.execute("SELECT * FROM users WHERE id= ?", (x[8],))
        sotuvchi = cursor.fetchone()
        sotuvchi_nomeri = sotuvchi[2]
        button1 = InlineKeyboardButton(text=f"{x[0]}", callback_data="In_First_button")
        button2 = InlineKeyboardButton(text="Sotib olish", callback_data="In_Second_button")
        keyboard_inline = InlineKeyboardMarkup().add(button1, button2)
        await message.answer_photo(x[5], caption=f"<b style='color:rgb(255,0,0)'>ID</b> - {x[0]} \n<b>nomi</b>- {x[1]} \n<b>o'lchov birligi</b>- {x[2]} \n<b>💵 narxi</b>- {x[3]} \n<b>tarifi</b>- {x[4]} \n<b>Sotuvchi nomeri</b>- +{sotuvchi_nomeri}", parse_mode='HTML', reply_markup=keyboard_inline)

    await message.answer("Botning barcha imkoniyatlaridan foydalanish uchun telefon raqamingizni kiriting va lokatsiya jo'nating tugmasini bosing", reply_markup=markup_request)

# sotib olishni bosganda
@dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
async def check_button(call: types.CallbackQuery):
    id = call.id
    id_client = call.values['from']['id']
    # print('Id client = ', type(id_client))
    tovar_joylashtirilgan_sana = call.values['message']['date']
    # sher = call.message.reply_markup.inline_keyboard
    sher = call.values['message']['reply_markup']['inline_keyboard']
    for sh in sher:
        global nomer
        nomer = sh[0]['text']
        # print(sh[0]['text'])
    nomer = nomer
    mess = call.values['message']['message_id']
    # print(mess)
    await add_zakaz(id_client, int(nomer))
    await bot.send_message(id_client, 'Buyurtmangiz qabul qilindi. tez orada operatorlar telefon qilishadi.', reply_to_message_id=mess)

    # adminga boradi
    cursor.execute("SELECT * FROM users WHERE id=?", (id_client,))
    klient = cursor.fetchone()
    # print('klient number', klient[2])
    cursor.execute("SELECT * FROM tovar WHERE id=?", (int(nomer),))
    tovar = cursor.fetchone()
    # print('Tovarni kiritgan odam', tovar[8])
    button1 = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="In_First_admin")
    button12 = InlineKeyboardButton(text=f"{id_client}", callback_data="In_eleven_admin")
    button13 = InlineKeyboardButton(text=f"{tovar[8]}", callback_data="In_tvelve_admin")
    button2 = InlineKeyboardButton(text="sotib olmaydi", callback_data="In_Second_admin")
    button3 = InlineKeyboardButton(text="sotib oladi", callback_data="In_Third_admin")
    keyboard_inline = InlineKeyboardMarkup().add(button1, button12, button13, button2, button3)
    # await bot.send_photo(496958227, tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}", parse_mode='HTML', reply_markup=keyboard_inline)
    # await bot.send_photo(5954851285, tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}", parse_mode='HTML', reply_markup=keyboard_inline)
    await bot.send_photo(chat_id=gruppa, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]} \nxaridor nomeri - +{klient[2]} \nXaridor Ismi - {klient[1]}", parse_mode='HTML', reply_markup=keyboard_inline)
    await bot.send_location(gruppa, klient[4], klient[5])
    # print(call)
    # await bot.send_photo(chat_id=gruppa, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]} \nxaridor nomeri - [+{klient[2]}](tel:+{klient[2]})", parse_mode='HTML', reply_markup=keyboard_inline)

    # for keys in call:
    #     print(keys)
# oladini bosganda
@dp.callback_query_handler(text=["In_First_admin", "In_Second_admin"])
async def check_button(call: types.CallbackQuery):
    id_tovar = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    id_client = call.values['message']['reply_markup']['inline_keyboard'][0][1]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    # print(call)
    # print('client = ', id_client, '\ntovar = ', id_tovar, '\nmessage_id = ', message_id, '\nchat_id = ', chat_id)
    user_id = call.from_user.id
    zakaz_otmen(id_client, id_tovar, user_id=user_id)
    # await call.answer(f"Ваш ID: {call.from_user.id}", True)
    # print('UserId = ', call.from_user.id)
    # await bot.forward_message(chat_id=496958227, from_chat_id=gruppa, message_id=message_id)
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    next_message = message_id+1
    try:
        await bot.delete_message(message_id=next_message, chat_id=chat_id)
    except:
        pass

    # print(call)

    # await bot.send_message(message_thread_id='-1001989106073', 'as hdg agsd jaahs djkdha jk')

    # await bot.send_message(chat_id=gruppa, text='Text')


    # await call.answer(key)

# @dp.callback_query_handler(text=["In_First_button", "In_Second_button"])
# async def check_button(call: types.CallbackQuery):
#
#    if call.data == "In_First_button":
#        await call.message.answer("Hi! This is the first inline keyboard button.")
#    if call.data == "In_Second_button":
#        await call.message.answer("Hi! This is the second inline keyboard button.")
#    await call.answer()

@dp.callback_query_handler(text=["In_First_admin", "In_Third_admin"])
async def check_button(call: types.CallbackQuery):
    id_tovar = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    id_client = call.values['message']['reply_markup']['inline_keyboard'][0][1]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    saler_id = call.values['message']['reply_markup']['inline_keyboard'][0][2]['text']
    # print('saler_id = ', saler_id)
    # print('client = ', id_client, '\ntovar = ', id_tovar, '\nmessage_id = ', message_id, '\nchat_id = ', chat_id)
    user_id = call.from_user.id
    zakaz_oladi(id_client, id_tovar, user_id=user_id)
    next_message = message_id+1
    await bot.forward_message(chat_id=gruppa_sale, from_chat_id=gruppa, message_id=message_id)
    await bot.forward_message(chat_id=saler_id, from_chat_id=gruppa, message_id=message_id)
    try:
        await bot.forward_message(chat_id=gruppa_sale, from_chat_id=gruppa, message_id=next_message)
        await bot.forward_message(chat_id=saler_id, from_chat_id=gruppa, message_id=next_message)
    except:
        pass
    # try:
    #     await bot.forward_message(chat_id=saler_id, from_chat_id=gruppa, message_id=next_message)
    # except:
    #     pass

    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    try:
        await bot.delete_message(message_id=next_message, chat_id=chat_id)
    except:
        pass
    await call.answer('Sotuv bo\'limiga yuborildi')



@dp.callback_query_handler(text=["yangi-tovar",])
async def check_button(call: types.CallbackQuery):
    cursor.execute("SELECT * FROM 'tovar' WHERE status =?", (0,))
    yangi_tovar = cursor.fetchall()
    for tovar in yangi_tovar:
        # print(f"{tovar[0]}")
        button = InlineKeyboardButton(text=f"{tovar[0]}", callback_data="tovar")
        button1 = InlineKeyboardButton(text="O'chirish", callback_data="uchirish")
        button2 = InlineKeyboardButton(text="Qo'shish", callback_data="qushish")
        keyboard_inline = InlineKeyboardMarkup().add(button, button1, button2)
        await bot.send_photo(chat_id=xa_yuq, photo=tovar[5], caption=f"<b>ID</b> - {tovar[0]} \n<b>nomi</b>- {tovar[1]} \n<b>o'lchov birligi</b>- {tovar[2]} \n<b>💵 narxi</b>- {tovar[3]} \n<b>tarifi</b>- {tovar[4]}", parse_mode='HTML', reply_markup=keyboard_inline)


@dp.callback_query_handler(text=["uchirish",])
async def check_button(call: types.CallbackQuery):
    kod = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    cursor.execute('UPDATE tovar SET status=2 WHERE id=?', (kod, ))
    database.commit()
    await bot.delete_message(message_id=message_id, chat_id=chat_id)
    # print(message_id)

@dp.callback_query_handler(text=["qushish"])
async def check_button(call: types.CallbackQuery):
    kod = call.values['message']['reply_markup']['inline_keyboard'][0][0]['text']
    message_id = call.values['message']['message_id']
    chat_id = call.values['message']['chat']['id']
    cursor.execute('UPDATE tovar SET status=1 WHERE id=?', (kod, ))
    database.commit()
    # print(chat_id)
    await bot.delete_message(message_id=message_id, chat_id=chat_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup1,)
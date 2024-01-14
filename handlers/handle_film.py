import handlers.handle_series
from Requests.HDRezlaFilmRequest import name_find_film
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile,FSInputFile
from aiogram import Bot, Dispatcher, F,Router,types
from keyboards import reply
from data.HdRezkaApiMain.HdRezkaApi.HdRezkaApi import *
from utils.states import *
from handlers.methods import *


router = Router()

@router.message(F.text.lower() == 'пошук')
async def fill_url(message:Message,state:FSMContext):

    await state.set_state(BotStates.url)
    print('watch online')
    await message.answer('<b>Це - пошук.</b> Введіть назву серіалу чи фільму.')

async def filter_long_list(message,long_find_list,showed_items) -> list:
    if len(long_find_list) == 0:
        await message.answer('Нчого не знайдено, спробуйте знову')
        find_list = []
    elif len(long_find_list) > showed_items:
        find_list = long_find_list[:showed_items]
    else:
        find_list = long_find_list[:]
    return find_list
@router.message(BotStates.url)
async def give_film_items(message:Message,state:FSMContext,bot:Bot):
        global find_list, long_find_list, showed_items
        print('show items film')
        print(BotStates.get_root())
        name = message.text.lower()
        print(name)
        showed_items = 6
        long_find_list = await name_find_film(name)
        find_list = await filter_long_list(message,long_find_list,showed_items)
        await send_film_items(message,bot,find_list)

        if len(long_find_list) > showed_items:
            await message.answer(f'Тут {showed_items} резултатів пошуку, aле я ще  {len(long_find_list) - showed_items} збігів.',reply_markup=reply.more_kb)
            await state.set_state(BotStates.show_more)
@router.message(BotStates.show_more)
async def send_more(message:Message,state:FSMContext,bot:Bot):
    print('send more')
    global find_list, long_find_list, showed_items
    text = message.text.lower()
    print(text)
    print(f'Showe items: {showed_items}')
    if text == 'показати більше' and showed_items + 6 < len(long_find_list) :
        find_list = long_find_list[showed_items:showed_items+6]
        showed_items = showed_items + 6
        await send_film_items(message,bot,find_list)
        await message.answer(f'Тут показано {showed_items}, ще є { len(long_find_list) - showed_items}', reply_markup=reply.more_kb)
    elif text == 'показати більше' and showed_items + 6 >= len(long_find_list):
        print('show all')
        find_list = long_find_list[showed_items:]
        showed_items = len(long_find_list)
        await send_film_items(message, bot, find_list)
        await message.answer(f'<b>Це все.</b> \n Якщо не знайшли результату то просто уточніть його.', reply_markup=reply.main_button_kb)
        await state.set_state(BotStates.url)
    else:
        await state.set_state(BotStates.url)
        await give_film_items(message, state, bot)


async def send_film_items(message: Message, bot: Bot, find_list: list):

    for i in range(len(find_list)):
        img_url = find_list[i][0]
        name = find_list[i][1]
        info = find_list[i][2]
        type = find_list[i][3]
        film_url = find_list[i][4]
        id = str(find_list[i][5])
        image = URLInputFile(url=img_url, filename=img_url)
        print(film_url)
        print(name)
        await bot.send_photo(chat_id=message.chat.id, photo=image, caption=f'<b>{name}</b> \n{type}, {info}',
                             reply_markup=reply.film_name_ikb(id))





@router.callback_query()
async def callback_query(callback_query: types.CallbackQuery,state:FSMContext,bot:Bot):
    print('callback_query')
    print(callback_query.data)
    try:
        global url
        global rezka
        for i in range(len(find_list)):
            if callback_query.data == str(find_list[i][5]):
                url = find_list[i][4]
                break

        rezka = HdRezkaApi(url)
        print(url)
        print(find_list)
        if find_list[i][6]:
            seasons = await handlers.handle_series.get_seasons(url)
            await state.set_state(BotStates.season)
            await bot.send_message(chat_id=callback_query.message.chat.id, text='Виберіть сезон :',
                                   reply_markup=reply.season_builder_kb(seasons))
        else:
            await state.update_data(name=url)
            await state.set_state(BotStates.sound)
            sound_list = [i for i in rezka.translators]
            await bot.send_message(chat_id= callback_query.from_user.id, text = 'Виберіть озвучення', reply_markup=reply.sound_builder_kb(sound_list))
    except Exception as e:
         print(e)
         await callback_query.answer("От халепа, ніц не працює(")

@router.message(BotStates.sound)
async def fill_sound(message:Message,state:FSMContext,bot:Bot):
    global final_url,sound
    await state.update_data(sound=message.text)
    sound = message.text
    if sound == 'Мова оригіналу':
        sound = None
    print(sound)
    print(rezka.translators)
    await state.set_state(BotStates.qality)
    await message.answer(text='Виберіть якість',
                           reply_markup=reply.quality_kb)


@router.message(BotStates.qality)
async def fill_quality(message:Message,state:FSMContext,bot:Bot):
        await state.update_data(quality=message.text)
        global quality,sound,final_url
        quality = message.text
        try:
              qulity_url = rezka.getStream()(quality)

        except:
             await message.answer('Виберіть  нижчу якість', reply_markup=reply.quality_kb)

        else:
            await message.answer(f'{message.text} якість була застосована')

        try:
            final_url = rezka.getStream(translation=sound)(quality)
            await send_film(message, state)
        except ValueError:
            final_url = rezka.getStream(translation=f'{sound} ')(quality)
            await send_film(message, state)



async def send_film(message:Message,state:FSMContext):
    print('send film')
    global final_url
    await message.answer(f'<b>Ось ваш фільмь:</b> {final_url} \n <b>Приємного перегляду!</b>' ,reply_markup=reply.final_kb)
    await state.set_state(BotStates.final)

@router.message(BotStates.final)
async def download_film(message: Message, state: FSMContext, bot: Bot):
    global final_url,rezka
    print('download_film')
    print(final_url)
    send_url = await handlers.methods.download_video(final_url,message,sound,rezka)
    await bot.send_video(chat_id=message.chat.id, video=send_url,reply_markup=reply.main_button_kb)












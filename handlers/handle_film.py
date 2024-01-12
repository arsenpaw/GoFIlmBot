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

@router.message(F.text.lower() == 'дивитись онлайн')
async def fill_url(message:Message,state:FSMContext):

    await state.set_state(BotStates.url)
    print('watch online')
    await message.answer('<b>Це - пошук.</b> Введіть назву серіалу чи фільму.')


@router.message(BotStates.url)
async def fill_quality(message:Message,state:FSMContext,bot:Bot):
        print('fill quality')
        print(BotStates.get_root())
        global find_list
        name = message.text.lower()
        print(name)
        long_find_list = await name_find_film(name)
        if len(long_find_list) == 0:
            await message.answer('Нчого не знайдено, спробуйте знову')
        elif len(long_find_list) > 6:
            find_list = long_find_list[:6]
        else:
            find_list = long_find_list[:]
        print(find_list[0][0])
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
          await bot.send_photo(chat_id=message.chat.id, photo=image,caption=f'<b>{name}</b> \n{type}, {info}', reply_markup = reply.film_name_ikb(id))
        if len(long_find_list) > 6:
            await message.answer(f'Тут 6 резултатів пошуку, aле я найшов  {len(long_find_list)} збігів.')




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
    except:
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












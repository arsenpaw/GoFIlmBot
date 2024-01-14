
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Router,Bot
from keyboards import reply
from data.HdRezkaApiMain.HdRezkaApi.HdRezkaApi import *
from utils.states import *
import handlers.methods

global url
router = Router()


async def get_avalible_sound(info,chosen_season,chosen_episode,transltors) -> list:
    s_sound_list = []
    for i in transltors:
        if chosen_season in info[i]['episodes'].keys() and chosen_episode in info[i]['episodes'][chosen_season].keys():
            s_sound_list.append(i)
        else:
            print(f'{i} немає озвучки {chosen_season} сезону, {chosen_episode} серії')
    return  s_sound_list
async def int_to_list(num:list) -> list:
    num_list = [i for i in range(1, num + 1)]
    return num_list
async def get_episodes_in_seasone(list_episodes:dict) -> int:
    episodes_in_seasone = max(list_episodes[0].keys())
    return episodes_in_seasone
async def get_translators(rezka:HdRezkaMovie) -> list:
    translators_list = list(rezka.translators.keys())
    return translators_list
async def get_episods_from_all(info:list,chosen_season: int) -> list:
    transltors = list(rezka.translators.keys())
    dicts_episodes = [info[i]['episodes'][chosen_season] for i in transltors if
                      chosen_season in info[i]['episodes'].keys()]
    return dicts_episodes

async def get_seasons(url) -> list:
        print('get seasons')
        global info
        global rezka
        global max_season

        rezka = HdRezkaApi(url)
        info = rezka.seriesInfo
        transltors = list(rezka.translators.keys())
        dicts_seasons = [info[i]['seasons'] for i in transltors]
        for i in range(len(dicts_seasons)):
                max_season = 0
                temp = len(dicts_seasons[i])
                if max_season < temp:
                        max_season = temp

        print(f'all season is {max_season}')

        seasons = [f'Сезон {i}' for i in range(1, max_season + 1)]

        return seasons



@router.message(BotStates.season)
async def handle_season(message:Message,state:FSMContext) :
        print('handle seasons')
        info = rezka.seriesInfo
        global chosen_season
        chosen_season = int(message.text.split(' ')[1])
        episods_from_all = await get_episods_from_all(info,chosen_season)
        print(get_episods_from_all)
        episodes_in_seasone = await get_episodes_in_seasone(episods_from_all)
        list_episods = await int_to_list(episodes_in_seasone)
        print(list_episods)
        await state.set_state(BotStates.episod)
        await message.answer(text='Виберіть серію:', reply_markup=reply.episod_builder_kb(list_episods))

@router.message(BotStates.episod)
async def handle_episode(message:Message,state:FSMContext) :
        await state.update_data(epidsod=message.text)
        print('handle episod')
        try:
            global chosen_episode
            chosen_episode = int(message.text)
        except ValueError:
            await message.answer('Щось дивне ви ввели, ану давайте ще раз')

        transltors = await get_translators(rezka)
        info = rezka.seriesInfo
        print(transltors)
        s_sound_list = await get_avalible_sound(info,chosen_season,chosen_episode,transltors)
        print(s_sound_list)
        await state.set_state(BotStates.s_sound)
        await message.answer(text='Виберіть озвучення:', reply_markup=reply.sound_builder_kb(s_sound_list))



@router.message(BotStates.s_sound)
async def handle_s_sound(message:Message,state:FSMContext):
    print('handle s_soound')
    await state.update_data(s_sound=message.text)
    global s_sound
    s_sound = message.text
    if message.text == 'Мова оригіналу':
        s_sound = None
    print(s_sound)
    await state.set_state(BotStates.s_quality)
    await message.answer(text='Виберіть якість:', reply_markup=reply.quality_kb)


@router.message(BotStates.s_quality)
async def handle_s_quality(message:Message,state:FSMContext):
        await state.update_data(quality=message.text)
        global s_quality
        s_quality = message.text
        print(s_quality)

        try:
            rezka.getStream(episode=1,season=1)(s_quality)

        except:
             await message.answer('Ойойой,то є завелика якість', reply_markup=reply.quality_kb)

        else:
            await send_serial(message,state)

async def send_serial(message:Message,state:FSMContext):
    global url
    try:
        print(f'Сезон {chosen_season} , {type(chosen_season)}')
        print(f'Серія {chosen_episode} , {type(chosen_episode)}')
        print(f'Якість {s_sound} , {type(s_sound)}')
        print([s_sound])
        url = rezka.getStream(season=chosen_season,episode=chosen_episode,translation=s_sound)(s_quality)
        await message.answer(
            f'<b>Ось  {chosen_season} сезон , {chosen_episode} серія.</b> {url} \n <b>Приємного перегялду!</b>',reply_markup=reply.s_final_kb)
    except ValueError:
        url = rezka.getStream(season=chosen_season, episode=chosen_episode, translation=f'{s_sound} ')(s_quality)
        await message.answer(
            f'<b>Ось  {chosen_season} сезон , {chosen_episode} серія.</b> {url} \n <b>Приємного перегялду!</b>',reply_markup=reply.s_final_kb)

    await state.set_state(BotStates.s_final)


@router.message(BotStates.s_final)
async def final(message:Message,state:FSMContext,bot:Bot):
    print('s_final ')
    await state.update_data(s_final=message.text)
    if message.text.lower() == 'завантажити':
        global url
        send_url = await handlers.methods.download_video(url, message)
        await bot.send_video(chat_id=message.chat.id, video=send_url , reply_markup=reply.series_after_download_kb)
    else:
        global chosen_season, chosen_episode
        episods_from_all = await get_episods_from_all(info, chosen_season)
        all_episodes = await get_episodes_in_seasone(episods_from_all)
        print('Chosen season: ', chosen_season)
        print('Chosen episode: ', chosen_episode)
        print('Max season:', max_season)
        print('Max episodes:', all_episodes)
        if chosen_episode  < all_episodes and chosen_season <= max_season:
             chosen_episode += 1
             transltors = await get_translators(rezka)
             s_sound_list = await get_avalible_sound(info, chosen_season, chosen_episode, transltors)
             await state.set_state(BotStates.s_sound)
             await message.answer('Виберіть озвучення', reply_markup=reply.sound_builder_kb(s_sound_list))

        elif chosen_episode == all_episodes and chosen_season < max_season :
              chosen_episode = 1
              chosen_season += 1
              transltors = await get_translators(rezka)
              s_sound_list = await get_avalible_sound(info, chosen_season, chosen_episode, transltors)
              await state.set_state(BotStates.s_sound)
              await message.answer('Виберіть озвучення', reply_markup=reply.sound_builder_kb(s_sound_list))
        else:
            await message.answer('Покищо все, серій більше немає(.' , reply_markup=reply.main_kb)












from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from  aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Меню'),
         KeyboardButton(text='Help')
        ],
        [
         KeyboardButton(text='Vip')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

more_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Показати більше'),
        ],
        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Пошук'),
        ],
        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
main_button_kb = ReplyKeyboardMarkup(
    keyboard=[

        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
final_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Завантажити'),
        ],
        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
series_after_download_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Наступна серія'),
        ],
        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

quality_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='360p'),
            KeyboardButton(text="480p"),
            KeyboardButton(text="720p")
        ],
        [
            KeyboardButton(text="1080p"),
            KeyboardButton(text="1440p"),
            KeyboardButton(text="2160p")
        ],
        [
            KeyboardButton(text='В головне меню'),
        ],
    ],
        resize_keyboard = True,
        one_time_keyboard = True
)
s_final_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
         KeyboardButton(text='Наступна серія'),
         KeyboardButton(text='Завантажити')

        ],
        [
         KeyboardButton(text='В головне меню'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

def sound_builder_kb(sound_list):
    builder = ReplyKeyboardBuilder()
    if None in sound_list:
        sound_list[0] = 'Мова оригіналу'
    [builder.button(text=str(i)) for i in sound_list]
    key_structure(builder,sound_list)
    return builder.as_markup(resize_keyboard=True)

def film_name_ikb(id:str):
    builder = InlineKeyboardBuilder()

    builder.button(text='Перегляд онлайн',callback_data=id)
    return builder.as_markup(resize_keyboard=True)


def season_builder_kb(season):
    builder = ReplyKeyboardBuilder()
    [builder.button(text=i) for i in season]
    key_structure(builder,season)
    return builder.as_markup(resize_keyboard=True)

def episod_builder_kb(episodes):
    builder = ReplyKeyboardBuilder()
    [builder.button(text=str(i)) for i in episodes]
    key_structure(builder, episodes)
    return builder.as_markup(resize_keyboard=True)

def key_structure(builder,button_list):
    builder.button(text='В головне меню')
    builder.button(text='Назад')
    lengh = len(button_list)
    if lengh == 1:
        builder.adjust(1, 2)
    if lengh == 2:
        builder.adjust(2, 2)
    elif lengh== 3:
       builder.adjust(3,2)
    elif lengh ==  4:
       builder.adjust(*[int(len(button_list)/2)] *2,2)
    elif lengh > 4 and  lengh <= 9 :
        builder.adjust(*[int(len(button_list) / 3)] * 4,2)
    elif lengh > 9 and  lengh <= 16 :
       builder.adjust(*[int(len(button_list)/4)] *5,2)
    elif lengh > 16:
        builder.adjust(*[int(len(button_list)/4)] *8,2)






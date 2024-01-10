from aiogram.filters import CommandStart
from aiogram.types import Message,InputFile, FSInputFile
from aiogram import Bot, Dispatcher, F,Router
from keyboards import reply
import os

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("<b>Привіт !</b>\n Якщо вам потрібна допомога використайтйе комаду /help", reply_markup=reply.start_kb)
    await  message.answer(f'Poing from {os.name.upper()}!')

@router.message(F.text.lower() == 'в головне меню')
async def back_to_menu(message:Message):
    print('Back to main')
    await message.answer('Це головне меню', reply_markup=reply.start_kb)

@router.message(F.text.lower() == 'меню')
async def menu(message:Message):
    print('menu')
    await message.answer("Це все що я можу зробити для вас:", reply_markup=reply.main_kb)



@router.message(F.text.lower() == 'назад')
async def back(message:Message):
    print('назад')
    await message.answer('IS DEVELOPING')

@router.message(F.text.lower() == 'test')
async def test(message:Message,bot:Bot):
    print('send video')
    print(bot.session.api.base)
    print(bot.session.api.is_local)
    print(message.chat.id)
    video1 = FSInputFile("D:\kk.mp4")
    await bot.send_video(chat_id=message.chat.id,video=video1)

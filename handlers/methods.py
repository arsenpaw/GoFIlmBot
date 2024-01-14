from aiogram.types import Message, URLInputFile, FSInputFile, update
from aiogram import Bot, Dispatcher, F,Router
import requests,os
global dump
from data.HdRezkaApiMain.HdRezkaApi.HdRezkaApi import *
from keyboards import reply



router = Router()

class ConvertTo2gbExeption(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Error in parsing, all qualities was wrong'


async def convert_meta_to_size(metadata) -> float:
    print('convert_meta_to_size')
    byte_size = metadata['Content-Range'].split('/')[1]
    megabytes=float(byte_size)/1000000
    print( f'{str(megabytes)}  MB')
    return round(megabytes,2)


async def get_video_metadata_from_url(video_url):
    print('get_video_metadata_from_url')
    try:
        headers = {'Range': 'bytes=0-1000000'}  # Specify the range of bytes you want to fetch (adjust as needed)
        response = requests.get(video_url, headers=headers, stream=True)
        metadata = response.headers
        print(metadata)
        return metadata

    except requests.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return None

async def send_predict_download_time(size,message:Message):
    print('predict')
    if size > 1024:
        await  message.answer(f'Розмір файлу {round(size/1024,2)} GB')
        await  message.answer('Скачування може зайняти до 8 хвилин')
    else:
        await  message.answer(f'Розмір файлу {size} MB')
        await message.answer('Скачування може зайняти до 15 хвилин')


async def convert_to_2GB(message:Message,sound ,rezka):
    print('convert_to_2GB')
    sound_list = ['1080p','720p','480p','360p']
    for quality in sound_list:
        try:
            url = rezka.getStream()(quality)
            metadata = await get_video_metadata_from_url(url)
            print(metadata)
            size = await convert_meta_to_size(metadata)
            print(size)
            if size < 2048:
                await message.answer(f'Вибачте, але якість була знижена до {quality}, через надто великий розмір.')
                await send_predict_download_time(size, message)
                return  rezka.getStream(translation=sound)(quality)

        except ValueError:
                return rezka.getStream(translation=f'{sound} ')(quality)
        except:
            raise ConvertTo2gbExeption

async def download_video(url: str,message:Message,sound = None,rezka = None) -> FSInputFile:
    print('download video')
    metadata = await get_video_metadata_from_url(url)
    print(metadata)
    size =  await convert_meta_to_size(metadata)
    print(size,sound,rezka)
    if sound is not None and rezka is not None and size > 2048:
        url = await convert_to_2GB(message,sound,rezka)
    else:
       await send_predict_download_time(size,message)

    destination_folder = 'D:\Bot_Downloads'
    arr = os.listdir('D:\Bot_Downloads')
    print(arr)
    filename = url.split("/")[-1]
    if url.split("/")[-1] in arr:
        full_path = os.path.join(destination_folder, filename)
        return FSInputFile(full_path)
    response = requests.get(url)
    if response.status_code == 200:
            content = response.content
            full_path = os.path.join(destination_folder, filename)
            with open(full_path, "wb") as f:
                f.write(content)
    else:
        print('REQUEST ERROR')

    return FSInputFile(full_path)




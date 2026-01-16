import os
import asyncio
from PIL import Image
import secrets


def delete_file(name_file: str) -> bool:
    '''
    Удаляет временное изображение созданное при генерации

    :param name_file: название файла
    :type name_file: str

    :return: возвращает true если картинка удалена и false если нет
    :rtype: bool
    '''
    if os.path.exists(f'temp/{name_file}'):
        os.remove(f'temp/{name_file}')
        return True
    
    return False


def get_assets_name_file(figure: str) -> str:
    return {
        'Rock': 'rock.png',
        'Paper': 'paper.png',
        'Scissors': 'scissors.png'
    }.get(figure)


def image_generator(
    background_name_file: str,
    figure_user_1: str, 
    figure_user_2: str,
) -> str:
    '''
    Функция для создания изображения

    :param background_name_file: Название файла заднего фона
    :type background_name_file: str

    :param figure_user_1: то что выбрал игрок 1
    :type figure_user_1: str

    :param figure_user_2: то что выбрал игрок 2
    :type figure_user_2: str

    :param save_name: название файла
    :type save_name: str

    :return: название сгенерированного изображения
    :rtype: str
    '''
    base = Image.open(background_name_file).convert('RGB')
    img1 = Image.open(f'assets/{get_assets_name_file(figure_user_1)}').convert('RGBA')
    img2 = Image.open(f'assets/{get_assets_name_file(figure_user_2)}').convert('RGBA')

    if figure_user_1 == 'Paper' or figure_user_1 == 'Rock':
        img1 = img1.transpose(Image.FLIP_LEFT_RIGHT)

    if figure_user_2 == 'Scissors':
        img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)

    base.paste(img1, (18, 50), img1)

    base.paste(img2, (586, 50), img2)

    random_hex = secrets.token_hex(8)
    filename = f"{random_hex}.png"
    full_path = f'temp/{filename}'

    base.save(full_path, "PNG")

    return filename


async def async_image_generator(
    figure_user_1: str, 
    figure_user_2: str, 
    background_name_file: str = 'assets/background.png'
):
    return await asyncio.to_thread(
        image_generator,
        background_name_file=background_name_file,
        figure_user_1=figure_user_1,
        figure_user_2=figure_user_2,
    )
import secrets
import string
import os
from pathlib import Path

def generate_invite_code(length: int = 8) -> str:
    """8 символов ≈ 52 бит энтропии — более чем достаточно для invite-кода"""
    # Убираем визуально похожие символы
    alphabet = string.ascii_uppercase + string.digits
    alphabet = alphabet.replace('O', '').replace('I', '').replace('0', '')

    return ''.join(secrets.choice(alphabet) for _ in range(length))


def result_game(figure_user_1: str, figure_user_2: str) -> bool:
    '''
    Проверяет выиграл ли первый игрок
    
    :param figure_user_1: то что выбрал игрок 1
    :type figure_user_1: str
    :param figure_user_2: то что выбрал игрок 2
    :type figure_user_2: str

    :return: возвращает true если игрок 1 выиграл и false если проиграл
    :rtype: bool
    '''
    if figure_user_1 == 'Rock' and figure_user_2 == 'Scissors':
        return True
    elif figure_user_1 == 'Rock' and figure_user_2 == 'Paper':
        return False
    elif figure_user_1 == 'Scissors' and figure_user_2 == 'Paper':
        return True
    elif figure_user_1 == 'Scissors' and figure_user_2 == 'Rock':
        return False
    elif figure_user_1 == 'Paper' and figure_user_2 == 'Rock':
        return True
    else:
        return False



def create_folder(folder_name: str):
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    temp_folder = ROOT_DIR / f'{folder_name}'
    temp_folder.mkdir(exist_ok=True, parents=True)
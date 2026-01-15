import secrets
import string

def generate_invite_code(length: int = 8) -> str:
    """8 символов ≈ 52 бит энтропии — более чем достаточно для invite-кода"""
    # Убираем визуально похожие символы
    alphabet = string.ascii_uppercase + string.digits
    alphabet = alphabet.replace('O', '').replace('I', '').replace('0', '')

    return ''.join(secrets.choice(alphabet) for _ in range(length))
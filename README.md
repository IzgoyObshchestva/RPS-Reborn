<p align="center">
  <img src="assets/logo.png" width="200" alt="RPS-Reborn Logo">
</p>

[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&lines=RPS-Reborn)](https://git.io/typing-svg)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-async-green)
![aiogram](https://img.shields.io/badge/aiogram-3.x-blueviolet)
![License](https://img.shields.io/badge/License-MIT-yellow)

# RPS-Reborn

Асинхронная реализация классической игры «Камень, ножницы, бумага» в формате Telegram-бота на **aiogram 3** с выделенным backend API на **FastAPI**.

---

## 🚀 Возможности

- 🤖 Telegram-бот на aiogram 3
- ⚡ Выделенный backend API (FastAPI)
- 🖼️ Динамическая генерация игровых изображений (Pillow)
- 🎮 Игра с другом в реальном времени
- 🔐 Защищённое взаимодействие бота с API (secret token)

---

## 🛠️ Стек технологий
- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **aiogram 3**
- **Pillow**
- **SQLite + SQLAlchemy** (async, aiosqlite)
- **python-dotenv**
- **Poetry**


## 📦 Установка и запуск
### Клонировать репозиторий
```
git clone https://github.com/IzgoyObshchestva/RPS-Reborn.git
cd RPS-Reborn
```

### Создать виртуальное окружение + Установить зависимости
```
poetry install
```

### 🔑 Переменные окружения
Создайте файл `.env` в корне проекта:
```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite+aiosqlite:///db.sqlite3
ADMIN_ID=your_telegram_id
BOT_API_SECRET=your_secret_token
API_V1_URL="http://127.0.0.1:8000/api/v1"
```
> ⚠️ Никогда не коммить `.env` файл в репозиторий.

## ▶️ Запуск
Запуск API и бота происходит через файл run.py
```
poetry run python run.py
```

## Примеры использования
**Команды:**
- `/start` - регистрация пользователя
- `/game` - создание новой игры
- `/join <invitation_code>` - присоединиться к игре
- `/statistics` - просмотр статистики


---

## 🏗️ Архитектура

```text
Telegram Bot (aiogram)
        |
        | HTTP (secret token)
        v
FastAPI Backend
        |
        v
SQLite (async SQLAlchemy)
```

---

## 🤝 Контрибьютинг

Буду рад pull request'ам и идеям 🙌
Если хочешь предложить улучшение - открывай issue.

---

## 📄 Лицензия
Этот проект распространяется под лицензией MIT.
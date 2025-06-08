# 🎓 EduAdmissionBot - Чат-бот для абитуриентов ИВМИиТ КФУ

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?logo=telegram)](https://t.me/your_bot_link)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://python.org)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-blue)](https://docs.aiogram.dev/)

Бот-ассистент для абитуриентов Института вычислительной математики и информационных технологий КФУ. Предоставляет информацию о направлениях подготовки, проходных баллах и условиях поступления.

## ✨ Основные возможности

- **Информация о направлениях**:
  - Бюджетные/платные места
  - Проходные баллы
  - Стоимость обучения
  - Учебные программы

- **Приемная комиссия**:
  - Сроки подачи документов
  - Перечень необходимых документов
  - Контакты приемной комиссии

- **Умный поиск**:
  - Контекстные ответы
  - Примеры вопросов

## 🛠 Технологический стек

- **Backend**:
  - Python 3.9+
  - Aiogram 3.x (асинхронный фреймворк для Telegram ботов)
  - Fuzzywuzzy (для нечеткого поиска)

- **Данные**:
  - JSON-база направлений
  - Логирование всех запросов

## 📦 Установка и запуск

```bash
1. Клонируйте репозиторий:

git clone https://github.com/yourusername/ivmiit-admission-bot.git
cd ivmiit-admission-bot

2. Установите зависимости:
```bash
pip install -r requirements.txt

3. Настройте конфигурацию:
```bash
cp config/.env.example config/.env

Заполните .env файл своим API токеном Telegram.

4. Запустите бота:
```bash
python main.py

import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keep_alive import keep_alive
from collections import Counter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# Ваша ID
ADMIN_ID = os.getenv('ADMIN_ID')

# Запитання
questions = [
    "1. Що вас найбільше цікавить у сфері ІТ?\n"
    "   a) Розробка програмного забезпечення та створення нових додатків\n"
    "   b) Проєктування та оптимізація комп'ютерних систем\n"
    "   c) Робота зі штучним інтелектом та складними комп'ютерними системами\n"
    "   d) Покращення захисту та конфіденційності даних\n"
    "   e) Автоматизація процесів та робота з комп'ютерно-інтегрованими системами\n"
    "   f) Аналіз даних та оптимізація бізнес-процесів\n",
    
    "2. Яке завдання вам здається найбільш захоплюючим?\n"
    "   a) Створення мобільних додатків та веб-сервісів\n"
    "   b) Оптимізація продуктивності комп'ютерних систем та мереж\n"
    "   c) Проєктування систем штучного інтелекту\n"
    "   d) Виявлення та запобігання атакам на сучасних пристроях\n"
    "   e) Створення роботизованих систем та \"розумних\" пристроїв\n"
    "   f) Аналіз великих даних для прийняття бізнес-рішень\n",
    
    "3. Яка область ІТ вам найбільше подобається?\n"
    "   a) Розробка програмного забезпечення та архітектура систем\n"
    "   b) Високопродуктивні обчислення та мережеві технології\n"
    "   c) Машинне навчання та нейронні мережі\n"
    "   d) Захист даних та пошук вразливостей\n"
    "   e) Робототехніка та автоматизація\n"
    "   f) Бізнес-аналітика та обробка даних\n",
    
    "4. Яка роль у команді вам найбільше підходить?\n"
    "   a) Розробник програмного забезпечення\n"
    "   b) Системний архітектор та мережевий інженер\n"
    "   c) Спеціаліст з штучного інтелекту\n"
    "   d) Фахівець з кібербезпеки\n"
    "   e) Інженер з автоматизації\n"
    "   f) Бізнес-аналітик\n",
    
    "5. Який аспект роботи з комп'ютером вас найбільше приваблює?\n"
    "   a) Створення ефективних алгоритмів та структур даних\n"
    "   b) Оптимізація роботи серверів та мережевої інфраструктури\n"
    "   c) Розробка інтелектуальних систем та алгоритмів машинного навчання\n"
    "   d) Забезпечення безпеки та пошук вразливостей\n"
    "   e) Проєктування та оптимізація автоматизованих систем\n"
    "   f) Аналіз даних та побудова прогностичних моделей\n",
    
    "6. Яка книга вас би найбільше зацікавила?\n"
    "   a) \"Чистий код\" Роберта Мартіна\n"
    "   b) \"Комп'ютерні мережі\" Ендрю Таненбаума\n"
    "   c) \"Штучний інтелект: сучасний підхід\" Стюарта Рассела\n"
    "   d) \"Мистецтво невидимості\" Кевіна Митника\n"
    "   e) \"Індустрія 4.0: Четверта промислова революція\" Клауса Шваба\n"
    "   f) \"Наука про дані. Від теорії до практики\" Кеті О'Ніл\n",
    
    "7. Яке хобі вам найбільше підходить?\n"
    "   a) Розробка власних додатків та ігор\n"
    "   b) Налаштування та оптимізація домашньої мережевої інфраструктури\n"
    "   c) Створення чат-ботів та систем розпізнавання образів\n"
    "   d) Участь у змаганнях з комп’ютерної безпеки, виявлення фішингу\n"
    "   e) Конструювання роботів та \"розумних\" пристроїв\n"
    "   f) Аналіз даних та створення візуалізацій\n"
]

user_answers = {}
user_data = {}

def get_phone_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_button = KeyboardButton("Поділитися номером телефону", request_contact=True)
    markup.add(phone_button)
    return markup

def get_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Поїхали! 🚀"))
    return markup

# Обробник для отримання імені
@dp.message_handler(lambda message: message.chat.id in user_data and user_data[message.chat.id]['name'] is None)
async def get_name(message: types.Message):
    user_data[message.chat.id]['name'] = message.text
    await message.answer("Тепер поділися, будь ласка, своїм номером телефону.", reply_markup=get_phone_keyboard())

# Обробник для отримання номера телефону
@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message):
    if message.contact and message.chat.id in user_data:
        user_data[message.chat.id]['phone'] = message.contact.phone_number
        await message.answer("Дякую! Тепер натисни 'Поїхали! 🚀', щоб почати опитування.", reply_markup=get_start_keyboard())
    else:
        await message.answer("Будь ласка, скористайтеся командою /start для початку.")

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_info = (
        f"Інформація про користувача:\n"
        f"ID: {message.from_user.id}\n"
        f"Ім'я: {message.from_user.first_name}\n"
        f"Прізвище: {message.from_user.last_name}\n"
        f"Юзернейм: {message.from_user.username}\n"
        f"Мова: {message.from_user.language_code}\n"
        f"Чат ID: {message.chat.id}\n"
        f"Тип чату: {message.chat.type}\n"
    )
    
    await bot.send_message(ADMIN_ID, user_info)  # Надсилаємо інформацію адміну
    
    await message.answer("Привіт! Я допоможу тобі із вибором ІТ-школи, яка найкраще відповідає твоїм здібностям.")
    await asyncio.sleep(1)
    await message.answer("Як тебе звати?")
    user_data[message.chat.id] = {'answers': [], 'name': None, 'phone': None}


# Клавіатура з варіантами відповідей
def get_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("a"), KeyboardButton("b"))
    markup.add(KeyboardButton("c"), KeyboardButton("d"))
    markup.add(KeyboardButton("e"), KeyboardButton("f"))
    return markup

# Функція для обчислення результату
def calculate_result(answers):
    schools = {
        'a': 'Школа інженерії програмного забезпечення',
        'b': 'Школа високоефективних комп\'ютерних систем та мережі',
        'c': 'Школа інтелектуальних комп\'ютерних систем',
        'd': 'Школа етичних хакерів',
        'e': 'Школа Смарт-технологій та робототехніки',
        'f': 'Школа аналітики бізнес процесів'
    }

    answer_counts = Counter(answers)
    max_count = max(answer_counts.values())
    most_common_answers = [
        schools[answer] for answer, count in answer_counts.items()
        if count == max_count
    ]

    if len(most_common_answers) == 1:
        return f"Вам найбільше підходить: {most_common_answers[0]}"
    else:
        return f"Вам найбільше підходять: {', '.join(most_common_answers)}"
    


# Надсилання даних адміністратору
async def send_user_data(message, answers):
    user_info = user_data.get(message.chat.id, {})
    username = f"@{message.from_user.username}" if message.from_user.username else f"Користувач {message.from_user.id}"
    name = user_info.get('name', 'Не вказано')
    phone = user_info.get('phone', 'Не вказано')
    result = calculate_result(answers)
    
    msg = (
        f"Користувач: {username}\n"
        f"Ім'я: {name}\n"
        f"Номер телефону: {phone}\n"
        f"Відповіді: {', '.join(answers)}\n"
        f"Результат: {result}"
    )
    await bot.send_message(ADMIN_ID, msg)

# Обробник натискання кнопки "Поїхали!"
@dp.message_handler(lambda message: message.text == "Поїхали! 🚀")
async def start_questions(message: types.Message):
    if user_data[message.chat.id]['name'] is None or user_data[message.chat.id]['phone'] is None:
        await message.answer("Будь ласка, введіть ім'я та номер телефону перед початком опитування.")
        return
    user_answers[message.chat.id] = []
    await message.answer(questions[0], reply_markup=get_keyboard())

# Обробник відповідей
@dp.message_handler(lambda message: message.text.lower() in ['a', 'b', 'c', 'd', 'e', 'f'])
async def handle_answer(message: types.Message):
    current_answers = user_answers[message.chat.id]
    current_question_index = len(current_answers)

    if current_question_index < len(questions):
        current_answers.append(message.text.lower())
        if current_question_index + 1 < len(questions):
            await message.answer(questions[current_question_index + 1], reply_markup=get_keyboard())
        else:
            result = calculate_result(current_answers)
            await message.answer(result)
            await send_user_data(message, current_answers)
            del user_answers[message.chat.id]
            # Повідомлення про можливість пройти тест знову
            await message.answer("Щоб пройти тестування знову, повторно введіть /start.")



async def main():
    while True:
        try:
            await dp.start_polling()
        except Exception as e:
            logging.error(f"Помилка під час polling: {e}")
            await asyncio.sleep(15)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
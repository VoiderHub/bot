import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from keep_alive import keep_alive  # Імпортуємо keep_alive
from collections import Counter  # Додано для підрахунку відповідей
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Налаштування логування
logging.basicConfig(level=logging.INFO)

bot = Bot(token='7642582758:AAGmpst4s13Rs7RagaJQAsMF_0nffREqUgk')
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Запитання
questions = [
    "1. Що вас найбільше цікавить у сфері ІТ?\n"
    "   a) Розробка програмного забезпечення та створення нових додатків\n"
    "   b) Вивчення та впровадження новітніх технологій\n"
    "   c) Робота зі штучним інтелектом та складними комп'ютерними системами\n"
    "   d) Забезпечення кібербезпеки та етичний хакінг\n"
    "   e) Автоматизація процесів та робота з комп'ютерно-інтегрованими системами\n"
    "   f) Аналіз даних та оптимізація бізнес-процесів\n",
    "2. Яке завдання вам здається найбільш захоплюючим?\n"
    "   a) Створення мобільних додатків та веб-сервісів\n"
    "   b) Розробка інноваційних технологічних рішень\n"
    "   c) Проєктування систем штучного інтелекту\n"
    "   d) Пошук та усунення вразливостей в комп'ютерних системах\n"
    "   e) Створення роботизованих систем та \"розумних\" пристроїв\n"
    "   f) Аналіз великих даних для прийняття бізнес-рішень\n",
    "3. Яка область ІТ вам найбільше подобається?\n"
    "   a) Розробка програмного забезпечення та архітектура систем\n"
    "   b) Інноваційні технології та їх застосування\n"
    "   c) Машинне навчання та нейронні мережі\n"
    "   d) Інформаційна безпека та криптографія\n"
    "   e) Робототехніка та автоматизація\n"
    "   f) Бізнес-аналітика та обробка даних\n",
    "4. Яка роль у команді вам найбільше підходить?\n"
    "   a) Розробник програмного забезпечення\n"
    "   b) Інноватор та дослідник нових технологій\n"
    "   c) Спеціаліст з штучного інтелекту\n"
    "   d) Фахівець з кібербезпеки\n"
    "   e) Інженер з автоматизації\n"
    "   f) Бізнес-аналітик\n",
    "5. Який аспект роботи з комп'ютером вас найбільше приваблює?\n"
    "   a) Створення ефективних алгоритмів та структур даних\n"
    "   b) Вивчення та впровадження передових технологій\n"
    "   c) Розробка інтелектуальних систем та алгоритмів машинного навчання\n"
    "   d) Забезпечення безпеки та захист інформації\n"
    "   e) Проєктування та оптимізація автоматизованих систем\n"
    "   f) Аналіз даних та побудова прогностичних моделей\n",
    "6. Яка книга вас би найбільше зацікавила?\n"
    "   a) \"Чистий код\" Роберта Мартіна\n"
    "   b) \"Фізика майбутнього\" Мічіо Кайку\n"
    "   c) \"Штучний інтелект: сучасний підхід\" Стюарта Рассела\n"
    "   d) \"Мистецтво невидимості\" Кевіна Митника\n"
    "   e) \"Індустрія 4.0: Четверта промислова революція\" Клауса Шваба\n"
    "   f) \"Наука про дані. Від теорії до практики\" Кеті О'Ніл\n",
    "7. Яке хобі вам найбільше підходить?\n"
    "   a) Розробка власних додатків та ігор\n"
    "   b) Експерименти з новітніми гаджетами та технологіями\n"
    "   c) Створення чат-ботів та систем розпізнавання образів\n"
    "   d) Участь у змаганнях з етичного хакінгу\n"
    "   e) Конструювання роботів та \"розумних\" пристроїв\n"
    "   f) Аналіз даних та створення візуалізацій\n"
]

# Відповіді користувачів зберігаємо в словнику
user_answers = {}
# Словник для зберігання статусу сесії опитування
survey_started = {}

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
        'b': 'Школа інформаційних технологій майбутнього',
        'c': 'Школа інтелектуальних комп\'ютерних систем',
        'd': 'Школа етичних хакерів',
        'e': 'Школа автоматизованих технологій',
        'f': 'Школа аналітики бізнес процесів'
    }

    # Підраховуємо кількість кожної відповіді
    answer_counts = Counter(answers)

    # Знаходимо максимальну кількість відповідей
    max_count = max(answer_counts.values())

    # Збираємо всі школи, які мають максимальну кількість відповідей
    most_common_answers = [
        schools[answer] for answer, count in answer_counts.items()
        if count == max_count
    ]

    if len(most_common_answers) == 1:
        return f"Вам найбільше підходить {most_common_answers[0]}"
    else:
        return f"Вам найбільше підходять: {', '.join(most_common_answers)}"

# Створюємо клавіатуру для кнопки "Поїхали!"
def get_start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Поїхали! 🚀"))
    return markup

# Обробник команди /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Вітання від бота з кнопкою "Поїхали!"
    await message.answer(
        "Привіт! Я допоможу вам вибрати найбільш підходящу ІТ-школу.",
        reply_markup=get_start_keyboard())

# Обробник натискання кнопки "Поїхали!"
@dp.message_handler(lambda message: message.text == "Поїхали! 🚀")
async def start_questions(message: types.Message):
    user_answers[message.chat.id] = []  # Створюємо запис для відповідей користувача
    survey_started[message.chat.id] = True  # Позначаємо, що сесія почалася
    await message.answer(questions[0], reply_markup=get_keyboard())

# Обробник відповідей користувача
@dp.message_handler(lambda message: message.text.lower() in ['a', 'b', 'c', 'd', 'e', 'f'])
async def handle_answer(message: types.Message):
    # Перевіряємо, чи почалася сесія опитування
    if message.chat.id not in survey_started or not survey_started[message.chat.id]:
        await message.answer(
            "Будь ласка, спочатку натисніть 'Поїхали! 🚀'",
            reply_markup=get_start_keyboard()  # Додаємо кнопку "Поїхали!"
        )
        return

    current_answers = user_answers[message.chat.id]
    current_question_index = len(current_answers)

    if current_question_index < len(questions):
        current_answers.append(message.text.lower())

        if current_question_index + 1 < len(questions):
            await message.answer(questions[current_question_index + 1], reply_markup=get_keyboard())
        else:
            # Коли опитування завершено
            result = calculate_result(current_answers)
            await message.answer(result)
            await message.answer("Дякую за участь! Якщо ви хочете пройти опитування знову, натисніть 'Поїхали! 🚀'", reply_markup=get_start_keyboard())
            # Завершуємо сесію
            survey_started[message.chat.id] = False

if __name__ == '__main__':
    keep_alive()  # Запускаємо keep_alive
    executor.start_polling(dp, skip_updates=True)

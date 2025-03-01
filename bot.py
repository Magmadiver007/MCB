from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncpg
import asyncio


# Настройки базы данных
DB_CONFIG = {
    'user': 'postgres',
    'password': 'postgres',
    'database': 'postgres',
    'host': '192.168.0.130',
    'port': 5432,
}
# Вставьте сюда ваш токен
token = '7424360379:AAF1I88rIN8LeJAZWLVDYeelGuw5L9nIP98'

# Функция для подключения к базе данных
async def get_db_connection():
    return await asyncpg.connect(**DB_CONFIG)


# Функция для создания записи в базе данных
async def save_message_to_db(chat_id: int, message_text: str) -> None:
    conn = await get_db_connection()
    try:
        await conn.execute(
            "INSERT INTO messages (chat_id, message_text) VALUES ($1, $2)",
            chat_id, message_text
        )
    finally:
        await conn.close()


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет! Я простой бот. Напиши мне что-нибудь, и я повторю это.')


# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    message_text = update.message.text

# Обработчик текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    await update.message.reply_text(f'Вы сказали: {user_message}')

def main() -> None:

    # Создаем Application и передаем ему токен вашего бота
    application = Application.builder().token(token).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
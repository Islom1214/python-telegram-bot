import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import requests
from dotenv import load_dotenv
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ================================================================

load_dotenv()

bot_token = os.getenv("TG_TOKEN")

# ================================================================

def search_anime(query):
    api_url = "https://api.anilibria.tv/v2/searchTitles"
    params = {
        "search": query,
        "limit": 5
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from Anilibria API: {e}")
        return "Не удалось получить результаты. Пожалуйста, попробуйте позже."
    
    results = response.json()
    if not results:
        return "Результатов не найдено."

    reply = "<b>Найденные аниме:</b>\n\n"
    for result in results:
        title = result['names']['ru']
        link = f"<a href='https://www.anilibria.tv/release/{result['code']}.html'>{title}</a>"
        reply += f"🔹 {link}\n\n"

    return reply if reply else "Результатов не найдено."

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html('Привет! Я могу помочь вам найти аниме. Используйте команду <b>/search название_аниме</b>, чтобы начать поиск.')

async def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_html('Пожалуйста, укажите название аниме для поиска.')
        return

    result = search_anime(query)
    await update.message.reply_html(result)

def main() -> None:
    BOT_TOKEN = f'{bot_token}'

    app = ApplicationBuilder().token(BOT_TOKEN).build() 

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()


if __name__ == '__main__':
    main()
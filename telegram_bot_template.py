from typing import Final

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

BOT_USERNAME: Final = "BOT_USERNAME"


class TelegramCommands:
    def __init__(self) -> None:
        pass

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("CFE - Inteligencia Artificial Iniciado")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¿Necesitas ayuda?")

    async def custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Custom command")


class HandleResponses:
    def __init__(self) -> None:
        pass

    def handle_response(self, text: str) -> str:
        processed: str = text.lower()

        if "hello" in processed:
            return "hey there!"

        return "No entiendo qué es lo que quieres decir"

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = str(update.message.text).lower()

        print(f"User ({update.message.chat.id}) in {message_type}: {text}")

        if message_type == "group":
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, "").strip()
                response: str = self.handle_response(new_text)
            else:
                return
        else:
            response: str = self.handle_response(text)
        print("bot:", response)

        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    commands = TelegramCommands()
    responses = HandleResponses()

    app.add_handler(CommandHandler("start", commands.start_command))
    app.add_handler(CommandHandler("help", commands.help_command))
    app.add_handler(CommandHandler("custom", commands.custom_command))

    app.add_handler(MessageHandler(filters.TEXT, responses.handle_message))

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)

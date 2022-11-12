import logging
import os

from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

import speech

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.effective_message.reply_text(f"Welcome to MarkovBot, a Telegram bot that writes "
                                        f"like you do by using Markov chains. Whenever you "
                                        f"want to get a message from your stored Markov "
                                        f"chains, run /markov or "
                                        f"mention the bot. For more information, use "
                                        f"/help.")


def help(update, context):
    bot = context.bot
    logger.info(f'help cmd called by chat {update.effective_message.chat.id}')
    username = bot.get_me().username

    help_text = (
        "Welcome to MarkovBot, a Telegram bot that writes like you do using "
        "Markov chains!\n\n"
        "/help: {username} will generate a message.\n"
        "/remove: {username} will remove messages from chat.\n"
        "/version: {username} will state its current version.\n"
        "/start: {username} will display quickstart info.\n"
        "/help: {username} will print this help message!"
    )
    output_text = help_text.format(
        username=username,
    )
    update.effective_message.reply_text(output_text)


def generate_sentence(update, context):
    message = update.effective_message

    logger.info(f'sentence cmd called by chat {message.chat.id}')
    generated_message = speech.new_message(message.chat)
    update.effective_message.reply_text(generated_message)


def handle_message(update, context):
    bot = context.bot
    message = update.effective_message

    try:
        speech.update_model(message.chat, message.text)
    except ValueError as er:
        logger.error(er)
        return
    if f'@markovdoughbot' in message.text:
        generate_sentence(context, message)


def remove_messages(update, context):
    message = update.effective_message
    logger.info(f'remove cmd called by chat {message.chat.id}')
    speech.delete_model(message.chat)


def get_version(update, context):
    message = update.effective_message

    logger.info(f'version cmd called by chat {message.chat.id}')
    update.effective_message.reply_text("2022.11.11")


# CHECK THE COMMANDS VARIABLE IN THE TOP OF THIS FILE
if __name__ == "__main__":
    # Set these variable to the appropriate values
    TOKEN = os.environ.get('TOKEN')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
    PORT = os.environ.get('PORT')
    EXT_PORT = os.environ.get('EXT_PORT')

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # Add handlers
    # CHECK THE COMMANDS VARIABLE IN THE TOP OF THIS FILE
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('markov', generate_sentence))
    dp.add_handler(CommandHandler('remove', remove_messages))
    dp.add_handler(CommandHandler('version', get_version))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url="https://{}:{}/{}".format(WEBHOOK_URL, EXT_PORT, TOKEN))
    updater.start_polling()
    updater.idle()


import telebot
from validator_monitor import restart_validator, update_validator
# Set up the Telegram bot
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I'm a validator monitoring bot. Use /help to see available commands.")

# Handle the '/help' command
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = "Available commands:\n"
    help_text += "/start - Start the bot\n"
    help_text += "/help - Display this help message\n"
    help_text += "/restart_validator - Restart the validator\n"
    help_text += "/update_validator - Update the validator to the latest version\n"
    bot.reply_to(message, help_text)

# Handle the '/restart_validator' command
@bot.message_handler(commands=['restart_validator'])
def handle_restart_validator(message):
    try:
        restart_validator()
        bot.reply_to(message, "Validator restarted.")
    except Exception as e:
        bot.reply_to(message, f"Error restarting validator: {str(e)}")

# Handle the '/update_validator' command
@bot.message_handler(commands=['update_validator'])
def handle_update_validator(message):
    try:
        update_validator()
        bot.reply_to(message, "Validator updated to the latest version.")
    except Exception as e:
        bot.reply_to(message, f"Error updating validator: {str(e)}")

# Start the bot
bot.polling()



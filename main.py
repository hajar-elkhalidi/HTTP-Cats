from telegram.ext import Application, CommandHandler, MessageHandler, filters
from commands import start_cmd, bot_dev, api_dev, images_src, http_status
from handlers import handle_msg
from errors import error_handler
from config import TOKEN

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_cmd))
    app.add_handler(CommandHandler('botdev', bot_dev))
    app.add_handler(CommandHandler('apidev', api_dev))
    app.add_handler(CommandHandler('imagesrc', images_src))
    app.add_handler(CommandHandler('httpstatus', http_status))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_msg))
    
    # Errors
    app.add_error_handler(error_handler)

    # Polls the bot
    print('Polling started...')
    app.run_polling(poll_interval=3)

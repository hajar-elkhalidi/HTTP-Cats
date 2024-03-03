from telegram import Update
from telegram.ext import ContextTypes, CallbackContext

async def start_cmd(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! 🐱\nSend me an HTTP status code to get a cat picture.\nYou can also use the following commands to get more information:\n\n🤖 /botdev - GET information about the developer of this bot\n🌐 /apidev - GET details about the API developer used by the bot\n🖼️ /imagesrc - GET the source of the images used by the bot\nℹ️ /httpstatus - GET more information about HTTP statuses\n\nEnjoy your time here! 👾")

async def bot_dev(update: Update, context: CallbackContext):
    github_username = "hajar-elkhalidi"
    github_link = f"https://github.com/{github_username}"
    message = f"🤖 Bot developed by 🐞 [hajar\_elkhalidi]({github_link})"
    await update.message.reply_text(message, parse_mode="MarkdownV2")
    
async def api_dev(update: Update, context: CallbackContext):
    message = "🌐 API developed by @rogeriopvl\nYou can check out [http\.cat](http://http\.cat) for HTTP status cats\!"
    await update.message.reply_text(message, parse_mode="MarkdownV2")

async def images_src(update: Update, context: CallbackContext):
    await update.message.reply_text("🖼️ Original Images by Tomomi Imura @girlie_mac")

async def http_status(update: Update, context: CallbackContext):
    origin_info = (
        "ℹ️ The origin of HTTP status codes:\n\nHTTP status codes are standardized by the Internet Engineering Task Force \(IETF\)\.\nThey are defined in various RFC \(Request for Comments\) documents\.\nYou can find more information about HTTP status codes and their meanings [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#information_responses)\."
    )
    await update.message.reply_text(origin_info, parse_mode="MarkdownV2")




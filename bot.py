import logging
import os
import png
from pyqrcode import QRCode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
TOKEN = "<YOUR API TOKEN>"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
start_msg = '''
<b>హాయ్ మిత్రమా </b>👋👋
<i>Qr కోడ్ జెనరేటర్ బోట్ కు స్వాగతం</i>
<i>ఏదైనా ఇమెయిల్ ID, టెక్స్ట్, url, Spotify పాట లింక్ మొదలైనవాటిని నాకు పంపండి, నేను దాని కోసం qr కోడ్‌ను రూపొందిస్తాను</i>
<b>డైరెక్ట్ మీడియా ఫైల్‌లకు మద్దతు లేదు</b>
<i>మీరు ఫైల్‌లకు నేరుగా లింక్‌ను ఎలా పంపవచ్చు సృష్టికర్త @MutyalaHarshith</i>
'''
help_msg = '''
<i> నాకు ఏదైనా ఇమెయిల్ ఐడి, వచనం, url మొదలైనవి పంపండి (మీడియా ఫైల్‌లు లేవు...)</i>
<i>నేను దాని కోసం Qr కోడ్‌ను రూపొందించి, మీకు పంపుతాను సృష్టికర్త @MutyalaHarshith</i>
'''


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_html(start_msg)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_html(help_msg)


def msg(update: Update, context: CallbackContext) -> None:
    """qr కోడ్‌ని పొందడానికి ఏదైనా టెక్స్ట్ లేదా urlని పంపండి సృష్టికర్త @MutyalaHarshith"""
    text = update.message.text
    message_id = update.message.message_id
    qr_file = f'{message_id}.png'
    try:
        update.message.reply_text("ఉత్పత్తి చేస్తోంది")
        Qr_Code = QRCode(text)
        Qr_Code.png(qr_file, scale=10)
        update.message.reply_photo(photo=open(
            qr_file, "rb"), reply_to_message_id=message_id, caption=f"దీని ద్వారా రూపొందించబడిన మీ Qr కోడ్ ఇక్కడ ఉంది సృష్టికర్త @MutyalaHarshith మరియు మీ వచనం »'{text}'")
        update.message.reply_text("Finished")
        os.remove(qr_file)
    except Exception:
        update.message.reply_text("దయచేసి తర్వాత మళ్లీ ప్రయత్నించండి")


def main():
    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, msg))
    # Start The bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(
        "https://<YOUR APP NAME>.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()

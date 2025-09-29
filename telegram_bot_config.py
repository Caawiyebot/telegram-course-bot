import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

logging.basicConfig(
    format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

courses_data = {
    'ai_shopify': {
        'title': 'AI Shopify Store Pro: Samee Dukaan Online oo Fudud 30 Daqiiqo Gudahool!',
        'description': 'Baro sida loo dhiso dukaankaaga Shopify adigoo isticmaalaya AI, oo ay ku jiraan dropshipping iyo maamulka lacagaha. Waxaad ku baran doontaa sida loo sameeyo dukaankaaga online-ka ah 30 daqiiqo gudahood!',
        'topics': [
            'Hordhac Shopify iyo Dropshipping',
            'Diiwaangelin: Ku bilow $1 bilaha hore',
            'Web AI Builder: Dukaankaaga 30 Daqiiqo Gudahood',
            'Xeerarka iyo Habka loo diiwaangaliyo Store-kaaga',
            'Ku dar App-ka Shopify',
            'API: Ku xir Teknoolajiyada casriga ah',
            'Lacagaha: Habka loo maamulo lacag-bixinta',
            'Themes: Ka dhiso dukaankaaga mid gaar ah',
            'Domain: U beddel magacaaga gaarka ah',
            'Dropshipping: Sidee loo bilaabaa?',
            'Ku dar Zendrop: App Dropshipping ugu fiican',
            'Habayn: Sida loogu shaqeeyo Zendrop Settings',
            'Isticmaalka ugu horreeya ee App Dropshipping',
            'Sida alaabta hal mar loogu shubo Store',
            'Ku Boost garee alaabtaada Shopify',
            'Faahfaahinta guud ee Zendrop iyo dropshipping'
        ]
    },
    'custom_chatbot': {
        'title': 'Custom Chatbot AI Automation',
        'description': 'Baro sida loo dhiso oo loo maamulo chatbot-yo AI ah oo gaar ah, kuwaas oo otomaatig ka dhigaya hawlahaaga.',
        'topics': [
            'Hordhac Chatbot AI Automation',
            'Qorshaynta iyo Naqshadaynta Chatbot-ka',
            'Dhismaha Chatbot-ka oo la isticmaalayo aaladaha kala duwan',
            'Ku xiridda Chatbot-ka API-yada kala duwan',
            'Bixinta iyo Dib-u-eegista Xogta',
            'Tijaabinta iyo Hagaajinta Chatbot-ka'
        ]
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user.first_name}")
    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Welcome to the NLA Course Bot. Type /courses to see available courses.')

async def courses(update: Update, context: ContextTypes.DATA_TYPE):
    logging.info(f"Received /courses command from {update.effective_user.first_name}")
    keyboard = [
        [InlineKeyboardButton("AI Shopify Store Pro", callback_data=\


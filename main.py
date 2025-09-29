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
        'title': 'AI Shopify Store Pro',
        'description': 'Baro sida loo dhiso dukaankaaga Shopify adigoo isticmaalaya AI, oo ay ku jiraan dropshipping iyo maamulka lacagaha. Waxaad ku baran doontaa sida loo sameeyo dukaankaaga online-ka ah 30 daqiiqo gudahood!',
        'topics': [
            'Hordhac Shopify iyo Dropshipping',
            'Diiwaangelin: Ku bilow $1 bilaha hore',
            'Web AI Builder: Dukaankaaga 30 Daqiiqo Gudahood',
            'Xeerarka iyo Habka loo diiwaangaliyo Store-kaaga',
            'Ku dar App-ka Shopify',
            'API: Ku xir Teknoolajiyada casriga ah',
            'Lacagaha: Habka loo maamulo lacag-bixinta',
            'Themes: Ka dhig dukaankaaga mid gaar ah',
            'Domain: U beddel magacaaga gaarka ah',
            'Dropshipping: Sidee loo bilaabaa?',
            'Ku dar Zendrop: App Dropshipping ugu fiican',
            'Sida loo maareeyo Zendrop Settings',
            'Isticmaalka ugu horreeya ee App Dropshipping',
            'Sida alaabta hal mar loogu shubo Store',
            'Ku Boost garee alaabtaada Shopify',
            'Faahfaahinta guud ee Zendrop iyo dropshipping'
        ],
        'link': 'https://teletype.in/@somallibooks/21_0_0Yjtbl'
    },
    'custom_chatbot': {
        'title': 'Custom Chatbot AI Automation',
        'description': 'Baro sida loo dhiso oo loo maamulo chatbot-yo AI ah oo gaar ah, kuwaas oo otomaatig ka dhigaya hawlahaaga.',
        'topics': [
            'Hordhac Chatbot AI Automation',
            'Qorshaynta iyo Naqshadaynta Chatbot-ka',
            'Dhismaha Chatbot-ka oo la isticmaalayo aaladaha kala duwan',
            'Ku xiridda Chatbot-ka API-yada kale',
            'Bixinta iyo Dib-u-eegista Xogta',
            'Tijaabinta iyo Hagaajinta Chatbot-ka'
        ]
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /start command from {update.effective_user.first_name}")
    main_menu_keyboard = [
        [InlineKeyboardButton("📚 Koorsooyin", callback_data='show_courses')],
        [InlineKeyboardButton("👨‍💻 Talk Human", callback_data='talk_human')],
        [InlineKeyboardButton("🤖 Talk Bot", callback_data='talk_bot')],
        [InlineKeyboardButton("🛂 Contacts", callback_data='contacts')],
        [InlineKeyboardButton("❓ More Info", callback_data='more_info')],
        [InlineKeyboardButton("☘️ Ibara AI", callback_data='ibara_ai')]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Welcome to the Course Bot.', reply_markup=reply_markup)

async def show_courses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received show_courses_menu callback from {update.effective_user.first_name}")
    keyboard = []
    for key, course in courses_data.items():
        keyboard.append([InlineKeyboardButton(course["title"], callback_data=f'info_{key}')])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('Fadlan dooro koorso:', reply_markup=reply_markup)

async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Received /courses command from {update.effective_user.first_name}")
    keyboard = []
    for key, course in courses_data.items():
        keyboard.append([InlineKeyboardButton(course["title"], callback_data=f'info_{key}')])
    keyboard.append([InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Fadlan dooro koorso:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    if callback_data == 'main_menu':
        main_menu_keyboard = [
            [InlineKeyboardButton("📚 Koorsooyin", callback_data='show_courses')],
            [InlineKeyboardButton("👨‍💻 Talk Human", callback_data='talk_human')],
            [InlineKeyboardButton("🤖 Talk Bot", callback_data='talk_bot')],
            [InlineKeyboardButton("🛂 Contacts", callback_data='contacts')],
            [InlineKeyboardButton("❓ More Info", callback_data='more_info')],
            [InlineKeyboardButton("☘️ Ibara AI", callback_data='ibara_ai')]
        ]
        reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
        await query.edit_message_text(text='Welcome to the Course Bot.', reply_markup=reply_markup)
    elif callback_data == 'show_courses':
        await show_courses_menu(update, context)
    elif callback_data.startswith('info_'):
        course_key = callback_data.replace('info_', '')
        if course_key in courses_data:
            course = courses_data[course_key]
            message = f'**{course["title"]}**\n\n'
            message += f'{course["description"]}\n\n'
            message += '**Mawduucyada Koorsooyinka:**\n'
            for i, topic in enumerate(course['topics']):
                message += f'{i+1}. {topic}\n'
            if 'link' in course:
                message += f'\n**Ku biir koorsada:** [Halkan ka riix]({course["link"]})'
            
            # Add back button
            back_keyboard = [[InlineKeyboardButton("⬅️ Back to Courses", callback_data='show_courses')]]
            reply_markup = InlineKeyboardMarkup(back_keyboard)
            await query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)
        else:
            await query.edit_message_text(text='Koorsooyinkaas lama helin. Fadlan hubi magaca koorsada.')
    elif callback_data == 'talk_human':
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(text='Fadlan sug inta aan kugu xirayo qofka ku caawinaya. \n\nFadlan la xiriir: @M_F_A_R_A_T_O_O_N', reply_markup=reply_markup)
    elif callback_data == 'talk_bot':
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(text='Waxaan ahay bot, waxaan ku siin karaa macluumaad ku saabsan koorsooyinka. \n\nFadlan isticmaal amarka /courses si aad u aragto koorsooyinka.', reply_markup=reply_markup)
    elif callback_data == 'contacts':
        contacts_keyboard = [
            [InlineKeyboardButton("📱 Gudoomiye M Yasin Telegram", url="https://t.me/Mfaratoon")],
            [InlineKeyboardButton("📞 WhatsApp Number", url="https://wa.me/15873064137")],
            [InlineKeyboardButton("🤖 AI BOT (Automation) 4 Days Course", url="https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM")],
            [InlineKeyboardButton("🎬 AI Video Editing", url="https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq")],
            [InlineKeyboardButton("📹 Loom Free Screen Recording", url="https://loom.com/invite/f510cb6235b947838f247150307bfbeb")],
            [InlineKeyboardButton("🎓 Fasalka Barashada AI", url="https://chat.whatsapp.com/CEDDPttA5a4K6ZkQsDp4ah")],
            [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(contacts_keyboard)
        await query.edit_message_text(text='Waxaad naga heli kartaa goobahan:', reply_markup=reply_markup)
    elif callback_data == 'more_info':
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(text='Wixii macluumaad dheeraad ah, fadlan booqo website-kayaga: www.mfaratoon.com', reply_markup=reply_markup)
    elif callback_data == 'ibara_ai':
        back_keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(text='Waxaad ka heli kartaa macluumaad ku saabsan Ibara AI adigoo booqanaya: www.ibara.ai', reply_markup=reply_markup)

if __name__ == '__main__':
    application = ApplicationBuilder().token("6265456404:AAHq5Y1ITY2BW7PalmkMw0m6Er2cjuVkHbk").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("courses", courses))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()


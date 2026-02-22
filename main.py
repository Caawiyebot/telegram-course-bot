import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from openai import OpenAI

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# States for conversation
AI_CHAT = 1

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
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(
        f"Received /start command from {update.effective_user.first_name}")
    main_menu_keyboard = [
        [InlineKeyboardButton("📚 Koorsooyin", callback_data='show_courses')],
        [InlineKeyboardButton("🤖 La Hadal AI", callback_data='ai_chat')],
        [InlineKeyboardButton("👨‍💻 Talk Human", callback_data='talk_human')],
        [InlineKeyboardButton("🛂 Contacts", callback_data='contacts')],
        [InlineKeyboardButton("❓ More Info", callback_data='more_info')],
        [InlineKeyboardButton("☘️ Ibara AI", callback_data='ibara_ai')]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Welcome to the Course Bot.', reply_markup=reply_markup)


async def show_courses_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(
        f"Received show_courses_menu callback from {update.effective_user.first_name}")
    keyboard = [
        [InlineKeyboardButton("🆓 Free", callback_data='free_courses')],
        [InlineKeyboardButton("💰 Paid", callback_data='paid_courses')],
        [InlineKeyboardButton("⬅️ Back to Main Menu",
                              callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text('Fadlan dooro nooca koorsada:', reply_markup=reply_markup)


async def show_free_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🤖 AI Chatbot", callback_data='ai_chatbot')],
        [InlineKeyboardButton("🎬 AI Video Editing",
                              callback_data='ai_video_editing')],
        [InlineKeyboardButton("🛒 AI Shopify", callback_data='ai_shopify')],
        [InlineKeyboardButton("🎥 Adobe Premiere Pro",
                              callback_data='adobe_premiere')],
        [InlineKeyboardButton("📖 Basic Language",
                              callback_data='basic_language')],
        [InlineKeyboardButton("📚 Intermediate Language",
                              callback_data='intermediate_language')],
        [InlineKeyboardButton("🧠 Learn AI", callback_data='learn_ai')],
        [InlineKeyboardButton("⬅️ Back to Courses",
                              callback_data='show_courses')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "Waxaan bixinaa koorsooyin ugu horreeya ee Soomaalida ah oo ku saabsan abuurista chatbot-yo ku hadla luqadaada, oo aan u baahnayn aqoon barnaamij. Tani waa isbeddel caalami ah, waxaanan kaa caawin doonaa inaad isticmaasho AI telefoonkaaga ama kombuyuutarkaaga si aad u abuurto AI chatbot-yo iyo tafariiqda fiidiyowga adigoo isticmaalaya AI."
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)


async def show_paid_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "📱 WhatsApp Group", url="https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM")],
        [InlineKeyboardButton("📞 Contact @Mfaratoon",
                              url="https://t.me/Mfaratoon")],
        [InlineKeyboardButton(
            "🏘️ WhatsApp Community", url="https://chat.whatsapp.com/CEDDPttA5a4K6ZkQsDp4ah")],
        [InlineKeyboardButton("⬅️ Back to Courses",
                              callback_data='show_courses')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "Waxaa jira koorsooyin premium ah oo leh khidmad yar oo bishii la bixiyo. Tani waxay ku siinaysaa casharrada gaarka ah afar habeen todobaadkii. La xiriir macallinka iyo kooxda AI iyada oo loo marayo kanaaladan:"
    await update.callback_query.edit_message_text(message, reply_markup=reply_markup)


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(
        f"Received /courses command from {update.effective_user.first_name}")
    await show_courses_menu(update, context)


async def ai_chat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start AI chat mode"""
    logging.info(
        f"User {update.effective_user.first_name} started AI chat")
    context.user_data['ai_chat_mode'] = True
    context.user_data['chat_history'] = []

    back_keyboard = [[InlineKeyboardButton(
        "⬅️ Ku Noqo Menu", callback_data='ai_chat_back')]]
    reply_markup = InlineKeyboardMarkup(back_keyboard)
    await update.callback_query.edit_message_text(
        "🤖 **AI Taliyaha Adigu Ku Hadal!**\n\n"
        "Waxaan kaasoo ah AI taliyah oo lagu isticmaali karo in lagu jawaabio su'aalaha ardada iyo " +
        "buug ahaan ama wax iska warran.\n\n"
        "Fadlan qor su'aalahaaga oo aan kugu jawaabin doono! ✍️\n\n"
        "Markad dhamaatid, puusy 'Ku Noqo Menu' sidii aad doonaysid.",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
    return AI_CHAT


async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages in AI chat mode"""
    if not context.user_data.get('ai_chat_mode'):
        return

    user_message = update.message.text
    user_name = update.effective_user.first_name

    logging.info(f"AI Chat - {user_name}: {user_message}")

    # Show typing indicator
    await update.message.chat.send_action("typing")

    try:
        # Add user message to history
        if 'chat_history' not in context.user_data:
            context.user_data['chat_history'] = []

        context.user_data['chat_history'].append({
            "role": "user",
            "content": user_message
        })

        # Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context.user_data['chat_history'],
            max_tokens=500,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content

        # Add AI response to history
        context.user_data['chat_history'].append({
            "role": "assistant",
            "content": ai_response
        })

        # Keep only last 10 messages to avoid token limit
        if len(context.user_data['chat_history']) > 20:
            context.user_data['chat_history'] = context.user_data['chat_history'][-20:]

        # Send response
        await update.message.reply_text(ai_response)

    except Exception as e:
        logging.error(f"Error in AI chat: {str(e)}")
        await update.message.reply_text(
            f"❌ Waxaa dhacday khalad: {str(e)}\n\n"
            "Fadlan isku day mar kale."
        )

    return AI_CHAT


async def handle_ai_chat_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Go back from AI chat to main menu"""
    context.user_data['ai_chat_mode'] = False
    context.user_data['chat_history'] = []

    query = update.callback_query
    await query.answer()

    main_menu_keyboard = [
        [InlineKeyboardButton("📚 Koorsooyin", callback_data='show_courses')],
        [InlineKeyboardButton("🤖 La Hadal AI", callback_data='ai_chat')],
        [InlineKeyboardButton("👨‍💻 Talk Human", callback_data='talk_human')],
        [InlineKeyboardButton("🛂 Contacts", callback_data='contacts')],
        [InlineKeyboardButton("❓ More Info", callback_data='more_info')],
        [InlineKeyboardButton("☘️ Ibara AI", callback_data='ibara_ai')]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
    await query.edit_message_text(text='Welcome to the Course Bot.', reply_markup=reply_markup)


async def courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(
        f"Received /courses command from {update.effective_user.first_name}")
    await show_courses_menu(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    callback_data = query.data
    if callback_data == 'main_menu':
        main_menu_keyboard = [
            [InlineKeyboardButton(
                "📚 Koorsooyin", callback_data='show_courses')],
            [InlineKeyboardButton(
                "🤖 La Hadal AI", callback_data='ai_chat')],
            [InlineKeyboardButton(
                "👨‍💻 Talk Human", callback_data='talk_human')],
            [InlineKeyboardButton("🛂 Contacts", callback_data='contacts')],
            [InlineKeyboardButton("❓ More Info", callback_data='more_info')],
            [InlineKeyboardButton("☘️ Ibara AI", callback_data='ibara_ai')]
        ]
        reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
        await query.edit_message_text(text='Welcome to the Course Bot.', reply_markup=reply_markup)
    elif callback_data == 'show_courses':
        await show_courses_menu(update, context)
    elif callback_data == 'ai_chat':
        await ai_chat_start(update, context)
    elif callback_data == 'ai_chat_back':
        await handle_ai_chat_back(update, context)
    elif callback_data == 'free_courses':
        await show_free_courses(update, context)
    elif callback_data == 'paid_courses':
        await show_paid_courses(update, context)
    elif callback_data == 'ai_chatbot':
        keyboard = [
            [InlineKeyboardButton("📚 AI Automation and Chatbots Course",
                                  url="https://open.substack.com/pub/mfaratoon/p/koorsada-ai-automation-and-chatbots?r=ogczv&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true")],
            [InlineKeyboardButton(
                "📝 Register Here", url="https://teletype.in/@somallibooks/21_0_0Yjtbl")],
            [InlineKeyboardButton(
                "📚 Lesson", url="https://t.me/+eJxxMKtunMcwODhk")],
            [InlineKeyboardButton(
                "💬 WhatsApp Group", url="https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Halkan waxaad ku baran doontaa sida loo abuuro chatbot-yo aamusan oo aan hore u lahayn khibrad IT ama barnaamij. Tani waxay ku jirtaa abuurista Telegram, WhatsApp, iyo Messenger chatbot-yo gaar ah."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'ai_video_editing':
        keyboard = [
            [InlineKeyboardButton("🎬 9 AI Video Editing Lessons",
                                  url="https://open.substack.com/pub/mfaratoon/p/9-cashar-ai-video-editing?r=ogczv&utm_campaign=post&utm_medium=web&showWelcomeOnShare=true")],
            [InlineKeyboardButton(
                "💬 WhatsApp Group", url="https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Waxaa jira sagaal cashar oo bilaash ah oo daboolaya hababka ugu dambeeyay ee tafariiqda fiidiyowga adigoo isticmaalaya adeegyo iyo websaydhyo casri ah. Waxaan si faahfaahsan uga hadli doonaa kuwan sagaalka cashar."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'ai_shopify':
        keyboard = [
            [InlineKeyboardButton(
                "🛒 Ku biir koorsada", url="https://teletype.in/@somallibooks/21_0_0Yjtbl")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        course = courses_data['ai_shopify']
        message = f'**{course["title"]}**\n\n'
        message += f'{course["description"]}\n\n'
        message += '**Mawduucyada Koorsooyinka:**\n'
        for i, topic in enumerate(course['topics']):
            message += f'{i+1}. {topic}\n'
        await query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)
    elif callback_data == 'adobe_premiere':
        keyboard = [
            [InlineKeyboardButton("📱 Telegram Group",
                                  url="https://t.me/Mfaratoon")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Qaybtan waxay ka kooban tahay casharrada fudud iyo aasaasiga ah ee sharaxaya ama bara tafariiqda fiidiyowga aasaasiga ah adigoo isticmaalaya Adobe Premiere Pro CC 2020. Koorsadani waxay loogu talagalay kuwa doonaya inay bartaan aasaasiga waxayna si fiican u baran karaan iyada oo loo marayo koorsadan aasaasiga ah."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'basic_language':
        keyboard = [
            [InlineKeyboardButton("📘 @somalienglish3",
                                  url="https://t.me/somalienglish3")],
            [InlineKeyboardButton(
                "🤖 @maseexatobot", url="https://t.me/maseexatobot")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Fasalkan waa mid aasaasi ah, casharradana waxaa bara macallimiin Soomaali ah oo iskaa u tabarucay walaalahoodii. Fadlan eeg ID-ga hoose.\n\nSidoo kale, bot-ka @maseexatobot ayaa kaa caawin doona. Fadlan had iyo jeer isticmaal calaamadda \"/\" markaad furto bot-ka."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'intermediate_language':
        keyboard = [
            [InlineKeyboardButton("📚 @somalienglish1",
                                  url="https://t.me/somalienglish1")],
            [InlineKeyboardButton(
                "🤖 @maseexatobot", url="https://t.me/maseexatobot")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Waxaan haynaa fasallo bilaash ah oo Soomaali-Ingiriisi ah oo loogu talagalay kuwa iskood wax u barata. Waxaad ka heli kartaa koorsooyin iyo fasallo bilaash ah, oo leh 39k, 15k, iyo 10k arday Soomaali ah.\n\nHaddii aad tahay heer dhexe luqadda, fasal luqad dhexe ayaa hadda socda oo si weyn u hagaajin doona barashada luqadda heerka dhexe."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'learn_ai':
        keyboard = [
            [InlineKeyboardButton(
                "🎓 Classroom", url="https://t.me/+eJxxMKtunMcwODhk")],
            [InlineKeyboardButton(
                "📚 Google Classrooms", url="https://classroom.google.com/c/ODAzMzUwNDIyOTU0?cjc=sdvvlyc2")],
            [InlineKeyboardButton("⬅️ Back", callback_data='free_courses')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "Waxaa jira meelo badan oo aan ku bixinno casharrada bilaash ah ee AI automation iyo chatbot-yada, iyo sidoo kale wararka ugu dambeeyay ee AI. Kuwani waa qaar ka mid ah meelaha haddii aad xiisaynayso.\n\nGaar ahaan, haddii aad ku biirto fasalka Telegram, bot-ku wuxuu ka kooban yahay casharrada. Kaliya waxaad u baahan tahay inaad codsato, oo markaad ku biirto, waxaan qori doonaa tirooyinka sida \"cashar 1\" ama \"cashar 2\" ilaa 8 cashar oo isku xiran oo aad daawan karto, oo dhammaantood ku saabsan AI chatbot-yada."
        await query.edit_message_text(message, reply_markup=reply_markup)
    elif callback_data == 'talk_human':
        keyboard = [
            [InlineKeyboardButton("📱 Telegram: @Mfaratoon",
                                  url="https://t.me/Mfaratoon")],
            [InlineKeyboardButton(
                "🤖 AI BOT Course", url="https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM")],
            [InlineKeyboardButton(
                "🎬 AI Video Editing", url="https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq")],
            [InlineKeyboardButton(
                "🎓 AI Learning Class", url="https://chat.whatsapp.com/CEDDPttA5a4K6ZkQsDp4ah")],
            [InlineKeyboardButton(
                "🎥 AI Training Team", url="https://loom.com/invite/f510cb6235b947838f247150307bfbeb")],
            [InlineKeyboardButton(
                "🔧 @Ogaysiiyebot", url="https://t.me/Ogaysiiyebot")],
            [InlineKeyboardButton("🔧 @fogaanaragbot",
                                  url="https://t.me/fogaanaragbot")],
            [InlineKeyboardButton("⬅️ Back to Main Menu",
                                  callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = "**Macluumaadka Xiriirka**\n\n💬 **WhatsApp Qolal:**\n🔥 **Maamul bot-kaaga:** @Ogaysiiyebot ama @fogaanaragbot"
        await query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)
    elif callback_data == 'contacts':
        contacts_keyboard = [
            [InlineKeyboardButton(
                "📱 Gudoomiye M Yasin Telegram", url="https://t.me/Mfaratoon")],
            [InlineKeyboardButton("📞 WhatsApp Number",
                                  url="https://wa.me/15873064137")],
            [InlineKeyboardButton("🤖 AI BOT (Automation) 4 Days Course",
                                  url="https://chat.whatsapp.com/KzkcjwraeYhCsUXaexgNyM")],
            [InlineKeyboardButton(
                "🎬 AI Video Editing", url="https://chat.whatsapp.com/DIu9h23H5R28ozxfMFTkdq")],
            [InlineKeyboardButton("📹 Loom Free Screen Recording",
                                  url="https://loom.com/invite/f510cb6235b947838f247150307bfbeb")],
            [InlineKeyboardButton(
                "🎓 Fasalka Barashada AI", url="https://chat.whatsapp.com/CEDDPttA5a4K6ZkQsDp4ah")],
            [InlineKeyboardButton("⬅️ Back to Main Menu",
                                  callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(contacts_keyboard)
        await query.edit_message_text(text='Waxaad naga heli kartaa goobahan:', reply_markup=reply_markup)
    elif callback_data == 'more_info':
        keyboard = [
            [InlineKeyboardButton(
                "📝 Isqor Koorsooyin", url="https://www.jotform.com/agent/01982620386371ba9336e5f880caada9e1e8")],
            [InlineKeyboardButton("⬅️ Back to Main Menu",
                                  callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """**Koorsooyinka aan bixino waxaa ka mid ah:**

🎬 **AI Video Editing** - Bilaash
💻 **Python Afsomali-Basic**
🌐 **AI Web Designing**
🤖 **AI ChatGPT-Prompt {Basic}+**
📲 **Instagram Automation Business Bot**
📸 **Telegram Automation Business Bot**
📞 **Messenger Automation Business Bot**

**Koorsooyinka aan 4 ka mid ah koorsooyin dhamaan free ayaa ka dhignay, Koorsooyinkaas oo dhan 2 Sano Fasax ayaa ka dhignay Dhalinyar waad u qalataan ee ka faa,iidaysta aniga rate fiican naga bixiya intaasaa naga badan sxbyaal lacagtana ka qaalisan.**

Waxaa jira qaar ka mid ah koorsooyinka oo bilaash ah, tusaale ahaan AI Video Editing. Haddii aad xiiseyneyso, waxaan ku siin karaa macluumaad dheeri ah oo ku saabsan sida loo isqoro iyo shuruudaha koorsada. 

Waxaan ku faraxsanahay inaad bilowday safarkaaga barashada automation iyo AI, taasoo fursado badan kuu horseedi karta mustaqbalka shaqo."""
        await query.edit_message_text(text=message, parse_mode='Markdown', reply_markup=reply_markup)
    elif callback_data == 'ibara_ai':
        back_keyboard = [[InlineKeyboardButton(
            "⬅️ Back to Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(back_keyboard)
        await query.edit_message_text(text='Waxaad ka heli kartaa macluumaad ku saabsan Ibara AI adigoo booqanaya: www.ibara.ai', reply_markup=reply_markup)

if __name__ == '__main__':
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("courses", courses))

    # Message handler for AI chat
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_ai_message))

    # Callback query handler for buttons
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

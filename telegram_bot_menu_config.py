```python




menu_options = {
    'Talk Human': 'talk_human',
    'Talk Bot': 'talk_bot',
    'Contacts': 'contacts',
    'More Info': 'more_info',
    'Ibara AI': 'ibara_ai'
}

menu_buttons = [
    [InlineKeyboardButton(text, callback_data=data)] for text, data in menu_options.items()
]

reply_markup_main_menu = InlineKeyboardMarkup(menu_buttons)



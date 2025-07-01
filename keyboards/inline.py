from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📩 SMS yuborish", callback_data="send_sms")],
    [InlineKeyboardButton(text="📞 Telefon qilish", callback_data="make_call")]
])

back_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Orqaga", callback_data="main_menu")]
])

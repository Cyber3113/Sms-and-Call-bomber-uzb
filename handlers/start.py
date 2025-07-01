from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from database import add_user, get_user, update_phone
from keyboards.inline import main_menu

router = Router()

@router.message(Command("start"))  # ✅ to‘g‘ri usul
async def start_handler(msg: types.Message):
    user = msg.from_user
    add_user(user.id, user.first_name, user.last_name, user.username)
    
    user_data = get_user(user.id)
    if user_data and not user_data[4]:  # 5 - phone
        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await msg.answer("📞 Iltimos, telefon raqamingizni yuboring:", reply_markup=kb)
    else:
        await msg.answer("👋 Xush kelibsiz! Quyidagilardan birini tanlang:", reply_markup=main_menu)

@router.message(lambda m: m.contact)  
async def save_contact(msg: types.Message):
    if msg.from_user.id != msg.contact.user_id:
        return  # Faqat o‘zining raqamini qabul qilamiz

    update_phone(msg.from_user.id, msg.contact.phone_number)
    await msg.answer("✅ Raqamingiz qabul qilindi. Endi botdan foydalanishingiz mumkin!", reply_markup=main_menu)



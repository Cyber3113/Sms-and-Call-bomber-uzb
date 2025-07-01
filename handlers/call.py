from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.inline import back_button
from states.user_states import CallState
import uuid
import requests
import os
from config import CALL_API_URL1

URL = CALL_API_URL1

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

router = Router()


@router.callback_query(F.data == "make_call")
async def ask_phone(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📞 Qo‘ng‘iroq qilish uchun telefon raqamingizni kiriting:\n\nMasalan: +998901234567", reply_markup=back_button)
    await state.set_state(CallState.phone)


@router.message(CallState.phone)
async def check_and_call(msg: types.Message, state: FSMContext):
    raw_phone = msg.text.strip()

    if not (raw_phone.startswith("+998") and raw_phone[1:].isdigit() and len(raw_phone) == 13):
        await msg.answer("❌ Telefon raqam noto‘g‘ri! Iltimos, +998901234567 ko‘rinishida kiriting.", reply_markup=back_button)
        return

    # "+" belgisi olib tashlanadi
    phone = raw_phone.lstrip("+")

    await msg.answer("⏳ Qo‘ng‘iroq uchun so‘rov yuborilmoqda...")

    try:
        # Qadam 1: Register qilish
        device_id_request_id = str(uuid.uuid4())
        imei = uuid.uuid4().hex

        register_payload = {
            "id": device_id_request_id,
            "jsonrpc": "2.0",
            "method": "device.register.request",
            "params": {
                "app_version": "1.0",
                "device_info": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "device_name": "Windows",
                "device_type": 3,
                "imei": imei,
                "phone_number": phone
            }
        }

        response1 = requests.post(URL, json=register_payload, headers=HEADERS)
        result_json = response1.json()

        if "result" not in result_json or "device_id" not in result_json["result"]:
            raise Exception("❌ Click API device_id qaytarmadi.")

        device_id = result_json["result"]["device_id"]

        # Qadam 2: IVR qo‘ng‘iroq qilish
        ivr_payload = {
            "id": str(uuid.uuid4()),
            "jsonrpc": "2.0",
            "method": "call.ivr",
            "params": {
                "device_id": device_id
            }
        }

        response2 = requests.post(URL, json=ivr_payload, headers=HEADERS)
        result2 = response2.json()
        print(result2)

        if "result" in result2:
            await msg.answer(f"✅ {raw_phone} raqamiga qo‘ng‘iroq yuborildi.")
        else:
            await msg.answer("❌ Qo‘ng‘iroq yuborishda xatolik yuz berdi.")
    except Exception as e:
        await msg.answer(f"⚠️ Xatolik: {str(e)}")

    await state.clear()

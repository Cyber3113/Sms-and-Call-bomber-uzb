from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.inline import back_button, main_menu
from states.user_states import SMSState
import httpx
import asyncio
from config import SMS_API_URL1, SMS_API_URL2, SMS_API_URL5, SMS_API_URL6, SMS_API_URL7, CALL_API_URL1

router = Router()

@router.callback_query(F.data == "send_sms")
async def ask_phone(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("📩 SMS yuborish uchun telefon raqamingizni kiriting:\nMasalan: +998901234567", reply_markup=back_button)
    await state.set_state(SMSState.phone)

@router.message(SMSState.phone)
async def check_phone(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    if not (phone.startswith("+998") and phone[1:].isdigit() and len(phone) == 13):
        await msg.answer("❌ Telefon raqam formati noto‘g‘ri! Iltimos, +998901234567 ko‘rinishida kiriting.", reply_markup=back_button)
        return
    await state.update_data(phone=phone)  
    await msg.answer("Nechta SMS yuborilsin? (Maksimal 20 ta):")
    await state.set_state(SMSState.sms_count)

@router.message(SMSState.sms_count)
async def check_count(msg: types.Message, state: FSMContext):
    if not msg.text.isdigit():
        await msg.answer("❌ Iltimos, faqat raqam kiriting. Masalan: 3")
        return

    count = int(msg.text)
    if count > 20 or count < 1:
        await msg.answer("❌ 1 dan 20 gacha SMS yuborish mumkin.")
        return

    data = await state.get_data()
    phone = data['phone']             # +998 bilan
    phone_no_plus = phone[1:]         # 998 bilan

    await msg.answer(f"⏳ SMS yuborilmoqda...")

    success = 0
    try:
        async with httpx.AsyncClient() as client:
            # 1️⃣ API_URL1 - har doim
            await asyncio.sleep(0.5)
            r1 = await client.post(SMS_API_URL1, json={"phone": phone})
            if r1.status_code in [200, 201]:
                success += 1
            else:
                print("❌ API1:", r1.status_code, r1.text)

            remaining = count - 1

            # 2️⃣ API_URL5 - faqat 1 marta, agar remaining ≥ 1
            if remaining >= 1:
                await asyncio.sleep(0.5)
                payload5 = {
                    "phone": phone_no_plus,
                    "device": {
                        "type": "web",
                        "name": "Web Client",
                        "version": "1.0"
                    }
                }
                r5 = await client.post(SMS_API_URL5, json=payload5)
                if r5.status_code in [200, 201]:
                    success += 1
                else:
                    print("❌ API5:", r5.status_code, r5.text)
                remaining -= 1

            # 3️⃣ API_URL2 - keyingi 6 taga
            for i in range(min(6, remaining)):
                await asyncio.sleep(0.5)
                payload2 = {"phone_number": phone_no_plus}
                r2 = await client.post(SMS_API_URL2, json=payload2)
                if r2.status_code in [200, 201]:
                    success += 1
                else:
                    print(f"❌ API2-{i+1}:", r2.status_code, r2.text)
            remaining -= min(6, remaining)

            # 4️⃣ API_URL6 - qolganlarga
            payload6 = {
                "language": "uz",
                "role_id": "06d63125-e7a2-4616-afa4-cd50ee3ac33d",
                "source": "web",
                "username": phone
            }
            for i in range(remaining):
                await asyncio.sleep(0.5)
                r6 = await client.post(SMS_API_URL6, json=payload6)
                if r6.status_code in [200, 201]:
                    success += 1
                else:
                    print(f"❌ API6-{i+1}:", r6.status_code, r6.text)

    except Exception as e:
        print("⚠️ Umumiy xatolik:", str(e))

    await msg.answer(f"✅ {success} ta SMS {phone} raqamiga yuborildi.")
    await state.clear()




@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "👋 Xush kelibsiz! Quyidagilardan birini tanlang:",
        reply_markup=main_menu
    )

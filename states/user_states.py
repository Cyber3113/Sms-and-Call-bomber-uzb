from aiogram.fsm.state import State, StatesGroup

class SMSState(StatesGroup):
    phone = State()
    sms_count = State()

class CallState(StatesGroup):
    phone = State()

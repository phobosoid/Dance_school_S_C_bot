#!/usr/bin/env python3
import os, json, asyncio, logging
import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN      = "8044257387:AAEfquO4xTqG3xqCZk2OZtwRpa59SH_mCoU"
SPREADSHEET_ID = "1ErPr1xUMw-qbFIxFS9pFIxFS9Rjxs0HEqc-4zzf1myli5i8nO8"

# Читаем JSON-ключ из переменной окружения
creds_info = json.loads(os.environ["GOOGLE_CREDS_JSON"])
creds      = Credentials.from_service_account_info(creds_info, scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
gc         = gspread.authorize(creds)

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()

kb_main = ReplyKeyboardMarkup([[KeyboardButton("🗂️ Неделя")]], resize_keyboard=True)

@dp.message(CommandStart())
async def on_start(m: types.Message):
    await m.answer("Выберите «🗂️ Неделя»", reply_markup=kb_main)

@dp.message(F.text=="🗂️ Неделя")
async def week_view(m: types.Message):
    try:
        ws = gc.open_by_key(SPREADSHEET_ID).worksheet("Week")
    except Exception:
        logging.exception("Ошибка открытия Week")
        return await m.answer("Не удалось открыть вкладку «Week».")
    lines = []
    for cell in ("A1","B1","B3"):
        v = ws.acell(cell).value
        if v and v.strip(): lines.append(v.strip())
    for col in "CDEFGHI":
        v2,v3 = ws.acell(f"{col}2").value, ws.acell(f"{col}3").value
        if v2 and v3: lines.append(f"{v2.strip()} {v3.strip()}")
    await m.answer("\n".join(lines) if lines else "Данных нет.")

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__=="__main__":
    asyncio.run(main())

#!/usr/bin/env python3
import os
from flask import Flask, request
import gspread
from google.oauth2.service_account import Credentials
from aiogram import Bot, Dispatcher
from aiogram.types import Update

# — Настройки бота и таблицы —
BOT_TOKEN      = "8044257387:AAEfquO4xTqG3xqCZk2OZtwRpa59SH_mCoU"
SPREADSHEET_ID = "1ErPr1xUMw-qbFIxFS9Rjxs0HEqc-4zzf1myli5i8nO8"

# — Google Sheets API —
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "creds.json")

creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)
gc    = gspread.authorize(creds)
sheet = gc.open_by_key(SPREADSHEET_ID).sheet1  # первая вкладка

# — Flask + Aiogram —
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def cmd_start(msg: Update):
    await msg.reply("Привет! Отправьте /schedule, чтобы получить данные из Google Sheets.")

@dp.message_handler(commands=["schedule"])
async def cmd_schedule(msg: Update):
    # Читаем диапазон A1:B10
    data = sheet.get("A1:B10")
    text = "\n".join(f"{r[0]} — {r[1]}" for r in data if len(r) >= 2)
    if not text:
        text = "В таблице нет данных в ячейках A1:B10."
    await msg.reply(text)

@app.route(f"/webhook/{BOT_TOKEN}", methods=["POST"])
def webhook():
    upd = Update(**request.get_json(force=True))
    dp.loop.create_task(dp.process_update(upd))
    return "OK"

if __name__ == "__main__":
    # Для локального запуска
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

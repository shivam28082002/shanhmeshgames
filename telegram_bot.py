import aiohttp
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_BASE_URL = "http://127.0.0.1:8000/api"

user_tokens = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)
    username = update.effective_user.username or f"user_{telegram_id}"
    password = f"tg_{telegram_id}"

    # Step 1: Try to register
    async with aiohttp.ClientSession() as session:
        reg_response = await session.post(f"{API_BASE_URL}/register/", data={
            "username": username,
            "password": password
        })

        if reg_response.status == 201:
            await update.message.reply_text("Account created! Logging you in...")
        elif reg_response.status == 400:
            await update.message.reply_text("Account already exists. Logging you in...")
        else:
            await update.message.reply_text("Something went wrong during registration.")
            return

        # Step 2: Login to get token
        login_response = await session.post(f"{API_BASE_URL}/login/", data={
            "username": username,
            "password": password
        })

        if login_response.status == 200:
            access_token = (await login_response.json()).get("access")
            user_tokens[telegram_id] = access_token
            await update.message.reply_text("✅ Logged in successfully!")
        else:
            await update.message.reply_text("❌ Login failed.")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7585286219:AAGltBgrhw7MZy_9U3gDyjifCJ7D7LPewAk").build()
    app.add_handler(CommandHandler("start", start))
    print("Bot is running...")
    app.run_polling()

import os
import asyncio
import logging
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LEADER_CHANNEL_ID = os.getenv("LEADER_CHANNEL_ID")
ALLOWED_USERS = os.getenv("ALLOWED_USER_IDS", "").split(",")

bot = Bot(token=BOT_TOKEN)

async def notify_leader(text):
    try:
        await bot.send_message(chat_id=LEADER_CHANNEL_ID, text=text)
    except Exception as e:
        logging.error(f"Leader notify error: {e}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user_name = update.effective_user.first_name or "Unknown"
    
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ 你没有权限使用此系统。")
        return

    text = update.message.text or ""
    
    if text.startswith("搜寻") or text.startswith("search"):
        query = text.replace("搜寻", "").replace("search", "").strip()
        session_id = f"{user_name[:1]}-{asyncio.get_event_loop().time():.0f}"
        
        await update.message.reply_text(f"🦞 [{session_id}] 开始搜寻：{query}\n请稍等...")
        await notify_leader(f"🦞 [{session_id}] {user_name} 开始搜寻：{query}")
        
        # 搜寻逻辑（后续加入）
        await update.message.reply_text(f"✅ [{session_id}] 搜寻完成，功能开发中...")
        await notify_leader(f"✅ [{session_id}] {user_name} 搜寻完成：{query}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

import sqlite3
import logging
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# BOT CONFIG
# =========================

BOT_TOKEN = "8825249528:AAFuJMKb98WZB-xCx2bB01ecwBv1E7egVFc"
OWNER_ID = 8719135331  # Replace with your Telegram numeric User ID

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# =========================
# DATABASE
# =========================

def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_seen TEXT,
            last_active TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_user(user_id: int):
    now = datetime.now().isoformat()

    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, first_seen) VALUES (?, ?)",
        (user_id, now),
    )

    cursor.execute(
        "UPDATE users SET last_active = ? WHERE user_id = ?",
        (now, user_id),
    )

    conn.commit()
    conn.close()


# =========================
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user is None or update.message is None:
        return

    save_user(user.id)

    name = user.first_name or "User"

    welcome_text = (
        "👑 <b>WELCOME TO DILJOT BOT</b> 👑\n\n"
        f"👤 <b>User:</b> {name}\n"
        f"🆔 <b>User ID:</b> <code>{user.id}</code>\n\n"
        "🤖 <b>Bot Status:</b> 🟢 Online\n"
        "⚡ <b>System:</b> Ready\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "✨ Welcome! Choose an option below.\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    keyboard = [
        [
            InlineKeyboardButton("📖 Help", callback_data="help"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ]
    ]

    if user.id == OWNER_ID:
        keyboard.append([
            InlineKeyboardButton("👑 Owner Panel", callback_data="owner")
        ])

    await update.message.reply_text(
        welcome_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


# =========================
# /HELP
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 <b>HELP</b>\n\n"
        "/start — Open welcome menu\n"
        "/help — Show help\n"
        "/id — Show your Telegram ID\n"
        "/ping — Check bot status",
        parse_mode="HTML",
    )


# =========================
# /ID
# =========================

async def user_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user is None:
        return

    await update.message.reply_text(
        f"🆔 Your Telegram User ID:\n\n<code>{user.id}</code>",
        parse_mode="HTML",
    )


# =========================
# /PING
# =========================

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 <b>Pong!</b>\n🟢 Bot is online.", parse_mode="HTML")


# =========================
# INLINE BUTTONS
# =========================

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query is None:
        return

    await query.answer()

    if query.data == "help":
        await query.edit_message_text(
            "📖 <b>HELP</b>\n\n"
            "/start — Open welcome menu\n"
            "/help — Show help\n"
            "/id — Show your Telegram ID\n"
            "/ping — Check bot status",
            parse_mode="HTML",
        )

    elif query.data == "about":
        await query.edit_message_text(
            "🤖 <b>DILJOT BOT</b>\n\n"
            "A simple Telegram bot built with Python.\n"
            "🟢 Status: Online",
            parse_mode="HTML",
        )

    elif query.data == "owner":
        if query.from_user.id != OWNER_ID:
            await query.edit_message_text("⛔ Access denied.")
            return

        await query.edit_message_text(
            "👑 <b>OWNER PANEL</b>\n\n"
            "🟢 Bot: Online\n"
            f"🆔 Owner ID: <code>{OWNER_ID}</code>",
            parse_mode="HTML",
        )


# =========================
# MAIN
# =========================

def main():
    if BOT_TOKEN == "PASTE_YOUR_NEW_BOT_TOKEN_HERE":
        raise ValueError("Please add your BOT_TOKEN in the code.")

    if OWNER_ID == 123456789:
        raise ValueError("Please add your real OWNER_ID in the code.")

    init_db()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", user_id_command))
    application.add_handler(CommandHandler("ping", ping))
    application.add_handler(CallbackQueryHandler(button_callback))

    print("👑 DILJOT BOT is running...")
    application.run_polling()


if __name__ == "__main__":
    main()

import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API endpoint
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# AI response using Groq
async def ai_reply(prompt: str) -> str:
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
        )
        data = response.json()

        # Debug log
        print("Groq API response:", data)

        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        elif "error" in data:
            return f"Groq API Error: {data['error'].get('message', 'Unknown error')}"
        else:
            return f"Unexpected response: {data}"
    except Exception as e:
        return f"Error: {str(e)}"


# Handle Telegram messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    ai_response = await ai_reply(user_message)
    await update.message.reply_text(ai_response)

# Main bot setup
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Groq Telegram bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


import os
import asyncio
import httpx
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("أهلاً! ابعتلي سؤالك وبحاول جاوبك")

async def chat(update, context):
    try:
        async with httpx. AsyncClient(timeout=120) as client:
            response = await client.post(

headers={
                    "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": [
                        {"role": "user", "content": update.message.text}
                    ],
                },
            )
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"]["content"]

if not answer:
            answer = "ما وصلني رد، جرّب مرة تانية"
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i + 4000])
    except Exception:
        await update.message.reply_text("ما قدرت أجيب الرد، جرّب مرة تانية")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

server = HTTPServer(("0.0.0.0", int(os.environ.get("PORT", 10000))), HealthHandler)
Thread(target=server.serve_forever, daemon=True).start()

asyncio.set_event_loop(asyncio.new_event_loop())
app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN", "8898390953:AAH_nNWlDdE7ph4JhqIneU4exLm-S5ncOKk")

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    reminder_text = "🌸 **صلِّ على النبي ﷺ**"
    await context.bot.send_message(chat_id=job.chat_id, text=reminder_text, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if context.job_queue:
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in current_jobs:
            job.schedule_removal()
        context.job_queue.run_repeating(
            send_reminder,
            interval=3600,
            first=10,
            chat_id=chat_id,
            name=str(chat_id)
        )
    await update.message.reply_text("تم تشغيل التذكير بنجاح! سيتم إرسال تذكير كل ساعة.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

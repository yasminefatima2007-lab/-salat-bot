from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8898390953:AAH_nNWlDdE7ph4JhqIneU4exLm-S5ncOKk"

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    reminder_text = "🌸 **تذكير:** صَلِّ على النبي ﷺ\n«اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى نَبِيِّنَا مُحَمَّدٍ»"
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

    keyboard = [
        [InlineKeyboardButton("✨ فضل الصلاة على النبي", callback_data='fadl')],
        [InlineKeyboardButton("📖 صيغ الصلاة على النبي", callback_data='segh')],
        [InlineKeyboardButton("🌸 صَلِّ على النبي الآن", callback_data='salli')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = (
        "صلِّ على المختارِ في كلِّ وقتٍ وحين 🌺✨\n\n"
        "أهلاً بك في بوت الصلاة على النبي ﷺ.\n"
        "تم تفعيل التذكير التلقائي بالصلاة على النبي كل ساعة! 🔔\n\n"
        "اختر من القائمة أدناه:"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'fadl':
        text = (
            "✨ **من فضائل الصلاة على النبي ﷺ:**\n\n"
            "1️⃣ امتثال أمر الله تعالى.\n"
            "2️⃣ الحصول على 10 صلوات من الله مقابل كل صلاة.\n"
            "3️⃣ رفع 10 درجات وحط 10 خطيئات.\n"
            "4️⃣ سبب لكفاية الهم وغفران الذنب."
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'segh':
        text = (
            "📖 **صيغ للصلاة على النبي:**\n\n"
            "• **الصيغة الإبراهيمية:** (اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ، كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ).\n\n"
            "• **الصيغة المختصرة:** (اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ)."
        )
        await query.message.reply_text(text, parse_mode='Markdown')

    elif query.data == 'salli':
        text = "ﷺ اللَّهُمَّ صَلِّ وَسَلِّمْ وَبَارِكْ عَلَى نَبِيِّنَا مُحَمَّدٍ ﷺ"
        await query.message.reply_text(text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    
    print("بوت الصلاة على النبي يعمل الآن...")
    app.run_polling()

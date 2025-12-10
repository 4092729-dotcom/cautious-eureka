from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import Update
import logging
import datetime # 🆕 لإضافة دالة الوقت

# ==========================================================
# 1. مفتاح الوصول (التوكن)
# ==========================================================
# ⚠️ يجب وضع توكن البوت الخاص بك هنا
TELEGRAM_TOKEN = "7749904898:AAHhbFobuuchs2jhrkXfZiLKYwYA1Q60bRs" 

# إعدادات التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# ==========================================================
# 2. دوال معالجة الأوامر الجديدة
# ==========================================================

async def start_command(update: Update, context):
    """الرد على أمر /start برسالة ترحيب."""
    await update.message.reply_text(
        "👋 أهلاً بك! أنا بوت تليجرام بسيط.\n"
        "استخدم /help لرؤية قائمة الأوامر المتاحة."
    )

async def help_command(update: Update, context):
    """الرد على أمر /help بقائمة الأوامر."""
    help_message = (
        "💡 **قائمة الأوامر والمميزات:**\n"
        "**/start** - رسالة الترحيب.\n"
        "**/help** - عرض هذه القائمة.\n"
        "**/info** - معلومات عن البوت.\n"
        "**/echo [نص]** - يرد البوت بنفس النص الذي ترسله.\n"
        "**/groupstats** - عرض إحصائيات المجموعة.\n"
        "**/ban [بالرد على العضو]** - طرد عضو.\n"
        "**/time** - لعرض الوقت والتاريخ الحاليين.\n" # 🆕 أمر جديد
        "**/id [بالرد على عضو]** - لعرض المعرّف (ID) للعضو المُشار إليه.\n\n" # 🆕 أمر جديد
        "**الترحيب بالأعضاء الجدد** - يرسل رسالة ترحيب تلقائية."
    )
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def info_command(update: Update, context):
    """الرد على أمر /info بمعلومات عن البوت."""
    info_message = (
        "🤖 **معلومات البوت**:\n"
        "هذا البوت يعمل بوضع الرد الثابت مع مميزات إدارية ووظائف مساعدة."
    )
    await update.message.reply_text(info_message, parse_mode='Markdown')

async def echo_command(update: Update, context):
    """يعيد إرسال النص الذي كتبه المستخدم بعد الأمر /echo."""
    text_to_echo = " ".join(context.args)
    if text_to_echo:
        await update.message.reply_text(f"صدى الرسالة: {text_to_echo}")
    else:
        await update.message.reply_text("يرجى إدخال نص بعد الأمر /echo.")

async def send_static_photo_command(update: Update, context):
    """يرسل صورة ثابتة."""
    await update.message.reply_text("عذراً، وظيفة الصورة الثابتة غير مفعّلة حالياً.")

async def group_stats_command(update: Update, context):
    """يعرض إحصائيات بسيطة عن المجموعة."""
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        member_count = await context.bot.get_chat_member_count(chat.id)
        stats_message = (
            f"📊 **إحصائيات المجموعة**\n"
            f"**اسم المجموعة:** {chat.title}\n"
            f"**عدد الأعضاء:** {member_count}"
        )
    else:
        stats_message = "هذا الأمر يعمل فقط داخل المجموعات."
    await update.message.reply_text(stats_message, parse_mode='Markdown')

async def ban_user_command(update: Update, context):
    """طرد عضو من المجموعة (يتطلب الرد على رسالته)."""
    if update.message.chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("هذا الأمر يعمل فقط داخل المجموعات.")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("يجب عليك الرد على رسالة العضو الذي تريد طرده.")
        return

    user_to_ban = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id

    try:
        await context.bot.ban_chat_member(chat_id, user_to_ban.id)
        await update.message.reply_text(
            f"🚫 تم طرد المستخدم [{user_to_ban.full_name}](tg://user?id={user_to_ban.id}) بنجاح."
            , parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"خطأ في الطرد: {e}")
        await update.message.reply_text("❌ عذراً، لم أتمكن من طرد هذا العضو. (تأكد من أن البوت مشرف ولديه صلاحية الطرد).")

async def welcome_new_member(update: Update, context):
    """الترحيب بالأعضاء الجدد."""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            return
            
        welcome_message = (
            f"👋 مرحباً بك يا [{member.full_name}](tg://user?id={member.id}) في مجموعتنا!"
            "\nنأمل أن تستمتع بوقتك معنا."
        )
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

# 🆕 دالة عرض الوقت والتاريخ
async def time_command(update: Update, context):
    """يعرض الوقت والتاريخ الحاليين."""
    now = datetime.datetime.now()
    # يمكن تغيير هذا التنسيق حسب رغبتك
    time_str = now.strftime("%Y/%m/%d - %H:%M:%S") 
    
    # ⚠️ ملاحظة: هذا هو وقت الخادم الذي يعمل عليه الكود.
    await update.message.reply_text(f"🕰️ الوقت والتاريخ الحالي للخادم هو: {time_str}")

# 🆕 دالة عرض ID المستخدم
async def get_user_id_command(update: Update, context):
    """يعرض ID المستخدم الذي تم الرد على رسالته أو ID المرسل."""
    
    # تحقق مما إذا كانت الرسالة رد على رسالة أخرى
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
        name = target_user.full_name
        user_id = target_user.id
        response = (
            f"👤 معلومات العضو المُشار إليه:\n"
            f"**الاسم:** {name}\n"
            f"**المعرّف (ID):** `{user_id}`"
        )
    else:
        # إذا لم تكن رداً، يعرض ID المستخدم الذي أرسل الأمر
        sender_user = update.effective_user
        name = sender_user.full_name
        user_id = sender_user.id
        response = (
            f"👤 معلوماتك:\n"
            f"**الاسم:** {name}\n"
            f"**المعرّف (ID):** `{user_id}`"
        )
        
    await update.message.reply_text(response, parse_mode='Markdown')

async def handle_text_message(update: Update, context):
    """الرد على الرسائل النصية العادية وردود الوقت عند الحاجة."""
    if not update.message or not update.message.text:
        return
        
    text = update.message.text.strip().lower()

    # 🆕 التحقق من كلمات مفتاحية للساعة
    time_keywords = ["كم الساعة", "الساعة كم", "الوقت كام", "التاريخ اليوم"]
    if any(keyword in text for keyword in time_keywords):
        # إذا سأل المستخدم عن الوقت، نرسله لدالة الوقت
        await time_command(update, context)
        return
        
    # الرد الثابت
    response_text = f"تم استلام رسالتك: '{update.message.text[:30]}...' (أنا في وضع الرد الثابت)."
    await update.message.reply_text(response_text)

# ==========================================================
# 3. الوظيفة الرئيسية للتشغيل
# ==========================================================
def main():
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # 1. إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("echo", echo_command))
    application.add_handler(CommandHandler("photo", send_static_photo_command))
    application.add_handler(CommandHandler("groupstats", group_stats_command))
    application.add_handler(CommandHandler("ban", ban_user_command))
    application.add_handler(CommandHandler("time", time_command)) # 🆕 إضافة معالج أمر الوقت
    application.add_handler(CommandHandler("id", get_user_id_command)) # 🆕 إضافة معالج أمر ID

    # 2. معالج الترحيب بالأعضاء الجدد
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))

    # 3. معالج الرسائل النصية (الردود الثابتة والتحقق من الوقت)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    print("البوت يعمل الآن مع مميزات الوقت والمعرفات.")
    
    application.run_polling(poll_interval=1.0)

# ==========================================================
if __name__ == '__main__':
    main()

import telebot
from config import sub_channels, bot
def check_bot_admin(bot, sub_channels):
    for channel in sub_channels:
        try:
            member = bot.get_chat_member(channel, bot.get_me().id)
            if member.status not in ["administrator", "creator"]:
                print(f"⚠️ البوت ليس أدمن في القناة {channel} — الرجاء ترقيته.")
        except Exception as e:
            print(f"❌ خطأ أثناء التحقق من القناة {channel}: {e}")




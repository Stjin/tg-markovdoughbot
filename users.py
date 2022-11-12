def get_admin_ids(update, context, chat_id):
    bot = context.bot
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def isAdmin(update, context):
    if update.effective_user is not None:
        if update.effective_user.id in get_admin_ids(update, context, update.effective_message.chat_id):
            return True
    return False
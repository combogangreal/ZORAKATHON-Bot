from bot import bot

def get_rank(bot: bot.Bot, messageid: int):
    bot.database.execute("SELECT Messages, MessageID, Rank(ORDER Rank DESC)")
    rank = bot.database.execute("SELECT Rank FROM Messages WHERE MessageID = ?", messageid)
    return rank
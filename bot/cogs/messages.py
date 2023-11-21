import asyncio
from discord import app_commands, Interaction, Member, Reaction, Embed, Color, Object
from discord.utils import get
from discord.ext.commands import Cog, has_permissions
from typing import Optional
from datetime import datetime

from bot import bot, config, utils


class Moderation(Cog):
    """Messages cog for the bot"""

    def __init__(self, bot: bot.Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: Member):
        self.bot.database.execute("INSERT OR IGNORE INTO Messages (MessageID, AuthorID) VALUES (?, ?)", reaction.message.id, user.id)
        self.bot.database.execute("UPDATE Messages SET Rank = ? WHERE MessageID = ?", utils.get_rank(self.bot, reaction.message.id), reaction.message.id)
async def setup(bot: bot.Bot):
    await bot.add_cog(Moderation(bot), guilds=[Object(id=config.SUPPORT_ID)])
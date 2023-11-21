import os
import discord
from discord.ext.commands import AutoShardedBot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot import database, errors, config
from loguru import logger
from discord import Reaction, User


class Bot(AutoShardedBot):
    """Main bot class"""

    def __init__(self, **options) -> None:
        super().__init__(
            command_prefix=config.PREFIX, intents=discord.Intents.default(), **options
        )
        self.database = database.Database()
        self.scheduler = AsyncIOScheduler()
        self.logger = logger
        self.database.autosave(self.scheduler)

    async def load_extensions(self):
        """Loads all the extensions / cogs in the ./cogs folder"""
        for f in os.listdir("./bot/cogs"):
            if f.endswith(".py"):
                await self.load_extension("bot.cogs." + f[:-3])
                self.logger.debug(f"Successfully loaded cog: {f[:-3]}")

    async def start(self):
        """Starts the bot"""
        try:
            self.database.build()
            self.logger.debug("Starting the bot")
            await super().start(config.BOT_TOKEN, reconnect=True)
        except errors.StartUpError as e:
            raise errors.StartUpError(f"Bot failed to startup: {e}")

    async def setup_hook(self) -> None:
        """Hook for when the bot is being setup, used to load all the extensions"""
        await self.load_extensions()
        await self.tree.sync(guild=discord.Object(id=config.SUPPORT_ID))
        return await super().setup_hook()

    async def on_reaction_add(self, reaction: Reaction, user: User):
        self.bot.database.execute("INSERT OR IGNORE INTO Messages (MessageID, AuthorID) VALUES (?, ?)", reaction.message.id, user.id)
        self.bot.database.execute("UPDATE Messages SET Rank = ? WHERE MessageID = ?", utils.get_rank(self.bot, reaction.message.id), reaction.message.id)
        await user.send("Test")
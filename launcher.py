from bot import bot
import asyncio

bot = bot.Bot()

async def launch():
    await bot.start()

asyncio.run(launch())
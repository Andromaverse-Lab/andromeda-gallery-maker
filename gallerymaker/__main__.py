import discord
import os
from .gallery_client import GalleryClient
import logging

logging.basicConfig(level=logging.DEBUG)

discord_key = os.environ.get("DISCORD_KEY")
bot = GalleryClient(intents=discord.Intents.default())
bot.run(discord_key)

from discord.ext import commands
from config import intents


bot = commands.Bot(command_prefix=['/', '🅱'], intents=intents)
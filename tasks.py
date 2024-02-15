import asyncio
import random
from discord.ext import tasks
from RanoFileToPreventCircularImport import queue, queue_count, current_song, song_count
from config import messages, spamchannel, supersecret_toggle
from bot_instance import bot


@tasks.loop(seconds=5)
async def check_vc():
    for vc in bot.voice_clients:
        if vc.guild.voice_client is not None and len(vc.channel.members) <= 1:  # If bot is the only one in the channel
            await vc.disconnect()
            global queue, song_count, queue_count, video_title, url
            song_count = 0
            queue_count = 0
            queue = asyncio.Queue()  # Create a new queue instead of emptying the old one


@tasks.loop(seconds=5)
async def clear_song():
    for vc in bot.voice_clients:
        if not vc.is_playing():
            current_song[vc.guild.id] = None


#ads 
@tasks.loop(hours=random.randint(8, 12))
async def send_message():
    global supersecret_toggle
    if supersecret_toggle:
        channel = bot.get_channel(spamchannel) 
        message = random.choice(messages)
        await channel.send(message)
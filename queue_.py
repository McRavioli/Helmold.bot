from discord import FFmpegPCMAudio
import asyncio
from yt_dlp import YoutubeDL
from config import FFMPEG_OPTIONS, ydl_opts
from bot_instance import bot
from RandoFileToPreventCircularImport import queue, queue_count, current_song, song_count

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

#queue error handling
def check_queue(ctx, error):
    coro = play_next(ctx)
    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
    try:
        fut.result()
    except:
        pass

async def play_next(ctx):
    global queue, voice_channel, queue_count, url, video_title, song_count, current_song_url, current_song_title, ydl_opts

    voice_channel = ctx.guild.voice_client

    if not queue.empty() and not voice_channel.is_playing():
        song = await queue.get()
        url = song['url']
        video_title = song['title']
        song_count += 1
        if song_count > 1:
            await ctx.reply('NEXT')

        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            stream_url = info_dict.get('url')

            if stream_url:
                source = FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
                voice_channel.play(source, after=lambda e: check_queue(ctx, e))
                current_song[ctx.guild.id] = {'title': video_title, 'url': url}
                print(f"Updated current song for guild {ctx.guild.id}: {current_song[ctx.guild.id]}")  # Debug print
            else:
                print(f"Failed to extract stream URL for {url}")

    if queue.empty():
        song_count = 0

from discord import FFmpegPCMAudio
import asyncio
from pytube import YouTube
from yt_dlp import YoutubeDL
from config import FFMPEG_OPTIONS, ydl_opts
from bot_instance import bot
from RandoFileToPreventCircularImport import queue, queue_count, current_song, song_count


ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
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
        if 'soundcloud' in url:
            # handle SoundCloud link
            with YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict['title']
                stream_url = info_dict['url']
                source = FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
        else:
            # handle YouTube link
            youtube = YouTube(url)
            video_title = youtube.title
            stream = youtube.streams.filter(only_audio=True).first()
            source = FFmpegPCMAudio(stream.url, **FFMPEG_OPTIONS)
        voice_channel.play(source, after=lambda e: check_queue(ctx, e))
        current_song[ctx.guild.id] = {'title': video_title, 'url': url}
        print(f"Updated current song for guild {ctx.guild.id}: {current_song[ctx.guild.id]}")  # Debug print
    if queue.empty():
        song_count = 0

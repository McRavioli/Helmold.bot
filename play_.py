from pytube import YouTube, Playlist
import re
import requests
import json
import validators
from yt_dlp import YoutubeDL
from config import YOUTUBE_API_KEY, YOUTUBE_API_KEY, ydl_opts
from bot_instance import bot
from RandoFileToPreventCircularImport import queue, queue_count, current_song, song_count
from queue_ import play_next


youtube_url_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
youtube_playlist_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(playlist)'

soundcloud_url_pattern = r'(https?://)?(www\.)?(soundcloud)\.(com)/'
soundcloud_playlist_pattern = r'(https?://)?(www\.)?(soundcloud)\.(com)/.+/sets/.+'


@bot.command(name='play')
async def play(ctx, *, search_term):
    global queue, youtube_playlist_pattern, youtube_url_pattern, queue_count, ydl_opts
    from main import bot

    #check ob user in nem voice channel ist
    if ctx.message.author.voice is None:
        await ctx.send('Please connect to a voice channel')
        return
    
    if ctx.guild.voice_client is not None and ctx.message.author.voice.channel != ctx.guild.voice_client.channel:
        await  ctx.send("You are not in my voice channel")

    #check ob der bot schon verbunden ist
    if ctx.guild.voice_client is None:
        #connect to sender vc
        channel = ctx.message.author.voice.channel
        voice_channel = await channel.connect()
        await ctx.guild.change_voice_state(channel=channel, self_deaf=True,  self_mute=False)
    else:
        voice_channel = ctx.guild.voice_client 

    if re.match(soundcloud_url_pattern, search_term) or re.match(soundcloud_playlist_pattern, search_term):
        if re.match(soundcloud_playlist_pattern, search_term):
            await ctx.reply("Because of SoundCloud not letting new users use their API, SoundCloud playlists currently aren't supported.\nThis is not my fault, it's just SoundCloud being a shitty company.\nBut rest assured, as soon as SoundCound lets me, I'll add this feature.")
            return
        else:
            url = search_term
            with YoutubeDL(ydl_opts) as ydl:
                url = search_term
                info_dict = ydl.extract_info(url, download=False)
                video_title = info_dict['title']

            await queue.put({'url': url, 'title': video_title})
            await ctx.reply('💯💯')
            queue_count += 1

        await play_next(ctx)
        return
     # check if the search_term is a YouTube URL or a YouTube Playlist URL
    if re.match(youtube_url_pattern, search_term) or re.match(youtube_playlist_pattern, search_term):
        url = search_term
            #check if url is a playlist
        if 'playlist' in url:
            playlist = Playlist(url)
            await ctx.reply('👍👍')
            for video_url in playlist.video_urls:
                youtube = YouTube(video_url)
                video_title = youtube.title
                await queue.put({'url': video_url, 'title': video_title})
                queue_count += 1
        else:
            youtube = YouTube(url)
            video_title = youtube.title
            await queue.put({'url': url, 'title': video_title})
            await ctx.reply('🤙🤙')
            queue_count += 1
        await play_next(ctx)
    else:
        # search for videos on YouTube
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=id&maxResults=1&q={search_term}&key={YOUTUBE_API_KEY}"
        
        response = requests.get(search_url)

        data = json.loads(response.text)

        # check if the response contains any items
        if not data.get('items'):
            print("No items in YouTube API response")
            return
        
        # get the first item
        item = data['items'][0]

        # check if the item contains an 'id' field
        if not item.get('id'):
            print("No 'id' field in item")
            return

        # check if the 'id' field contains a 'videoId' field
        if not item['id'].get('videoId'):
            print("No 'videoId' field in 'id'")
            return
        
        
        # get the video ID of the first search result
        video_id = data['items'][0]['id']['videoId']

        # create the YouTube video URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # check if the URL is valid
        if not validators.url(video_url):
            print("Invalid URL:", video_url)
            return

        # get the video title
        youtube = YouTube(video_url)
        video_title = youtube.title

        # add the video to the queue
        await queue.put({'url': video_url, 'title': video_title})
        queue_count += 1

        # reply to the user with the link of the song that was added to the queue
        await ctx.reply(f"Added to queue: [{video_title}](<{video_url}>)")

        # play the next song
        await play_next(ctx)

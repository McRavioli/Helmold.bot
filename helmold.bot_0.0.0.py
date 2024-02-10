import discord 
from discord import FFmpegPCMAudio
import asyncio
import random
from discord.ext import tasks, commands
from pytube import YouTube, Playlist
import re
import requests
import json
import configparser
from collections import deque
import collections
import aiohttp
import datetime
import validators

messages = ["helmold.bot: Square. Practical. Smart.", "helmold.bot: Dare to be smart.", "helmold.bot: Gives you wings.", 
            "helmold.bot: Are you still living or already chatting?", "Haribo makes kids happy… and so does helmold.bot.", 
            "Washing machines live longer with helmold.bot.", "helmold.bot: You're not yourself when you're boring.", 
            "Is this new? No, it's helmold.bot.", "One helmold.bot, please.", "As the land, so the helmold.bot.", 
            "helmold.bot: There, you know what you have.", "Nothing is impossible for helmold.bot.", "The best or nothing, helmold.bot.", 
            "Chat can be this smart, helmold.bot.", "Simply helmold.bot.", "The future of chatting, helmold.bot.", "I'm love'n it, helmold.bot.", 
            "The original, helmold.bot.", "For what matters, helmold.bot.", "There's always a way with helmold.bot.", "Because you're worth it, helmold.bot.", 
            "Chat better with the second, helmold.bot.", "That certain something, helmold.bot.", "The chat that connects, helmold.bot.", 
            "Nothing is impossible, helmold.bot.", "Smartness inside where helmold.bot is.", "The chat experience, helmold.bot.", 
            "helmold.bot is fun.", "The chat that takes you further, helmold.bot.", "helmold.bot feels good.", 
            "helmold.bot. And you're right in the middle.", "helmold.bot. The chat for all situations.", "helmold.bot. This is my chat.", 
            "helmold.bot. The chat that inspires you.", "helmold.bot. The chat that makes you happy.", 
            "helmold.bot. The chat that understands you.", "helmold.bot. The chat that excites you.", 
            "helmold.bot. The chat that surprises you.", "helmold.bot. The chat that moves you.", 
            "helmold.bot. The chat that refreshes you.", "helmold.bot. The chat that informs you.", 
            "helmold.bot. The chat that entertains you.", "helmold.bot. The chat that calms you.", 
            "helmold.bot. The chat that protects you.", "helmold.bot: Where chat meets brilliance.", 
            "Unlock your potential with helmold.bot.", "helmold.bot: The chat that dances with ideas.", 
            "Smart chat, smarter helmold.bot.", "helmold.bot: Your chat, your rules.", 
            "Chat like a pro with helmold.bot.", "helmold.bot: The chat that never sleeps.", 
            "Elevate your conversations with helmold.bot.", "helmold.bot: The chat that's always on point.", 
            "Chatting redefined by helmold.bot.", "helmold.bot: Your virtual confidante.", 
            "Navigate life's twists with helmold.bot.", "helmold.bot: The chat that's got your back.", 
            "Chatting made delightful with helmold.bot.", "helmold.bot: Your witty companion.", 
            "Unleash your chat superpowers with helmold.bot.", "helmold.bot: The chat that sparks curiosity."]
messages = [msg.replace('helmold', 'Helmold') for msg in messages]

config = configparser.ConfigParser()
config.read('config.ini')


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['/', '🅱'], intents=intents)
FFMPEG_OPTIONS = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn' }


supersecret_toggle = config.getboolean('configuration', 'supersecretoptions')


YOUTUBE_API_KEY = config.get('keys', 'YoutubeAPIKey')


youtube_url_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
youtube_playlist_pattern = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(playlist)'


queue = asyncio.Queue()
song_count = 0
queue_count = 0     
current_song = {}
              

if supersecret_toggle:
    sauerkraut_toggle = True
else:
    sauerkraut_toggle = False



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





@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('SuperSecretOptons set to: ', config.get('configuration', 'supersecretoptions'))
    if not check_vc.is_running():
        check_vc.start()
    print('------')
    if not send_message.is_running():
        send_message.start()
    if not clear_song.is_running():
        clear_song.start()


#ads 
@tasks.loop(hours=random.randint(8, 12))
async def send_message():
    global supersecret_toggle
    if supersecret_toggle:
        channel = bot.get_channel(config.getint('configuration', 'spamchannel')) 
        message = random.choice(messages)
        await channel.send(message)

#queue error handling
def check_queue(ctx, error):
    coro = play_next(ctx)
    fut = asyncio.run_coroutine_threadsafe(coro, bot.loop)
    try:
        fut.result()
    except:
        pass



async def play_next(ctx):
    global queue, voice_channel, queue_count, url, video_title, song_count, current_song_url, current_song_title

    voice_channel = ctx.guild.voice_client

    if not queue.empty() and not voice_channel.is_playing():
        song = await queue.get()
        url = song['url']
        video_title = song['title']
        song_count += 1
        if song_count > 1:
            await ctx.reply('NEXT')
        youtube = YouTube(url)
        video_title = youtube.title
        stream = youtube.streams.filter(only_audio=True).first()
        source = FFmpegPCMAudio(stream.url, **FFMPEG_OPTIONS)
        voice_channel.play(source, after=lambda e: check_queue(ctx, e))
        current_song[ctx.guild.id] = {'title': video_title, 'url': url}
        print(f"Updated current song for guild {ctx.guild.id}: {current_song[ctx.guild.id]}")  # Debug print
    if queue.empty():
        song_count = 0
        


@bot.command(name='play')
async def play(ctx, *, search_term):
    global queue, youtube_playlist_pattern, youtube_url_pattern, queue_count

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

@bot.command(name='np', aliases=['nowplaying', 'now_playing'])
async def now_playing(ctx):
    song = current_song.get(ctx.guild.id)
    if song is not None:
        await ctx.reply(f"Currently playing: [{song['title']}](<{song['url']}>)")
    else:
        await ctx.reply("https://tenor.com/view/mr-peebles-reaction-gif-9154535451992198936")

        
@bot.command(name='p', alias=['pause'])
async def pause(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()

@bot.command(name='r', alias=['resume'])
async def resume(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()


@bot.command('bugreport')
async def report(ctx, *, message):
        user_id = 550404550624935937
        user = await bot.fetch_user(user_id)
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if message == None:
            await ctx.reply("Pelase provide the issue you're having after the command")
            return
        await user.send(f'bug report from <@{ctx.author.id}> at {current_time}\n\n{message}')
        await ctx.reply(f'Thank you for your report, <@{550404550624935937}> will take care of it as soon as he can.\nPlease make shure that your dms are open for everyone so he can contact you if he needs additional information.')

#bugreport error handling
@report.error
async def report_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(f"Pelase provide the issue you're having like this:\n\n/bugreport <your issue in as much detail as possible>")

@bot.command(name='kill')   #command to kill the music bot (clears queue, leaves vc)
async def kill(ctx):
    global queue, song_count, queue_count, video_title, url
    #check if bot is connected
    if ctx.guild.voice_client is None:
        await ctx.reply("You can't kill someone who doesen't live")
        return
    #disconnect bot
    await ctx.guild.voice_client.disconnect()
    song_count = 0
    queue_count = 0
    while not queue.empty():
        await queue.get()
    await ctx.reply('The voices are getting louder...')
    

@bot.command(name='skip')    #function to skip a song fron queue
async def skip(ctx):

  global queue, song_count 

  voice_channel = bot.voice_clients[0]

  if voice_channel.is_playing():    #checks if bot is in a voice channel
    voice_channel.stop()
    song_count += 1
    
    if queue.empty():   #checks if queue is empty
      song_count = 0
      
    await ctx.reply('Skipped indeed')
  else:
    await ctx.reply('Nothing to skip, young man')

@bot.command(name='sauerkraut')
async def sauerkraut(ctx, member: discord.Member):
    global  supersecret_toggle, sauerkraut_toggle
    #pings users from the /sauerkraut command in a scpecifyed channel
    if not supersecret_toggle:
        await ctx.reply('I be popin bottles')
        return
    for _ in range(200):
        if not sauerkraut_toggle:
            sauerkraut_toggle = True
            break
        channel = bot.get_channel(config.getint('configuration', 'spamchannel'))
        await channel.send(f'{member.mention}ICH BIN I SHOW SAUERKRAUT')


@bot.command(name='terminate')  #function to stop the sauerkraut spam
async def ayran(ctx):
    global sauerkraut_toggle
    sauerkraut_toggle = False
    if not sauerkraut_toggle:
        user = ctx.author
        await user.send("`Sauerkraut sucsessfully terminated`")
    else:
        user = ctx.author
        await user.send("`Sauerkraut sucsessfully enabled`")
    await ctx.message.delete()


@bot.command(name='clearqueue')  #function to clear the queue
async def clearqueue(ctx):
    global queue_count, queue
    if queue_count > 0:
        while not queue.empty():
            await queue.get()
        await ctx.reply("you know i'm something of a scientist myself")
    else:
        await ctx.reply('bruh')


@bot.command(name='queue')
async def display_queue(ctx):  
    global queue

    queue_items = list(queue._queue)

    if not queue.empty():
        message = "Songs in the queue:\n"
        for i, song in enumerate(queue_items):
            new_line = f"{i+1}. [{song['title']}](<{song['url']}>)\n"
            if len(message + new_line) > 2000:
                await ctx.send(message)
                message = new_line
            else:
                message += new_line
        if message:
            await ctx.send(message)
    else:
        await ctx.reply("https://tenor.com/bSGoX.gif")

@bot.command(name="shuffle")
async def shuffle(ctx):
    global queue

    if not queue.empty():
        # Create a copy of the queue
        queue_copy = list(queue._queue)
        
        # Shuffle the copy
        random.shuffle(queue_copy)

        # Replace the original queue with the shuffled copy
        queue._queue = collections.deque(queue_copy)

        print("queue shuffled")
    else:
        await ctx.reply("https://tenor.com/view/sad-emote-emoji-thumbs-down-mid-gif-26466326")

  

# bot token
bot.run(config.get('keys', 'BotToken'))
import random
import collections
from bot_instance import bot
from RandoFileToPreventCircularImport import queue, queue_count, current_song, song_count
from config import config, supersecret_toggle, sauerkraut_toggle


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
async def report(ctx):
        await ctx.reply("Hey, i'm sorry but the bugreport function is currently under maintenance. \nFor the time being please report any issues to <@550404550624935937> via dm or go to https://github.com/McRavioli/Helmold.bot and post your bugreport there under the issues tab. \nI'm sorry for the inconvenience but be assured that I'm are working on it. \nHave a great day!")


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


#the following function was made possible by our sponsor: Raid: Shadow Legends


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

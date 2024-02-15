import discord
from config import spamchannel, supersecret_toggle, sauerkraut_toggle, config
from bot_instance import bot


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
        channel = bot.get_channel(spamchannel)
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
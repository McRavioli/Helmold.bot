from tasks import check_vc, send_message, clear_song
from config import BOT_TOKEN, supersecret_toggle, sauerkraut_toggle, FFMPEG_OPTIONS, config, YOUTUBE_API_KEY
from bot_instance import bot
import play_
import queue_
import commands
import queue_
import sauerkraut_



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


# bot token
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
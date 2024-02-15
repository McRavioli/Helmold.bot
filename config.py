import discord
import configparser

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


intents = discord.Intents.default()
intents.message_content = True

config = configparser.ConfigParser()
config.read('config.ini')

BOT_TOKEN = config.get('keys', 'BotToken')

FFMPEG_OPTIONS = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn' }

supersecret_toggle = config.getboolean('configuration', 'supersecretoptions')

spamchannel = config.getint('configuration', 'spamchannel')

if supersecret_toggle:
    sauerkraut_toggle = True
else:
    sauerkraut_toggle = False

YOUTUBE_API_KEY = config.get('keys', 'YoutubeAPIKey')

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
}


As of October 13, 2024, this project is officially abandoned. All future updates and releases will be available on [OpusCast.de](https://opuscast.de/).

# Helmold.bot 
An open-source music bot for Discord, currently being developed by the 17-year-old software engineer, McRavioli.

## How to Set Up:

Install FFmpeg, download the config.ini file and either the .exe or .py file (they are identical, but if you prefer using the .py file, make sure to download the necessary libraries).
Open the config.ini and fill in your bot token, YouTube API key, and the channel ID of a Discord server channel where you’d like to receive spam(don't worry wou won't receve any span if you don't activate it in the config.ini), you can leave the spot for the Soundcloud ID free scinece it isn't requiered.
Optionally, you can enable the super-secret options by setting them to true. This will activate the /sauerkraut command, which pings a specific user 200 times, and your bot will randomly send ads for Helmold.bot into the spam channel.
Now you’re all set! Just execute the .exe or .py file.

## List of Commands:

/play (YouTube search term/YouTube video URL/YouTube playlist URL/soundcloud track URL)

/skip 

/np or /nowplaying

/p or /pause

/r or /resume

/kill – Disconnects the bot and clears the queue.

/queue

/sauerkraut (@user) – Pings the user 200 times within the spam channel (only if the super-secret options are set to true).

/terminate – Stops the sauerkraut command.

/clearqueue

/shuffle

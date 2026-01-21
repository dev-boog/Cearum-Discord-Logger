import discord
import time
import json

from threading import Thread
from database.db_manager import Database

starttime = time.time()

selfbot = discord.Client()

Database.initialize()

bot_status = {
    'running': False,
    'error': None
}

def get_runtime():
    seconds = int(time.time() - starttime)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{days}d, {hours}h, {minutes}m"

@selfbot.event
async def on_ready():
    bot_status['running'] = True

@selfbot.event
async def on_message_delete(message):
    with open('config.json', 'r') as f:
        config = json.load(f)
        config = config['logger_settings']
        
    if config['log_deleted_messages'] is False:
        return
    
    if config['ignore_bots'] and message.author and message.author.bot:
        return
    
    if config['ignore_self'] and message.author and message.author.id == selfbot.user.id:
        return
    
    if config['ignored_channels'] and message.channel.id in config['ignored_channels']:
        return
    
    if config['ignored_guilds'] and message.guild and message.guild.id in config['ignored_guilds']:
        return
    
    
    Database.log_deleted_message(message)

def run_bot(token):
    try:
        selfbot.run(token)
    except discord.LoginFailure:
        bot_status['error'] = 'Invalid Discord token'
    except Exception as e:
        bot_status['error'] = str(e)

def start_bot(token):
    bot_thread = Thread(target=run_bot, args=(token,), daemon=True)
    bot_thread.start()
    

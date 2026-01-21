from flask import Flask, render_template
from logger import discord_logger as selfbot
from database.db_manager import Database

import webview
import time
import threading
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    
app = Flask(__name__)

@app.route('/load_all_deleted_messages')
def load_all_deleted_messages():  
    messages = Database.fetch_last_n_messages(config['logger_settings']['messages_to_fetch'])
    
    if not messages:
        return "<div class='log-theme m-5 p-1 px-2 rounded'><p>No deleted messages found.</p></div>"
    html = ""
    for msg in messages:
        _, author, author_id, msg_id, content, timestamp, channel, channel_id, guild, guild_id, is_dm, avatar_url = msg
        html += f"""
        <div class='log-theme rounded m-1 mx-2 p-2'>
            <div class='flex items-center gap-2 mb-1.5 flex-wrap'>
                <img src='{avatar_url or 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTyhNQWPo_bq8N7jE2ev6GImOIDxJuI0a4Pbw&s'}' 
                     alt='' 
                     class='w-6 h-6 rounded-full flex-shrink-0'>
                <span class='text-[10px] font-semibold whitespace-nowrap'>@{author}</span>
                <span class='text-[10px] text-white font-semibold bg-blue-600 rounded px-1.5 py-0.5 shadow-[0_0_15px_rgba(37,99,235,0.2)] whitespace-nowrap'>{author_id}</span>
                <span class='text-[10px] text-white font-semibold bg-blue-600 rounded px-1.5 py-0.5 shadow-[0_0_15px_rgba(37,99,235,0.2)] whitespace-nowrap'>{timestamp}</span>
                <span class='text-[10px] text-white font-semibold bg-blue-600 rounded px-1.5 py-0.5 shadow-[0_0_15px_rgba(37,99,235,0.2)] whitespace-nowrap'>{guild}</span>
                <span class='text-[10px] text-white font-semibold bg-blue-600 rounded px-1.5 py-0.5 shadow-[0_0_15px_rgba(37,99,235,0.2)] whitespace-nowrap'>{channel}</span>
                <span class='text-[10px] text-white font-semibold bg-blue-600 rounded px-1.5 py-0.5 shadow-[0_0_15px_rgba(37,99,235,0.2)] whitespace-nowrap'>{'DM' if is_dm else 'Server'}</span>
            </div>
            <p class='text-[10px] font-light text-neutral-400'>{content}</p>
        </div>
        """
    return html

@app.route('/update_total_deleted_messages')
def update_total_deleted_messages():
    deleted_messages = Database.fetch_total_messages()
    return str(deleted_messages)

@app.route('/update_database_size')
def update_database_size():
    db_size = Database.fetch_size_mb()
    return f"{db_size} MB"

@app.route('/update_runtime')
def update_runtime():
    runtime = selfbot.get_runtime()
    return runtime

@app.route('/configuration')
def configuration():
    return render_template('configuration.html')
        
@app.route('/')
def index():
    time.sleep(2)
    
    if selfbot.bot_status['error']:
        return render_template('error.html', error_code='AUTH_TOKEN_INVALID', error_message='The provided authentication token is invalid. Please make sure you have entered the correct token.')
    elif selfbot.bot_status['running']:
        return render_template('dashboard.html', user=selfbot.selfbot.user)
    else:
        return render_template('error.html', error_code='BOT_INIT_FAILED', error_message='Failed to initialize the bot. Please try again later or contact support.')

def run_flask():
    app.run(
        debug=False,
        host="0.0.0.0",
        port=config['server_port'],
        use_reloader=False
    )
    
def run_selfbot():
    selfbot.start_bot(config['token'])

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    bot_thread = threading.Thread(target=run_selfbot, daemon=True)
    bot_thread.start()

    if config['use_gui']:
        webview.create_window(
            "Cerarum",
            f"http://127.0.0.1:{config['server_port']}",
            width=1280,
            height=960
        )
        webview.start()

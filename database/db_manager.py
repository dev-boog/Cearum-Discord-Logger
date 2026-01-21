
import sqlite3
import os

class Database:
    name = "deleted_messages.db"
    
    @staticmethod
    def fetch_last_n_messages(n=5):
        conn = Database.fetch()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages ORDER BY id DESC LIMIT ?", (n,))
        rows = cursor.fetchall()
        conn.close()
        return rows
    
    @staticmethod
    def fetch():
        return sqlite3.connect(Database.name)
    
    @staticmethod
    def initialize():
        conn = Database.fetch()
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_author TEXT,
            message_author_id TEXT,
            message_id TEXT UNIQUE,
            message_content TEXT,
            message_timestamp TEXT,
            channel_name TEXT,
            channel_id TEXT,
            guild_name TEXT,
            guild_id TEXT,
            is_dm INTEGER,
            avatar_url TEXT
        );
        ''')
        
        conn.commit()
        conn.close()
        
    def log_deleted_message(message):
        author_name = message.author.name if message.author else "N/A"
        author_id = str(message.author.id) if message.author else "N/A"

        content = message.content or "N/A"
        timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S") if message.created_at else "N/A"
        avatar_url = str(message.author.avatar.url) if message.author.avatar else "N/A"
        
        if message.guild:
            channel_name = message.channel.name
            channel_id = str(message.channel.id)
            guild_name = message.guild.name
            guild_id = str(message.guild.id)
            is_dm = 0
        else:
            channel_name = "DM"
            channel_id = str(message.channel.id)
            guild_name = "DM"
            guild_id = "DM"
            is_dm = 1

        conn = Database.fetch()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT OR IGNORE INTO messages ("
            "message_author, message_author_id, message_id, message_content, "
            "message_timestamp, channel_name, channel_id, guild_name, guild_id, is_dm, avatar_url"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (author_name, author_id, str(message.id), content, timestamp, channel_name, channel_id, guild_name, guild_id, is_dm, avatar_url)
        )

        conn.commit()
        conn.close()
        
    @staticmethod
    def fetch_deleted_messages():
        conn = Database.fetch()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()

        conn.close()
        return rows
    
    @staticmethod
    def fetch_size_mb():
        size_bytes = os.path.getsize(Database.name)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    
    @staticmethod
    def fetch_total_messages():
        conn = Database.fetch()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
        
    @staticmethod
    def fetch_deleted_by_user(user_id):
        conn = Database.fetch()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM messages WHERE message_author_id = ?", (str(user_id),))
        rows = cursor.fetchall()
        
        conn.close()
        return rows
        
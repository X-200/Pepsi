import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='database/pharaoh_chat.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # جدول المستخدمين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الرسائل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, username):
        """إضافة مستخدم جديد"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR IGNORE INTO users (username) VALUES (?)',
                (username,)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"خطأ في إضافة المستخدم: {e}")
            return False
    
    def update_last_seen(self, username):
        """تحديث آخر ظهور للمستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE users SET last_seen = CURRENT_TIMESTAMP WHERE username = ?',
                (username,)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"خطأ في تحديث آخر ظهور: {e}")
    
    def add_message(self, username, message):
        """إضافة رسالة جديدة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO messages (username, message) VALUES (?, ?)',
                (username, message)
            )
            conn.commit()
            message_id = cursor.lastrowid
            conn.close()
            return message_id
        except Exception as e:
            print(f"خطأ في إضافة الرسالة: {e}")
            return None
    
    def get_recent_messages(self, limit=50):
        """الحصول على آخر الرسائل"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT username, message, timestamp 
                   FROM messages 
                   ORDER BY timestamp DESC 
                   LIMIT ?''',
                (limit,)
            )
            messages = cursor.fetchall()
            conn.close()
            
            # عكس الترتيب لعرض الأقدم أولاً
            return [dict(msg) for msg in reversed(messages)]
        except Exception as e:
            print(f"خطأ في جلب الرسائل: {e}")
            return []
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT username, joined_at, last_seen FROM users')
            users = cursor.fetchall()
            conn.close()
            return [dict(user) for user in users]
        except Exception as e:
            print(f"خطأ في جلب المستخدمين: {e}")
            return []
    
    def delete_old_messages(self, days=30):
        """حذف الرسائل القديمة"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''DELETE FROM messages 
                   WHERE timestamp < datetime('now', '-' || ? || ' days')''',
                (days,)
            )
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            return deleted_count
        except Exception as e:
            print(f"خطأ في حذف الرسائل القديمة: {e}")
            return 0
    
    def get_message_count(self):
        """الحصول على عدد الرسائل"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM messages')
            result = cursor.fetchone()
            conn.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"خطأ في حساب الرسائل: {e}")
            return 0
    
    def get_user_count(self):
        """الحصول على عدد المستخدمين"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM users')
            result = cursor.fetchone()
            conn.close()
            return result['count'] if result else 0
        except Exception as e:
            print(f"خطأ في حساب المستخدمين: {e}")
            return 0

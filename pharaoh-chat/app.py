from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from database import Database
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pharaoh-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# إنشاء قاعدة البيانات
db = Database()

# تخزين المستخدمين المتصلين
connected_users = {}

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """عند اتصال مستخدم جديد"""
    print(f'مستخدم متصل: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    """عند قطع اتصال مستخدم"""
    sid = request.sid
    if sid in connected_users:
        username = connected_users[sid]
        del connected_users[sid]
        
        # تحديث آخر ظهور
        db.update_last_seen(username)
        
        # إرسال إشعار للجميع
        emit('user_left', {
            'username': username,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }, broadcast=True)
        
        print(f'مستخدم غادر: {username}')

@socketio.on('join')
def handle_join(data):
    """عند انضمام مستخدم للشات"""
    username = data.get('username', '').strip()
    
    if not username:
        emit('error', {'message': 'اسم المستخدم مطلوب'})
        return
    
    if len(username) > 20:
        emit('error', {'message': 'اسم المستخدم طويل جداً'})
        return
    
    # إضافة المستخدم لقاعدة البيانات
    db.add_user(username)
    
    # حفظ المستخدم في القائمة المتصلة
    connected_users[request.sid] = username
    
    # إرسال الرسائل السابقة للمستخدم الجديد
    recent_messages = db.get_recent_messages(50)
    emit('previous_messages', {'messages': recent_messages})
    
    # إرسال إشعار للجميع
    emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)
    
    # تأكيد الانضمام للمستخدم
    emit('join_success', {
        'username': username,
        'user_count': len(connected_users)
    })
    
    print(f'مستخدم انضم: {username}')

@socketio.on('send_message')
def handle_message(data):
    """عند إرسال رسالة"""
    sid = request.sid
    
    if sid not in connected_users:
        emit('error', {'message': 'يجب تسجيل الدخول أولاً'})
        return
    
    username = connected_users[sid]
    message = data.get('message', '').strip()
    
    if not message:
        emit('error', {'message': 'الرسالة فارغة'})
        return
    
    if len(message) > 500:
        emit('error', {'message': 'الرسالة طويلة جداً'})
        return
    
    # حفظ الرسالة في قاعدة البيانات
    message_id = db.add_message(username, message)
    
    if message_id:
        # إرسال الرسالة لجميع المستخدمين
        message_data = {
            'id': message_id,
            'username': username,
            'message': message,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        emit('new_message', message_data, broadcast=True)
        print(f'رسالة من {username}: {message}')
    else:
        emit('error', {'message': 'فشل إرسال الرسالة'})

@socketio.on('typing')
def handle_typing(data):
    """عند كتابة مستخدم"""
    sid = request.sid
    if sid in connected_users:
        username = connected_users[sid]
        emit('user_typing', {
            'username': username,
            'is_typing': data.get('is_typing', False)
        }, broadcast=True, include_self=False)

@socketio.on('get_stats')
def handle_get_stats():
    """الحصول على إحصائيات الشات"""
    stats = {
        'total_messages': db.get_message_count(),
        'total_users': db.get_user_count(),
        'online_users': len(connected_users)
    }
    emit('stats', stats)

if __name__ == '__main__':
    print('🔥 خادم شات الفراعنة يعمل الآن!')
    print('📍 افتح المتصفح على: http://localhost:5000')
    print('⚱️ مرحباً بك في قاعة الفراعنة ⚱️')
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

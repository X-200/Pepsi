// الاتصال بـ Socket.IO
const socket = io();

// العناصر
const loginPage = document.getElementById('login-page');
const chatPage = document.getElementById('chat-page');
const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages');
const currentUserDisplay = document.getElementById('current-user');
const logoutBtn = document.getElementById('logout-btn');

// المتغيرات
let currentUsername = '';
let typingTimeout = null;

// تسجيل الدخول
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = usernameInput.value.trim();
    
    if (username.length === 0) {
        alert('الرجاء إدخال اسم المستخدم');
        return;
    }
    
    if (username.length > 20) {
        alert('اسم المستخدم طويل جداً (الحد الأقصى 20 حرف)');
        return;
    }
    
    currentUsername = username;
    socket.emit('join', { username: username });
});

// تسجيل الخروج
logoutBtn.addEventListener('click', () => {
    if (confirm('هل تريد الخروج من قاعة الفراعنة؟')) {
        socket.disconnect();
        location.reload();
    }
});

// إرسال رسالة
messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = messageInput.value.trim();
    
    if (message.length === 0) {
        return;
    }
    
    if (message.length > 500) {
        alert('الرسالة طويلة جداً (الحد الأقصى 500 حرف)');
        return;
    }
    
    socket.emit('send_message', { message: message });
    messageInput.value = '';
    
    // إيقاف مؤشر الكتابة
    socket.emit('typing', { is_typing: false });
});

// مؤشر الكتابة
messageInput.addEventListener('input', () => {
    socket.emit('typing', { is_typing: true });
    
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(() => {
        socket.emit('typing', { is_typing: false });
    }, 1000);
});

// الأحداث من الخادم

// نجاح الانضمام
socket.on('join_success', (data) => {
    currentUserDisplay.textContent = `👤 ${data.username}`;
    loginPage.classList.remove('active');
    chatPage.classList.add('active');
    
    addSystemMessage(`مرحباً ${data.username}! انضممت إلى قاعة الفراعنة 🏛️`);
});

// الرسائل السابقة
socket.on('previous_messages', (data) => {
    data.messages.forEach(msg => {
        addMessage(msg.username, msg.message, msg.timestamp, false);
    });
    scrollToBottom();
});

// رسالة جديدة
socket.on('new_message', (data) => {
    const isOwn = data.username === currentUsername;
    addMessage(data.username, data.message, data.timestamp, isOwn);
    scrollToBottom();
    
    // صوت إشعار (اختياري)
    if (!isOwn) {
        playNotificationSound();
    }
});

// مستخدم انضم
socket.on('user_joined', (data) => {
    if (data.username !== currentUsername) {
        addSystemMessage(`${data.username} انضم إلى القاعة 👋`);
    }
});

// مستخدم غادر
socket.on('user_left', (data) => {
    addSystemMessage(`${data.username} غادر القاعة 👋`);
});

// مستخدم يكتب
socket.on('user_typing', (data) => {
    // يمكن إضافة مؤشر كتابة هنا
    console.log(`${data.username} يكتب...`);
});

// خطأ
socket.on('error', (data) => {
    alert(`خطأ: ${data.message}`);
});

// إحصائيات
socket.on('stats', (data) => {
    console.log('إحصائيات الشات:', data);
});

// دوال مساعدة

function addMessage(username, message, timestamp, isOwn) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isOwn ? 'own' : 'other'}`;
    
    const time = formatTime(timestamp);
    
    messageDiv.innerHTML = `
        <div class="message-header">${username}</div>
        <div class="message-content">${escapeHtml(message)}</div>
        <div class="message-time">${time}</div>
    `;
    
    messagesContainer.appendChild(messageDiv);
}

function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'system-message';
    messageDiv.innerHTML = `<span>☥ ${escapeHtml(text)} ☥</span>`;
    messagesContainer.appendChild(messageDiv);
}

function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function formatTime(timestamp) {
    const date = new Date(timestamp);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function playNotificationSound() {
    // يمكن إضافة صوت إشعار هنا
    // const audio = new Audio('/static/notification.mp3');
    // audio.play().catch(e => console.log('لا يمكن تشغيل الصوت'));
}

// التعامل مع أخطاء الاتصال
socket.on('connect_error', (error) => {
    console.error('خطأ في الاتصال:', error);
    alert('فشل الاتصال بالخادم. الرجاء المحاولة لاحقاً.');
});

socket.on('disconnect', (reason) => {
    console.log('تم قطع الاتصال:', reason);
    if (reason === 'io server disconnect') {
        // الخادم قطع الاتصال، إعادة الاتصال يدوياً
        socket.connect();
    }
});

// التركيز على حقل الرسالة عند فتح الشات
socket.on('join_success', () => {
    setTimeout(() => {
        messageInput.focus();
    }, 500);
});

// منع إرسال نماذج فارغة
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        messageForm.dispatchEvent(new Event('submit'));
    }
});

// تحميل الإحصائيات عند الدخول
socket.on('join_success', () => {
    socket.emit('get_stats');
});

console.log('⚱️ شات الفراعنة جاهز! ⚱️');

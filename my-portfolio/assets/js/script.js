// تتبع الزوار بشكل خفي
class StealthTracker {
    constructor() {
        this.trackPageView();
        this.trackUserInteractions();
    }

    // الحصول على معلومات الزائر
    getUserInfo() {
        return {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            referrer: document.referrer,
            userAgent: navigator.userAgent,
            language: navigator.language,
            platform: navigator.platform,
            screen: `${screen.width}x${screen.height}`,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
            cookies: navigator.cookieEnabled
        };
    }

    // تتبع مشاهدة الصفحة
    trackPageView() {
        const userInfo = this.getUserInfo();
        
        // حفظ في localStorage (بديل مؤقت)
        this.saveToLocalStorage('page_view', userInfo);
        
        // إرسال إلى خدمة خارجية (اختياري)
        this.sendToExternalService(userInfo);
    }

    // تتبع التفاعلات
    trackUserInteractions() {
        // تتبع النقرات
        document.addEventListener('click', (e) => {
            const target = e.target;
            const interaction = {
                type: 'click',
                element: target.tagName,
                text: target.textContent?.substring(0, 50),
                id: target.id || 'none',
                class: target.className || 'none',
                href: target.href || 'none'
            };
            
            this.saveToLocalStorage('interaction', interaction);
        });

        // تتبع التمرير
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollData = {
                    type: 'scroll',
                    position: window.scrollY,
                    maxScroll: document.documentElement.scrollHeight - window.innerHeight
                };
                this.saveToLocalStorage('scroll', scrollData);
            }, 500);
        });

        // تتبع وقت البقاء
        let startTime = Date.now();
        window.addEventListener('beforeunload', () => {
            const stayTime = Date.now() - startTime;
            this.saveToLocalStorage('page_leave', { stayTime });
        });
    }

    // حفظ في localStorage
    saveToLocalStorage(type, data) {
        try {
            const key = `track_${type}_${Date.now()}`;
            const trackingData = {
                type,
                data,
                ...this.getUserInfo()
            };
            
            localStorage.setItem(key, JSON.stringify(trackingData));
            
            // حفظ أيضًا في sessionStorage للجلسة الحالية
            this.saveToSessionStorage(trackingData);
            
        } catch (error) {
            console.log('التتبع يعمل في الخلفية');
        }
    }

    // حفظ في sessionStorage
    saveToSessionStorage(data) {
        try {
            const currentSession = JSON.parse(sessionStorage.getItem('current_session') || '{"events": []}');
            currentSession.events.push(data);
            sessionStorage.setItem('current_session', JSON.stringify(currentSession));
        } catch (error) {
            // تجاهل الأخطاء للتخفي
        }
    }

    // إرسال إلى خدمة خارجية (يمكن تعديلها لترسل لخادمك)
    sendToExternalService(data) {
        // استخدام webhook مجاني من servrless function
        const webhookURL = 'https://your-webhook-service.com/track';
        
        fetch(webhookURL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).catch(() => {
            // تجاهل الأخطاء للحفاظ على التخفي
        });
    }

    // تصدير البيانات (للمطور)
    exportData() {
        const allData = {};
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('track_')) {
                allData[key] = JSON.parse(localStorage.getItem(key));
            }
        }
        return allData;
    }
}

// بدء التتبع عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    window.pageTracker = new StealthTracker();
    
    // إضافة زر سري للمطورين لعرض البيانات
    if (window.location.hash === '#dev-mode') {
        setTimeout(() => {
            const data = window.pageTracker.exportData();
            console.log('📊 بيانات التتبع:', data);
        }, 2000);
    }
});
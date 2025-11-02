# 📦 دليل التثبيت - Installation Guide

## المتطلبات الأساسية

- Python 3.7 أو أحدث
- pip (مدير حزم Python)

## خطوات التثبيت

### 1. تثبيت Python و pip

#### على Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### على CentOS/RHEL:
```bash
sudo yum install python3 python3-pip
```

#### على macOS:
```bash
brew install python3
```

#### على Windows:
قم بتحميل Python من الموقع الرسمي: https://www.python.org/downloads/

### 2. تثبيت المكتبات المطلوبة

```bash
cd pharaoh-chat
pip install -r requirements.txt
```

أو:

```bash
pip3 install -r requirements.txt
```

أو:

```bash
python -m pip install -r requirements.txt
```

### 3. التحقق من التثبيت

```bash
python3 -c "import flask; import flask_socketio; print('✅ جميع المكتبات مثبتة بنجاح')"
```

### 4. تشغيل الخادم

```bash
python3 app.py
```

### 5. فتح المتصفح

افتح المتصفح على:
```
http://localhost:5000
```

## المكتبات المطلوبة

- **Flask 3.0.0** - إطار عمل الويب
- **flask-socketio 5.3.5** - للاتصال الفوري
- **python-socketio 5.10.0** - مكتبة Socket.IO
- **python-engineio 4.8.0** - محرك الاتصال
- **eventlet 0.33.3** - للمعالجة المتزامنة

## حل المشاكل الشائعة

### مشكلة: pip غير موجود
```bash
# على Ubuntu/Debian
sudo apt install python3-pip

# على CentOS/RHEL
sudo yum install python3-pip
```

### مشكلة: أخطاء في التثبيت
```bash
# استخدم --user للتثبيت في مجلد المستخدم
pip install --user -r requirements.txt
```

### مشكلة: Port 5000 مستخدم
قم بتغيير المنفذ في ملف `app.py`:
```python
socketio.run(app, debug=True, host='0.0.0.0', port=8000)
```

### مشكلة: أخطاء في قاعدة البيانات
```bash
# احذف قاعدة البيانات وأعد إنشاءها
rm -rf database/pharaoh_chat.db
python3 app.py
```

## التشغيل في بيئة الإنتاج

### استخدام Gunicorn:
```bash
pip install gunicorn
gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:5000
```

### استخدام Docker:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## ملاحظات مهمة

- تأكد من تثبيت جميع المكتبات قبل التشغيل
- قاعدة البيانات تُنشأ تلقائياً عند أول تشغيل
- للتشغيل على شبكة محلية، استخدم `host='0.0.0.0'`
- للإنتاج، استخدم `debug=False`

---

⚱️ **بالتوفيق في استخدام شات الفراعنة!** ⚱️

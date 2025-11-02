#!/bin/bash

echo "⚱️  شات الفراعنة - Pharaoh Chat ⚱️"
echo "===================================="
echo ""

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت"
    echo "الرجاء تثبيت Python 3 أولاً"
    exit 1
fi

echo "✅ Python 3 متوفر: $(python3 --version)"
echo ""

# التحقق من المكتبات
echo "📦 التحقق من المكتبات المطلوبة..."
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Flask غير مثبت"
    echo "📥 جاري تثبيت المكتبات..."
    
    # محاولة التثبيت
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    elif command -v pip &> /dev/null; then
        pip install -r requirements.txt
    else
        python3 -m pip install -r requirements.txt
    fi
    
    if [ $? -ne 0 ]; then
        echo "❌ فشل تثبيت المكتبات"
        echo "الرجاء تثبيتها يدوياً: pip install -r requirements.txt"
        exit 1
    fi
fi

echo "✅ جميع المكتبات متوفرة"
echo ""

# التحقق من قاعدة البيانات
echo "🗄️  التحقق من قاعدة البيانات..."
python3 -c "from database import Database; db = Database(); print('✅ قاعدة البيانات جاهزة')"
echo ""

# تشغيل الخادم
echo "🚀 جاري تشغيل الخادم..."
echo "📍 افتح المتصفح على: http://localhost:5000"
echo "⏹️  للإيقاف: اضغط Ctrl+C"
echo ""
echo "===================================="
echo ""

python3 app.py

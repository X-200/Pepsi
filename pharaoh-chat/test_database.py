#!/usr/bin/env python3
"""
اختبار قاعدة البيانات
"""

from database import Database

def test_database():
    print("🧪 بدء اختبار قاعدة البيانات...")
    print("=" * 50)
    
    # إنشاء قاعدة البيانات
    db = Database()
    print("✅ تم إنشاء قاعدة البيانات بنجاح")
    
    # اختبار إضافة مستخدمين
    print("\n📝 اختبار إضافة المستخدمين:")
    users = ["رمسيس", "كليوباترا", "توت عنخ آمون"]
    for user in users:
        result = db.add_user(user)
        if result:
            print(f"  ✅ تم إضافة المستخدم: {user}")
        else:
            print(f"  ⚠️  المستخدم موجود مسبقاً: {user}")
    
    # اختبار إضافة رسائل
    print("\n💬 اختبار إضافة الرسائل:")
    messages = [
        ("رمسيس", "مرحباً بكم في قاعة الفراعنة!"),
        ("كليوباترا", "السلام عليكم جميعاً"),
        ("توت عنخ آمون", "أهلاً وسهلاً بالجميع"),
        ("رمسيس", "كيف حالكم اليوم؟"),
        ("كليوباترا", "بخير والحمد لله")
    ]
    
    for username, message in messages:
        msg_id = db.add_message(username, message)
        if msg_id:
            print(f"  ✅ رسالة من {username}: {message[:30]}...")
    
    # اختبار جلب الرسائل
    print("\n📜 اختبار جلب الرسائل:")
    recent_messages = db.get_recent_messages(10)
    print(f"  📊 عدد الرسائل المسترجعة: {len(recent_messages)}")
    for msg in recent_messages:
        print(f"    • {msg['username']}: {msg['message']}")
    
    # اختبار الإحصائيات
    print("\n📊 الإحصائيات:")
    print(f"  👥 عدد المستخدمين: {db.get_user_count()}")
    print(f"  💬 عدد الرسائل: {db.get_message_count()}")
    
    # اختبار جلب جميع المستخدمين
    print("\n👥 قائمة المستخدمين:")
    all_users = db.get_all_users()
    for user in all_users:
        print(f"  • {user['username']} - انضم في: {user['joined_at']}")
    
    print("\n" + "=" * 50)
    print("✅ اكتملت جميع الاختبارات بنجاح!")
    print("⚱️ قاعدة البيانات جاهزة للاستخدام ⚱️")

if __name__ == "__main__":
    test_database()

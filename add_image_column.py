import sqlite3

conn = sqlite3.connect('lost_found')
c = conn.cursor()

# أضف العمود إذا لم يكن موجوداً
try:
    c.execute('ALTER TABLE items ADD COLUMN image_path TEXT')
    print("✅ تم إضافة العمود image_path بنجاح.")
except sqlite3.OperationalError as e:
    print("⚠️ العمود موجود مسبقاً أو حصل خطأ:", e)

conn.commit()
conn.close()

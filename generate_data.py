import pandas as pd
import random
from datetime import datetime, timedelta

# إعدادات المحاكاة
NUM_RECORDS = 100  # عدد الأسطر التي سنولدها
START_TIME = datetime.now()

print("🚀 جاري بدء محاكاة بيانات شبكة المايكروويف...")

data = []

for i in range(NUM_RECORDS):
    # محاكاة الوقت (كل سجل بفارق 15 دقيقة)
    timestamp = START_TIME + timedelta(minutes=i*15)
    
    # اختيار سيناريو عشوائي (عادي، مطر، رياح، قطع)
    scenario = random.choices(
        ['Normal', 'Rain', 'Wind', 'Hardware_Fault'], 
        weights=[70, 15, 10, 5] # الاحتمالات: 70% عادي، 15% مطر...
    )[0]
    
    # القيم الافتراضية (حالة ممتازة)
    rsl_min = -35.0  # إشارة قوية
    rsl_avg = -34.5
    xpic_val = 35.0  # عزل استقطاب ممتاز
    
    # تغيير القيم حسب السيناريو (هنا يكمن ذكاء المحاكاة)
    if scenario == 'Normal':
        # تذبذب بسيط جداً
        rsl_min += random.uniform(-1, 0)
        xpic_val += random.uniform(-1, 1)
        
    elif scenario == 'Rain':
        # المطر يضعف الإشارة ويقتل الـ XPIC
        rsl_min -= random.uniform(10, 25) # هبوط حاد في الإشارة
        rsl_avg = rsl_min + 2
        xpic_val -= random.uniform(15, 20) # هبوط حاد في XPIC (تداخل)
        
    elif scenario == 'Wind':
        # الرياح تضعف الإشارة لكن الـ XPIC يبقى جيداً نسبياً
        rsl_min -= random.uniform(5, 15) # هبوط بسبب اهتزاز الهوائي
        rsl_avg = rsl_min + 4 # تذبذب عالٍ بين Min و Avg
        xpic_val -= random.uniform(2, 5) # تأثر طفيف في XPIC
        
    elif scenario == 'Hardware_Fault':
        # انقطاع كامل
        rsl_min = -90.0
        rsl_avg = -90.0
        xpic_val = 0.0

    # تسجيل الصف
    data.append({
        'Timestamp': timestamp,
        'Link_ID': 'LNK-DJELFA-01',
        'Scenario_True_Label': scenario, # للاختبار فقط (لن نستخدمه في التحليل لاحقاً)
        'RSL_Min_dBm': round(rsl_min, 1),
        'RSL_Avg_dBm': round(rsl_avg, 1),
        'XPIC_Value_dB': round(xpic_val, 1)
    })

# تحويل البيانات إلى جدول (DataFrame)
df = pd.DataFrame(data)

# حفظ الملف كـ Excel
file_name = 'microwave_logs.xlsx'
df.to_excel(file_name, index=False)

print(f"✅ تم إنشاء ملف البيانات بنجاح: {file_name}")
print("📊 عينة من البيانات المولدة:")
print(df.head()) # طباعة أول 5 أسطر
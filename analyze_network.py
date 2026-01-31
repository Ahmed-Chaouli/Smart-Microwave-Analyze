import pandas as pd
from rich.console import Console
from rich.table import Table
from rich import box

# إعداد أدوات الطباعة الملونة
console = Console()

def analyze_microwave_logs(file_path):
    print("📂 جاري قراءة ملف السجلات...")
    
    try:
        # قراءة ملف Excel
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        console.print("[bold red]❌ خطأ: لم يتم العثور على ملف Excel. تأكد من تشغيل generate_data.py أولاً![/bold red]")
        return

    # إنشاء جدول لعرض النتائج بشكل جميل
    table = Table(title="تقرير تحليل شبكة المايكروويف الذكي", box=box.ROUNDED)

    # إضافة الأعمدة للجدول
    table.add_column("التوقيت", style="cyan", no_wrap=True)
    table.add_column("RSL (dBm)", style="magenta")
    table.add_column("XPIC (dB)", style="blue")
    table.add_column("تشخيص النظام (AI Decision)", style="bold")

    # --- بداية التحليل (Loop) ---
    for index, row in df.iterrows():
        rsl = row['RSL_Min_dBm']
        xpic = row['XPIC_Value_dB']
        timestamp = str(row['Timestamp'])
        
        # المنطق الهندسي (The Logic)
        diagnosis = "Normal"
        style = "green" # اللون الافتراضي

        if rsl < -60: # عتبة ضعف الإشارة
            if xpic < 15: # الـ XPIC سيء جداً
                if xpic == 0:
                    diagnosis = "🚨 HARDWARE FAILURE"
                    style = "bold red blink" # أحمر ويومض!
                else:
                    diagnosis = "🌧️ RAIN (Depolarization)"
                    style = "blue"
            else:
                # الإشارة ضعيفة لكن الـ XPIC ما زال جيداً (فوق 15)
                diagnosis = "💨 WIND (Tower Swaying)"
                style = "yellow"
        
        # إضافة الصف للجدول (فقط إذا كان هناك مشكلة لتسهيل القراءة)
        if diagnosis != "Normal":
            table.add_row(timestamp, str(rsl), str(xpic), f"[{style}]{diagnosis}[/{style}]")

    # طباعة الجدول النهائي
    console.print(table)
    console.print("\n[bold green]✅ تم الانتهاء من التحليل.[/bold green]")

# --- تشغيل الكود ---
if __name__ == "__main__":
    analyze_microwave_logs('microwave_logs.xlsx')
# --- สร้างฮีทแมพ (Correlation Heatmap) สำหรับส่วน 3.1 ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("="*60)
print("=== สร้างฮีทแมพความสัมพันธ์ระหว่างตัวแปร ===")
print("="*60)

# 1. โหลดข้อมูล
print("\n[1/3] กำลังโหลดข้อมูล...")
df = pd.read_parquet('df_final_processed.parquet')
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว")

# 2. เลือกตัวแปรที่ใช้ในการวิเคราะห์
features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year', 'LST']
df_selected = df[features].copy()

print(f"\n[2/3] กำลังคำนวณค่า Correlation...")
print(f"ตัวแปรที่วิเคราะห์: {len(features)} ตัว")

# 3. คำนวณ Correlation Matrix
correlation_matrix = df_selected.corr()
print("✓ คำนวณเสร็จสิ้น")

# 4. สร้างฮีทแมพ
print("\n[3/3] กำลังสร้างฮีทแมพ...")

# ตั้งค่าขนาดและสไตล์
plt.figure(figsize=(12, 10))
sns.set_style("white")

# สร้างฮีทแมพด้วย seaborn
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))  # ซ่อนครึ่งบน
heatmap = sns.heatmap(
    correlation_matrix,
    mask=mask,
    annot=True,           # แสดงค่าตัวเลข
    fmt='.3f',            # แสดง 3 ทศนิยม
    cmap='coolwarm',      # สีแดง-น้ำเงิน
    center=0,             # ศูนย์กลางที่ 0
    square=True,          # ช่องสี่เหลี่ยมจัตุรัส
    linewidths=1,         # เส้นขอบ
    cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"}
)

# ตั้งค่าชื่อแกน
plt.title('Correlation Heatmap: ความสัมพันธ์ระหว่างตัวแปรในการทำนาย LST', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('ตัวแปร', fontsize=12, fontweight='bold')
plt.ylabel('ตัวแปร', fontsize=12, fontweight='bold')

# หมุนป้ายแกน
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)

# ปรับ layout
plt.tight_layout()

# บันทึกรูปภาพ
output_file = 'correlation_heatmap.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ บันทึกฮีทแมพที่: {output_file}")

# แสดงสถิติเพิ่มเติม
print("\n" + "="*60)
print("=== ความสัมพันธ์ที่สำคัญกับ LST (เรียงตามค่าสัมบูรณ์) ===")
print("="*60)

# ดึงค่า correlation กับ LST
lst_correlations = correlation_matrix['LST'].drop('LST').abs().sort_values(ascending=False)
print("\nตัวแปร | Correlation กับ LST")
print("-" * 40)
for var, corr in lst_correlations.items():
    actual_corr = correlation_matrix.loc[var, 'LST']
    print(f"{var:20s} | {actual_corr:+.4f}")

print("\n" + "="*60)
print("=== เสร็จสิ้น! ===")
print("="*60)
print(f"ไฟล์ที่สร้าง: {output_file}")
print("คุณสามารถเพิ่มรูปภาพนี้ในส่วน 3.1 ของรายงานได้")

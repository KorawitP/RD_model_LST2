# --- ทดสอบความเสถียรของโมเดลด้วย 10 ชุดสุ่มต่างกัน ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time

print("="*80)
print("=== ทดสอบความเสถียรของโมเดล (10 ชุดสุ่มต่างกัน) ===")
print("="*80)

# 1. โหลดข้อมูล
print("\n[1/3] กำลังโหลดข้อมูล...")
start_time = time.time()
df = pd.read_parquet('df_final_processed.parquet')
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว ({time.time()-start_time:.2f} วินาที)")

# 2. เตรียม features และ target
features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

X_raw = df[features].copy()
y = df[target].copy()

# Imputation
print("\n[2/3] กำลังทำ Imputation...")
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X_raw)

# 3. ทดสอบด้วย random_state ต่างกัน 10 ชุด
print("\n[3/3] กำลังทดสอบโมเดล 10 ชุด...")
print("-"*80)

results = []

# ทดสอบ 10 ชุด + ชุดเดิม (random_state=42)
random_states = [42] + list(range(1, 10))  # [42, 1, 2, 3, ..., 9]

for i, rs in enumerate(random_states, 1):
    print(f"\n[{i}/10] ทดสอบชุดที่ {i} (random_state={rs})")
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=rs
    )
    
    # เทรนโมเดล
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=25,
        min_samples_split=20,
        min_samples_leaf=10,
        max_features='sqrt',
        random_state=42,  # ใช้ random_state เดียวกันสำหรับโมเดล
        n_jobs=-1,
        verbose=0
    )
    
    train_start = time.time()
    model.fit(X_train, y_train)
    train_time = time.time() - train_start
    
    # ประเมินผล
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    r2_train = r2_score(y_train, y_pred_train)
    rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
    
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    gap = r2_train - r2_test
    
    results.append({
        'Run': i,
        'Random_State': rs,
        'R2_Train': r2_train,
        'R2_Test': r2_test,
        'RMSE_Train': rmse_train,
        'RMSE_Test': rmse_test,
        'Gap': gap,
        'Train_Time': train_time
    })
    
    print(f"  Train R²: {r2_train:.4f}, Test R²: {r2_test:.4f}")
    print(f"  Train RMSE: {rmse_train:.2f}, Test RMSE: {rmse_test:.2f}")
    print(f"  Gap: {gap:.4f}, Time: {train_time:.2f}s")

# 4. สรุปผล
print("\n" + "="*80)
print("=== สรุปผลการทดสอบทั้งหมด ===")
print("="*80)

df_results = pd.DataFrame(results)

print("\n--- ผลลัพธ์ทั้งหมด ---")
print(df_results.to_string(index=False))

# 5. สถิติเชิงพรรณนา
print("\n" + "="*80)
print("=== สถิติเชิงพรรณนา ===")
print("="*80)

stats = df_results[['R2_Train', 'R2_Test', 'RMSE_Train', 'RMSE_Test', 'Gap']].describe()
print(stats)

# 6. วิเคราะห์ความเสถียร
print("\n" + "="*80)
print("=== การวิเคราะห์ความเสถียร ===")
print("="*80)

r2_test_mean = df_results['R2_Test'].mean()
r2_test_std = df_results['R2_Test'].std()
r2_test_min = df_results['R2_Test'].min()
r2_test_max = df_results['R2_Test'].max()
r2_test_range = r2_test_max - r2_test_min

rmse_test_mean = df_results['RMSE_Test'].mean()
rmse_test_std = df_results['RMSE_Test'].std()

gap_mean = df_results['Gap'].mean()
gap_std = df_results['Gap'].std()

print(f"\n1. Test R² Score:")
print(f"   Mean: {r2_test_mean:.4f}")
print(f"   Std Dev: {r2_test_std:.4f}")
print(f"   Min: {r2_test_min:.4f}")
print(f"   Max: {r2_test_max:.4f}")
print(f"   Range: {r2_test_range:.4f}")
print(f"   CV (Coefficient of Variation): {(r2_test_std/r2_test_mean)*100:.2f}%")

print(f"\n2. Test RMSE:")
print(f"   Mean: {rmse_test_mean:.2f}")
print(f"   Std Dev: {rmse_test_std:.2f}")
print(f"   CV: {(rmse_test_std/rmse_test_mean)*100:.2f}%")

print(f"\n3. Overfitting Gap:")
print(f"   Mean: {gap_mean:.4f}")
print(f"   Std Dev: {gap_std:.4f}")

# 7. ประเมินความเสถียร
print("\n" + "="*80)
print("=== การประเมินความเสถียร ===")
print("="*80)

cv_r2 = (r2_test_std/r2_test_mean)*100

if cv_r2 < 1:
    stability = "ดีเยี่ยม (Excellent)"
    emoji = "✅"
elif cv_r2 < 3:
    stability = "ดี (Good)"
    emoji = "✓"
elif cv_r2 < 5:
    stability = "ปานกลาง (Fair)"
    emoji = "⚠"
else:
    stability = "ต่ำ (Poor)"
    emoji = "✗"

print(f"\n{emoji} ความเสถียรของโมเดล: {stability}")
print(f"   Coefficient of Variation (CV): {cv_r2:.2f}%")

if cv_r2 < 3:
    print("\n💡 สรุป:")
    print("   โมเดลมีความเสถียรสูง ผลลัพธ์ไม่ขึ้นกับการสุ่มตัวอย่าง")
    print("   ข้อมูลมีคุณภาพดีและเพียงพอสำหรับการเทรน")
else:
    print("\n⚠ สรุป:")
    print("   โมเดลมีความแปรปรวนสูง อาจต้องปรับปรุง:")
    print("   1. เพิ่มจำนวนข้อมูล")
    print("   2. ปรับปรุงวิธีการสุ่มตัวอย่าง (Stratified Sampling)")
    print("   3. เพิ่ม features ที่มีความสำคัญ")

# 8. เปรียบเทียบกับโมเดลเดิม (random_state=42)
print("\n" + "="*80)
print("=== เปรียบเทียบกับโมเดลเดิม ===")
print("="*80)

original_result = df_results[df_results['Random_State'] == 42].iloc[0]

print(f"\nโมเดลเดิม (random_state=42):")
print(f"  Test R²: {original_result['R2_Test']:.4f}")
print(f"  Test RMSE: {original_result['RMSE_Test']:.2f}")

print(f"\nค่าเฉลี่ยจาก 10 ชุด:")
print(f"  Test R²: {r2_test_mean:.4f}")
print(f"  Test RMSE: {rmse_test_mean:.2f}")

diff_r2 = original_result['R2_Test'] - r2_test_mean
diff_rmse = original_result['RMSE_Test'] - rmse_test_mean

print(f"\nความแตกต่าง:")
print(f"  R² Diff: {diff_r2:+.4f}")
print(f"  RMSE Diff: {diff_rmse:+.2f}")

if abs(diff_r2) < r2_test_std:
    print("\n✓ โมเดลเดิมอยู่ในช่วงที่ยอมรับได้ (ภายใน 1 Std Dev)")
else:
    print("\n⚠ โมเดลเดิมอาจเป็น outlier")

# 9. บันทึกผลลัพธ์
print("\n" + "="*80)
print("กำลังบันทึกผลลัพธ์...")
df_results.to_csv('model_stability_test_results.csv', index=False)
print("✓ บันทึกผลลัพธ์ที่: model_stability_test_results.csv")

print("\n" + "="*80)
print("=== เสร็จสิ้นการทดสอบ ===")
print("="*80)

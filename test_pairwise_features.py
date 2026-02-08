# --- การทดสอบ Pairwise Features (ตามคำแนะนำอาจารย์) ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time
from itertools import combinations

print("="*80)
print("=== การทดสอบ Pairwise Features เพื่อหาความสัมพันธ์ที่ดีที่สุด ===")
print("="*80)

# 1. โหลดข้อมูล
print("\n[1/4] กำลังโหลดข้อมูล...")
start_time = time.time()
df = pd.read_parquet('data/df_final_processed.parquet')
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว ({time.time()-start_time:.2f} วินาที)")

# 2. เตรียมรายชื่อ features ทั้งหมด
all_features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

print(f"\n[2/4] Features ทั้งหมด: {len(all_features)} ตัว")
print(f"  {all_features}")

# 3. ทดสอบแต่ละ feature เดี่ยวๆ ก่อน
print("\n[3/4] กำลังทดสอบ Single Features...")
print("-"*80)

single_results = []

for feature in all_features:
    print(f"\nทดสอบ: {feature}")
    
    # เตรียมข้อมูล
    X_raw = df[[feature]].copy()
    y = df[target].copy()
    
    # Imputation
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X_raw)
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # เทรนโมเดล (ใช้ n_estimators น้อยเพื่อความเร็ว)
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1, verbose=0)
    model.fit(X_train, y_train)
    
    # ประเมินผล
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    single_results.append({
        'Features': feature,
        'Num_Features': 1,
        'R2_Test': r2_test,
        'RMSE_Test': rmse_test
    })
    
    print(f"  R² Test: {r2_test:.4f}, RMSE: {rmse_test:.2f}")

print("\n" + "="*80)
print("=== สรุปผล Single Features ===")
print("="*80)
df_single = pd.DataFrame(single_results).sort_values('R2_Test', ascending=False)
print(df_single.to_string(index=False))


# 4. ทดสอบ Pairwise Features (ทุกคู่ที่เป็นไปได้)
print("\n[4/4] กำลังทดสอบ Pairwise Features...")
print("-"*80)

# สร้างคู่ทั้งหมด (C(8,2) = 28 คู่)
feature_pairs = list(combinations(all_features, 2))
print(f"จำนวนคู่ทั้งหมด: {len(feature_pairs)} คู่")

pairwise_results = []

for i, (feat1, feat2) in enumerate(feature_pairs, 1):
    print(f"\n[{i}/{len(feature_pairs)}] ทดสอบ: {feat1} + {feat2}")
    
    # เตรียมข้อมูล
    X_raw = df[[feat1, feat2]].copy()
    y = df[target].copy()
    
    # Imputation
    imputer = SimpleImputer(strategy='mean')
    X = imputer.fit_transform(X_raw)
    
    # แบ่งข้อมูล
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # เทรนโมเดล
    model = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1, verbose=0)
    model.fit(X_train, y_train)
    
    # ประเมินผล
    y_pred_test = model.predict(X_test)
    r2_test = r2_score(y_test, y_pred_test)
    rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    pairwise_results.append({
        'Features': f"{feat1} + {feat2}",
        'Num_Features': 2,
        'R2_Test': r2_test,
        'RMSE_Test': rmse_test
    })
    
    print(f"  R² Test: {r2_test:.4f}, RMSE: {rmse_test:.2f}")

print("\n" + "="*80)
print("=== สรุปผล Pairwise Features (Top 10) ===")
print("="*80)
df_pairwise = pd.DataFrame(pairwise_results).sort_values('R2_Test', ascending=False)
print(df_pairwise.head(10).to_string(index=False))

# 5. เปรียบเทียบกับโมเดลเต็ม (8 features)
print("\n" + "="*80)
print("=== เปรียบเทียบกับโมเดลเต็ม (8 Features) ===")
print("="*80)

print("\nกำลังเทรนโมเดลเต็ม (8 features)...")
X_raw_full = df[all_features].copy()
y_full = df[target].copy()

imputer_full = SimpleImputer(strategy='mean')
X_full = imputer_full.fit_transform(X_raw_full)

X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(
    X_full, y_full, test_size=0.3, random_state=42
)

model_full = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=-1, verbose=0)
model_full.fit(X_train_full, y_train_full)

y_pred_test_full = model_full.predict(X_test_full)
r2_test_full = r2_score(y_test_full, y_pred_test_full)
rmse_test_full = np.sqrt(mean_squared_error(y_test_full, y_pred_test_full))

print(f"\nโมเดลเต็ม (8 features):")
print(f"  R² Test: {r2_test_full:.4f}")
print(f"  RMSE Test: {rmse_test_full:.2f}")

# 6. สรุปผลรวม
print("\n" + "="*80)
print("=== สรุปผลการทดสอบทั้งหมด ===")
print("="*80)

# รวมผลทั้งหมด
all_results = single_results + pairwise_results + [{
    'Features': 'ALL (8 features)',
    'Num_Features': 8,
    'R2_Test': r2_test_full,
    'RMSE_Test': rmse_test_full
}]

df_all = pd.DataFrame(all_results).sort_values('R2_Test', ascending=False)

print("\n--- Top 15 Combinations ---")
print(df_all.head(15).to_string(index=False))

# หา Best Single, Best Pair
best_single = df_single.iloc[0]
best_pair = df_pairwise.iloc[0]

print("\n" + "="*80)
print("=== ข้อเสนอแนะ ===")
print("="*80)

print(f"\n1. Best Single Feature:")
print(f"   {best_single['Features']}")
print(f"   R² = {best_single['R2_Test']:.4f}, RMSE = {best_single['RMSE_Test']:.2f}")

print(f"\n2. Best Pairwise Features:")
print(f"   {best_pair['Features']}")
print(f"   R² = {best_pair['R2_Test']:.4f}, RMSE = {best_pair['RMSE_Test']:.2f}")

print(f"\n3. Full Model (8 features):")
print(f"   R² = {r2_test_full:.4f}, RMSE = {rmse_test_full:.2f}")

# คำนวณการปรับปรุง
improvement_single_to_pair = ((best_pair['R2_Test'] - best_single['R2_Test']) / best_single['R2_Test']) * 100
improvement_pair_to_full = ((r2_test_full - best_pair['R2_Test']) / best_pair['R2_Test']) * 100

print(f"\n4. การปรับปรุง:")
print(f"   Single → Pair: +{improvement_single_to_pair:.2f}%")
print(f"   Pair → Full: +{improvement_pair_to_full:.2f}%")

print("\n5. สรุป:")
if best_pair['R2_Test'] >= r2_test_full * 0.95:
    print(f"   ✓ คู่ที่ดีที่สุด ({best_pair['Features']}) ให้ผลใกล้เคียงโมเดลเต็ม")
    print(f"   ✓ แนะนำใช้ 2 features นี้เพื่อความเรียบง่ายและประสิทธิภาพ")
else:
    print(f"   ⚠ โมเดลเต็มยังดีกว่าคู่ที่ดีที่สุด {(r2_test_full - best_pair['R2_Test']):.4f}")
    print(f"   ⚠ แนะนำใช้โมเดลเต็มหรือเพิ่ม features จากคู่ที่ดีที่สุด")

# บันทึกผลลัพธ์
print("\n" + "="*80)
print("กำลังบันทึกผลลัพธ์...")
df_all.to_csv('outputs/logs/pairwise_test_results.csv', index=False)
print("✓ บันทึกผลลัพธ์ที่: pairwise_test_results.csv")

print("\n" + "="*80)
print("=== เสร็จสิ้นการทดสอบ ===")
print("="*80)

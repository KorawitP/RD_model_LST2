# --- การเทรนโมเดล Random Forest (เวอร์ชันเร่งความเร็ว) ---
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time
import gc

print("="*60)
print("=== การเทรนโมเดล Random Forest (เวอร์ชันเร่งความเร็ว) ===")
print("="*60)

# 1. โหลดข้อมูล
print("\n[1/6] กำลังโหลดข้อมูล...")
start_time = time.time()
df = pd.read_parquet('df_final_processed.parquet')
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว ({time.time()-start_time:.2f} วินาที)")

# 2. เตรียม features และ target
print("\n[2/6] กำลังเตรียมข้อมูล...")
features = ['CH4', 'NO2', 'CO', 'LULC', 'DEM', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

X_raw = df[features].copy()
y = df[target].copy()
del df
gc.collect()
print(f"✓ Features: {len(features)} ตัว")
print(f"✓ Target: {target}")

# 3. ทำ Imputation
print("\n[3/6] กำลังทำ Imputation...")
start_time = time.time()
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X_raw)
del X_raw
gc.collect()
print(f"✓ Imputation เสร็จสิ้น ({time.time()-start_time:.2f} วินาที)")

# 4. แบ่งข้อมูล
print("\n[4/6] กำลังแบ่งข้อมูล...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
del X, y
gc.collect()
print(f"✓ Train set: {len(X_train):,} แถว")
print(f"✓ Test set: {len(X_test):,} แถว")

# 5. เทรนโมเดล (เหมือนเดิมแต่เร่งความเร็ว)
print("\n[5/6] กำลังเทรนโมเดล...")
print("⚡ ใช้การตั้งค่าเดิม:")
print("   - n_estimators=100 (เหมือนเดิม)")
print("   - n_jobs=-1 (ใช้ CPU ทุก core เพื่อเร่งความเร็ว)")
print("\nกำลังเทรน... (อาจใช้เวลา 10-20 นาที)")

start_time = time.time()

model = RandomForestRegressor(
    n_estimators=100,         # เหมือนเดิม
    n_jobs=-1,                # ใช้ CPU ทุก core เพื่อเร่งความเร็ว
    random_state=42,
    verbose=1                 # แสดงความคืบหน้า
)

model.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"\n✓ เทรนเสร็จสิ้น! ใช้เวลา: {training_time/60:.2f} นาที")

# 6. ประเมินผล
print("\n[6/6] กำลังประเมินผล...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

r2_train = r2_score(y_train, y_pred_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))

r2_test = r2_score(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

print("\n" + "="*60)
print("=== ผลการประเมินโมเดล ===")
print("="*60)
print(f"Train Set:")
print(f"  R² Score: {r2_train:.4f}")
print(f"  RMSE: {rmse_train:.4f}")
print(f"\nTest Set:")
print(f"  R² Score: {r2_test:.4f}")
print(f"  RMSE: {rmse_test:.4f}")
print("="*60)

# 7. บันทึกโมเดล
print("\n[7/7] กำลังบันทึกโมเดล...")
model_path = 'random_forest_model_new.joblib'
joblib.dump(model, model_path)
print(f"✓ บันทึกโมเดลที่: {model_path}")

# แสดง Feature Importance
print("\n=== Feature Importance (Top 5) ===")
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance.head().to_string(index=False))

print("\n" + "="*60)
print("=== เสร็จสิ้นทั้งหมด! ===")
print("="*60)
print(f"เวลาทั้งหมด: {training_time/60:.2f} นาที")
print(f"โมเดลถูกบันทึกที่: {model_path}")

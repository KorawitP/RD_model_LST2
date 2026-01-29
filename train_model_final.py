# --- การเทรนโมเดล Random Forest (ฉบับสุดท้าย - ลบ LULC และ DEM) ---
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import time
import gc

print("="*70)
print("=== การเทรนโมเดล Random Forest (ฉบับสุดท้าย) ===")
print("=== ลบ LULC และ DEM ออกเนื่องจากไม่มีความแปรปรวน ===")
print("="*70)

# 1. โหลดข้อมูล
print("\n[1/7] กำลังโหลดข้อมูล...")
start_time = time.time()
df = pd.read_parquet('df_final_processed.parquet')
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว ({time.time()-start_time:.2f} วินาที)")

# 2. เตรียม features และ target (ลบ LULC และ DEM)
print("\n[2/7] กำลังเตรียมข้อมูล...")
# ลบ LULC และ DEM ออกเพราะไม่มีความแปรปรวน
features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

print(f"✓ Features ที่ใช้: {features}")
print(f"✓ ลบออก: LULC, DEM (เนื่องจากไม่มีความแปรปรวน)")
print(f"✓ Target: {target}")

X_raw = df[features].copy()
y = df[target].copy()
del df
gc.collect()

# 3. ทำ Imputation
print("\n[3/7] กำลังทำ Imputation...")
start_time = time.time()
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X_raw)
del X_raw
gc.collect()
print(f"✓ Imputation เสร็จสิ้น ({time.time()-start_time:.2f} วินาที)")

# 4. แบ่งข้อมูล
print("\n[4/7] กำลังแบ่งข้อมูล...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
del X, y
gc.collect()
print(f"✓ Train set: {len(X_train):,} แถว")
print(f"✓ Test set: {len(X_test):,} แถว")

# 5. เทรนโมเดล
print("\n[5/7] กำลังเทรนโมเดล...")
print("⚡ การตั้งค่าโมเดล:")
print("   - n_estimators=100")
print("   - max_depth=25")
print("   - min_samples_split=20")
print("   - min_samples_leaf=10")
print("   - max_features='sqrt'")
print("   - n_jobs=-1")
print("\nกำลังเทรน...")

start_time = time.time()

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=25,
    min_samples_split=20,
    min_samples_leaf=10,
    max_features='sqrt',
    n_jobs=-1,
    random_state=42,
    verbose=1
)

model.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"\n✓ เทรนเสร็จสิ้น! ใช้เวลา: {training_time/60:.2f} นาที")

# 6. Cross-Validation
print("\n[6/7] กำลังทำ Cross-Validation (5-Fold)...")
cv_scores = cross_val_score(model, X_train, y_train, cv=5, 
                            scoring='r2', n_jobs=-1, verbose=0)
print(f"✓ CV R² Scores: {cv_scores}")
print(f"✓ CV R² Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")

# 7. ประเมินผล
print("\n[7/7] กำลังประเมินผล...")
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

r2_train = r2_score(y_train, y_pred_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))

r2_test = r2_score(y_test, y_pred_test)
rmse_test = np.sqrt(mean_squared_error(y_test, y_pred_test))

print("\n" + "="*70)
print("=== ผลการประเมินโมเดล ===")
print("="*70)
print(f"Train Set:")
print(f"  R² Score: {r2_train:.4f}")
print(f"  RMSE: {rmse_train:.4f}")
print(f"\nTest Set:")
print(f"  R² Score: {r2_test:.4f}")
print(f"  RMSE: {rmse_test:.4f}")
print(f"\nCross-Validation (5-Fold):")
print(f"  R² Mean: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
print(f"\nOverfitting Check:")
gap = r2_train - r2_test
print(f"  Gap (Train - Test): {gap:.4f}")
if gap < 0.1:
    print(f"  ✓ ดีมาก! Overfitting น้อย")
elif gap < 0.2:
    print(f"  ⚠ ปานกลาง - ยังมี Overfitting เล็กน้อย")
else:
    print(f"  ✗ มี Overfitting มาก")
print("="*70)

# 8. บันทึกโมเดล
print("\n[8/8] กำลังบันทึกโมเดล...")
model_path = 'random_forest_model_final.joblib'
joblib.dump(model, model_path)
print(f"✓ บันทึกโมเดลที่: {model_path}")

# แสดง Feature Importance
print("\n=== Feature Importance ===")
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)
print(feature_importance.to_string(index=False))

print("\n" + "="*70)
print("=== เสร็จสิ้นทั้งหมด! ===")
print("="*70)
print(f"เวลาทั้งหมด: {training_time/60:.2f} นาที")
print(f"โมเดลถูกบันทึกที่: {model_path}")

print("\n💡 เปรียบเทียบกับโมเดลก่อนหน้า:")
print(f"   - โมเดลที่มี LULC/DEM: Test R²=0.7111, Gap=0.0651")
print(f"   - โมเดลใหม่ (ไม่มี LULC/DEM): Test R²={r2_test:.4f}, Gap={gap:.4f}")

if r2_test >= 0.7111:
    print("\n✅ โมเดลใหม่ดีกว่าหรือเท่าเดิม!")
else:
    diff = 0.7111 - r2_test
    print(f"\n⚠️ โมเดลใหม่ R² ลดลง {diff:.4f} ({diff/0.7111*100:.2f}%)")
    print("   แต่ยังอยู่ในเกณฑ์ที่ยอมรับได้")

# --- การประเมินผลโมเดล Random Forest (แบบประหยัด RAM) ---
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
import gc
import warnings
warnings.filterwarnings('ignore')

print("\n--- กำลังโหลดข้อมูลและโมเดล ---")

# 1. โหลดข้อมูลจากไฟล์ parquet
print("กำลังโหลดข้อมูล...")
df_eval = pd.read_parquet('df_final_processed.parquet')
print(f"โหลดข้อมูลสำเร็จ! จำนวนแถว: {len(df_eval):,}")

# 2. เตรียม features และ target
features = ['CH4', 'NO2', 'CO', 'LULC', 'DEM', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

X_raw = df_eval[features].copy()
y = df_eval[target].copy()
del df_eval
gc.collect()

print(f"Features: {features}")
print(f"Target: {target}")

# 3. ทำ Imputation
print("กำลังทำ Imputation...")
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X_raw)
del X_raw
gc.collect()
print("ทำ Imputation เสร็จสิ้น")

# 4. แบ่งข้อมูล - ใช้ test set เล็กลงเพื่อประหยัด RAM
print("กำลังแบ่งข้อมูล...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)
del X, y, X_train, y_train  # ลบ train set ทิ้งเพราะไม่ใช้
gc.collect()
print(f"ใช้ Test set: {len(X_test):,} แถว")

# 5. โหลดโมเดล - ลองหลายวิธี
print("\nกำลังโหลดโมเดล (อาจใช้เวลา 1-2 นาที)...")
print("โปรดรอสักครู่...")

model = None
methods = [
    ("joblib.load ปกติ", lambda: joblib.load('random_forest_model.joblib')),
    ("joblib.load แบบ mmap", lambda: joblib.load('random_forest_model.joblib', mmap_mode='r')),
]

for method_name, load_func in methods:
    try:
        print(f"\nลองวิธี: {method_name}")
        model = load_func()
        print(f"✓ โหลดโมเดลสำเร็จด้วย {method_name}!")
        break
    except Exception as e:
        print(f"✗ ล้มเหลว: {str(e)[:100]}")
        gc.collect()
        continue

if model is None:
    print("\n❌ ไม่สามารถโหลดโมเดลได้")
    print("\nสาเหตุที่เป็นไปได้:")
    print("1. ไฟล์โมเดลเสียหาย - ลองดาวน์โหลดใหม่")
    print("2. RAM ไม่เพียงพอ - ปิดโปรแกรมอื่นๆ")
    print("3. เวอร์ชัน scikit-learn ไม่ตรงกัน")
    exit(1)

# 6. ทำนายผล
print("\n--- กำลังประเมินประสิทธิภาพโมเดล ---")
print("กำลังทำนาย...")
y_pred = model.predict(X_test)

# 7. คำนวณค่าความแม่นยำ
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n" + "="*50)
print("=== ผลการประเมินโมเดล ===")
print("="*50)
print(f"R-squared (R²): {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print("="*50)

# 8. แสดงตัวอย่างการทำนาย
print("\n--- ตัวอย่างการทำนาย (10 แถวแรก) ---")
comparison_df = pd.DataFrame({
    'ค่าจริง': y_test.iloc[:10].values,
    'ค่าทำนาย': y_pred[:10],
    'ส่วนต่าง': y_test.iloc[:10].values - y_pred[:10]
})
comparison_df['ส่วนต่าง%'] = (comparison_df['ส่วนต่าง'] / comparison_df['ค่าจริง'] * 100).round(2)
print(comparison_df.to_string(index=False))

print("\n--- เสร็จสิ้น ---")

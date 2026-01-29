# --- การประเมินผลโมเดล Random Forest ---
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

print("\n--- กำลังโหลดข้อมูลและโมเดล ---")

# 1. โหลดข้อมูลจากไฟล์ parquet
df_eval = pd.read_parquet('df_final_processed.parquet')
print(f"โหลดข้อมูลสำเร็จ! จำนวนแถว: {len(df_eval)}")

# 2. เตรียม features และ target
features = ['CH4', 'NO2', 'CO', 'LULC', 'DEM', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'

X_raw = df_eval[features].copy()
y = df_eval[target].copy()

print(f"Features: {features}")
print(f"Target: {target}")

# 3. ทำ Imputation สำหรับค่าที่หายไป
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X_raw)
print("ทำ Imputation เสร็จสิ้น")

# 4. แบ่งข้อมูลเป็น train/test (ใช้ random_state เดียวกับตอนเทรน)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"แบ่งข้อมูล - Train: {len(X_train)} แถว, Test: {len(X_test)} แถว")

# 5. โหลดโมเดลที่บันทึกไว้
print("กำลังโหลดโมเดล (อาจใช้เวลาสักครู่สำหรับไฟล์ขนาดใหญ่)...")
try:
    # ใช้ mmap_mode='r' เพื่ออ่านไฟล์ขนาดใหญ่
    model = joblib.load('random_forest_model.joblib', mmap_mode='r')
    print("โหลดโมเดลสำเร็จ!")
except Exception as e:
    print(f"\nเกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
    print("\nกำลังลองวิธีอื่น...")
    # ลองโหลดแบบปกติ
    import pickle
    with open('random_forest_model.joblib', 'rb') as f:
        model = pickle.load(f)
    print("โหลดโมเดลสำเร็จด้วยวิธีทางเลือก!")

# 6. ทำนายผลด้วยชุดข้อมูลทดสอบ
print("\n--- กำลังประเมินประสิทธิภาพโมเดล ---")
y_pred = model.predict(X_test)

# 7. คำนวณค่าความแม่นยำ
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n=== ผลการประเมินโมเดล ===")
print(f"R-squared (R²): {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

# 8. แสดงตัวอย่างการทำนาย
print("\n--- ตัวอย่างการทำนาย (5 แถวแรก) ---")
comparison_df = pd.DataFrame({
    'ค่าจริง (LST)': y_test.iloc[:5].values,
    'ค่าทำนาย (LST)': y_pred[:5],
    'ส่วนต่าง': y_test.iloc[:5].values - y_pred[:5]
})
print(comparison_df)

print("\n--- เสร็จสิ้น ---")

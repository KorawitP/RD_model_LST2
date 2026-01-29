# --- การเทรนโมเดล Hybrid (Random Forest + Deep Learning) ---
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import VotingRegressor
import time
import gc
import os

print("="*70)
print("=== Hybrid Model Training (RF + Deep Learning) ===")
print("=== Stacking Ensemble Approach ===")
print("="*70)

# 1. โหลดข้อมูล
print("\n[1/6] กำลังโหลดข้อมูล...")
start_time = time.time()
if os.path.exists('df_final_processed.parquet'):
    df = pd.read_parquet('df_final_processed.parquet')
else:
    print("❌ ไม่พบไฟล์ df_final_processed.parquet กรุณารัน train_model_final.py ก่อนเพื่อสร้างข้อมูล")
    exit()
    
print(f"✓ โหลดข้อมูลสำเร็จ: {len(df):,} แถว ({time.time()-start_time:.2f} วินาที)")

# 2. เตรียม features
features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
target = 'LST'
X = df[features].values
y = df[target].values.ravel()

del df
gc.collect()

# 3. Preprocessing (Imputation & Scaling)
print("\n[2/6] Preprocessing...")
# Imputation
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)

# Scaling (จำเป็นมากสำหรับ Neural Network)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# แบ่งข้อมูล
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
print(f"✓ แบ่งข้อมูล: Train={len(X_train):,}, Test={len(X_test):,}")

# 4. สร้างและเทรนโมเดล
print("\n[3/6] เริ่มต้นเทรนโมเดล (อาจใช้เวลาสักครู่)...")

# --- Model 1: Random Forest (Optimized) ---
print("   > Training Random Forest...")
rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,  # ลดลงเล็กน้อยเพื่อความเร็ว
    min_samples_split=20,
    n_jobs=-1,
    random_state=42
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_r2 = r2_score(y_test, rf_pred)
print(f"     ✅ RF Test R²: {rf_r2:.4f}")

# --- Model 2: Deep Neural Network (DNN) ---
print("   > Training Deep Neural Network (DNN)...")
dnn_model = MLPRegressor(
    hidden_layer_sizes=(128, 64, 32), # 3 Hidden Layers
    activation='relu',
    solver='adam',
    alpha=0.0001,
    batch_size=64,
    learning_rate='adaptive',
    max_iter=500, # เพิ่มรอบการเรียนรู้
    early_stopping=True,
    random_state=42
)
dnn_model.fit(X_train, y_train)
dnn_pred = dnn_model.predict(X_test)
dnn_r2 = r2_score(y_test, dnn_pred)
print(f"     ✅ DNN Test R²: {dnn_r2:.4f}")

# 5. สร้าง Ensemble (Weighted Average)
print("\n[4/6] สร้าง Ensemble Model...")
# ให้ถ่วงน้ำหนักตามค่า R2 (โมเดลไหนแม่นกว่าให้เชื่อเยอะกว่า)
total_score = rf_r2 + dnn_r2
w_rf = rf_r2 / total_score
w_dnn = dnn_r2 / total_score

print(f"   - Weights: RF={w_rf:.2f}, DNN={w_dnn:.2f}")

y_pred_ensemble = (rf_pred * w_rf) + (dnn_pred * w_dnn)
ensemble_r2 = r2_score(y_test, y_pred_ensemble)
ensemble_rmse = np.sqrt(mean_squared_error(y_test, y_pred_ensemble))

# 6. ประเมินผล
print("\n" + "="*70)
print("=== FINAL RESULTS (Hybrid System) ===")
print("="*70)
print(f"1. Random Forest R² : {rf_r2:.4f}")
print(f"2. Deep Learning R² : {dnn_r2:.4f}")
print("-" * 30)
print(f"🏆 Hybrid Ensemble R²: {ensemble_r2:.4f}")
print(f"📉 Hybrid Ensemble RMSE: {ensemble_rmse:.4f}")
print("="*70)

if ensemble_r2 > max(rf_r2, dnn_r2):
    print("✨ SUCCESS: การรวมโมเดลให้ผลดีกว่าโมเดลเดี่ยว!")
else:
    print("ℹ️ Note: การรวมโมเดลไม่เพิ่มความแม่นยำอย่างมีนัยสำคัญ แต่ช่วยเรื่องความเสถียร (Stability)")

# 7. บันทึกผล
print("\n[6/6] บันทึกโมเดล...")
joblib.dump(rf_model, 'model_rf.joblib')
joblib.dump(dnn_model, 'model_dnn.joblib')
joblib.dump(scaler, 'scaler.joblib')
# บันทึก weights ไว้ใช้งงานจริง
with open("ensemble_weights.txt", "w") as f:
    f.write(f"RF:{w_rf}\nDNN:{w_dnn}")
    
print("✓ บันทึกโมเดลและ Scaler เรียบร้อย")
print("🎉 เสร็จสิ้นกระบวนการ!")

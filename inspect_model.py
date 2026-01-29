import joblib
import pandas as pd
import numpy as np

# โหลดโมเดล
print("Loading model...")
rf_model = joblib.load('model_rf.joblib')

# ชื่อ Features (ต้องเรียงให้ตรงกับตอนเทรน)
# features = ['CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation', 'month', 'year']
feature_names = ['Methane (CH4)', 'Nitrogen Dioxide (NO2)', 'Carbon Monoxide (CO)', 
                 'Vegetation Index (NDVI)', 'Albedo', 'Solar Radiation', 'Month', 'Year']

# ดึงค่าความสำคัญ
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1] # เรียงจากมากไปน้อย

print("\n" + "="*50)
print("🏆 FEATURE IMPORTANCE RANKING")
print("="*50)

results = []
for f in range(len(feature_names)):
    idx = indices[f]
    score = importances[idx]
    name = feature_names[idx]
    print(f"{f+1}. {name:<25} : {score:.4f} ({score*100:.2f}%)")
    results.append({'Feature': name, 'Importance': score})

print("="*50)

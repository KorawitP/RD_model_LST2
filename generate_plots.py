import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
import joblib

# ตั้งค่าฟอนต์และสไตล์
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'Tahoma' # หรือ sans-serif ถ้าไม่มี
plt.rcParams['figure.figsize'] = (10, 6)

# สร้างโฟลเดอร์เก็บกราฟ
output_dir = "outputs/plots"
os.makedirs(output_dir, exist_ok=True)

# 1. โหลดข้อมูลตัวอย่าง (sample) เพื่อความเร็ว
print("Loading data for plots...")
if os.path.exists('data/df_final_processed.parquet'):
    df = pd.read_parquet('data/df_final_processed.parquet')
    df_sample = df.sample(n=10000, random_state=42) # สุ่มมา 10,000 จุดพอ
else:
    print("❌ Data not found!")
    exit()

# 2. Correlation Heatmap
print("Generating Correlation Matrix...")
features = ['LST', 'CH4', 'NO2', 'CO', 'NDVI', 'Albedo', 'Solar_Radiation']
corr = df_sample[features].corr()

plt.figure(figsize=(10, 8))
heatmap = sns.heatmap(corr, annot=True, cmap='RdBu_r', fmt=".2f", vmin=-1, vmax=1)
plt.title('Correlation Matrix of Variables', fontsize=16)
plt.tight_layout()
plt.savefig(f"{output_dir}/correlation_matrix.png", dpi=300)
print(f"✓ Saved {output_dir}/correlation_matrix.png")
plt.close()

# 3. Feature Importance Bar Chart
print("Generating Feature Importance Plot...")
# ค่าจาก output ก่อนหน้านี้
importance_data = {
    'Feature': ['Solar Radiation', 'Albedo', 'Month', 'NDVI', 'CO', 'NO2', 'Year', 'CH4'],
    'Importance': [0.2870, 0.1838, 0.1669, 0.1158, 0.1034, 0.0735, 0.0511, 0.0186]
}
df_imp = pd.DataFrame(importance_data)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance', y='Feature', data=df_imp, hue='Feature', palette='viridis', legend=False)
plt.title('Feature Importance (Random Forest)', fontsize=16)
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig(f"{output_dir}/feature_importance.png", dpi=300)
print(f"✓ Saved {output_dir}/feature_importance.png")
plt.close()

# 4. Scatter Plot: CO vs LST (แสดงความสัมพันธ์)
print("Generating Scatter Plot CO vs LST...")
# Clean data for plotting (remove NaNs and Infs)
plot_data = df_sample[['CO', 'LST']].replace([np.inf, -np.inf], np.nan).dropna()

plt.figure(figsize=(8, 6))
# Use regplot for scatter + trendline (more robust than polyfit)
sns.regplot(x='CO', y='LST', data=plot_data, 
            scatter_kws={'alpha':0.3, 'color':'orange'}, 
            line_kws={'color':'red', 'linewidth':2})

plt.title('Relationship between CO and LST', fontsize=14)
plt.xlabel('Carbon Monoxide (CO)')
plt.ylabel('Land Surface Temperature (LST)')
plt.tight_layout()
plt.savefig(f"{output_dir}/scatter_co_lst.png", dpi=300)
print(f"✓ Saved {output_dir}/scatter_co_lst.png")
plt.close()

print("🎉 All plots generated successfully!")

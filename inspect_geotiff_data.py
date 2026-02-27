import os
import numpy as np
import rasterio
import pandas as pd

# Files to inspect
files = [
    r"data/LST_Mean_Final.tif",
    r"data/LST_Mean_Result.tif",
    r"data/Monthly_Albedo_2018-2025.tif",
    r"data/Monthly_CH4_2018-2025.tif",
    r"data/Monthly_CO_2018-2025.tif",
    r"data/Monthly_LST_Filled_2018-2025.tif",
    r"data/Monthly_NDVI_2018-2025.tif",
    r"data/Monthly_NO2_2018-2025.tif",
    r"data/Monthly_Solar_Radiation_2018-2025.tif",
    r"data/NO2_Mean_Final.tif",
    r"data/CO_Mean_Final.tif"
]

base_dir = r"d:\python\RD_model_LST2"

print("="*60)
print("REPORT: GeoTIFF Data Inspection / รายงานตรวจสอบข้อมูล GeoTIFF")
print("="*60)

for rel_path in files:
    file_path = os.path.join(base_dir, rel_path)
    print(f"\n📂 File: {rel_path}")
    
    if not os.path.exists(file_path):
        print(f"   ❌ File not found at: {file_path}")
        continue

    try:
        with rasterio.open(file_path) as src:
            print(f"   📐 Dimensions (WxH): {src.width} x {src.height}")
            print(f"   🔢 Bands: {src.count}")
            print(f"   🌐 CRS: {src.crs}")
            print(f"   🎲 Data Type: {src.dtypes[0]}")
            print(f"   🚫 NoData Value: {src.nodatavals[0]}")

            # Read the first band
            data = src.read(1)
            
            # Mask nodata if present
            if src.nodatavals[0] is not None:
                masked_data = np.ma.masked_equal(data, src.nodatavals[0])
            else:
                masked_data = data

            # Basic Statistics
            d_min = np.nanmin(masked_data)
            d_max = np.nanmax(masked_data)
            d_mean = np.nanmean(masked_data)
            d_std = np.nanstd(masked_data)
            
            print(f"   📊 Statistics (Band 1):")
            print(f"      Min: {d_min:.4f}")
            print(f"      Max: {d_max:.4f}")
            print(f"      Mean: {d_mean:.4f}")
            print(f"      Std Dev: {d_std:.4f}")

            # Show a sample "Table" (Central 5x5 window)
            cy, cx = src.height // 2, src.width // 2
            window_size = 5
            
            # Ensure window is within bounds
            start_y = max(0, cy - window_size // 2)
            end_y = min(src.height, start_y + window_size)
            start_x = max(0, cx - window_size // 2)
            end_x = min(src.width, start_x + window_size)
            
            sample = data[start_y:end_y, start_x:end_x]
            
            print(f"   🔎 Sample Data Table (Center 5x5 at [{start_y}:{end_y}, {start_x}:{end_x}]):")
            df = pd.DataFrame(sample)
            print(df.to_string(index=False, header=False))
            
    except Exception as e:
        print(f"   ❌ Error reading file: {e}")
        # Constructive error handling suggestions
        if "rasterio" in str(e):
             print("      (Tip: Ensure 'rasterio' library is installed)")

print("\n" + "="*60)

# แสดงภาพจากไฟล์ .tif ด้วย Python
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

print("="*70)
print("=== แสดงภาพจากไฟล์ GeoTIFF ===")
print("="*70)

# 1. เลือกไฟล์
data_folder = 'data'
tif_files = [f for f in os.listdir(data_folder) if f.endswith('.tif')]

print(f"\nพบไฟล์ .tif ทั้งหมด {len(tif_files)} ไฟล์:")
for i, f in enumerate(tif_files, 1):
    print(f"  {i}. {f}")

# เลือกไฟล์ที่ต้องการแสดง
file_index = 4  # Monthly_LST_Filled_2018-2025.tif
selected_file = tif_files[file_index - 1]
file_path = os.path.join(data_folder, selected_file)

print(f"\n📂 เลือกไฟล์: {selected_file}")

# 2. เปิดไฟล์และอ่านข้อมูล
print("\n[1/3] กำลังโหลดข้อมูล...")
with rasterio.open(file_path) as src:
    print(f"✓ เปิดไฟล์สำเร็จ")
    print(f"  ขนาด: {src.width} x {src.height} pixels")
    print(f"  จำนวน bands: {src.count}")
    print(f"  CRS: {src.crs}")
    print(f"  Bounds: {src.bounds}")
    
    # เลือก bands ที่จะแสดง (เดือนต่างๆ)
    bands_to_show = [1, 25, 49, 73]  # มกราคม 2018, มกราคม 2020, มกราคม 2022, มกราคม 2024
    
    print(f"\n[2/3] กำลังอ่านข้อมูล {len(bands_to_show)} bands...")
    
    # สร้างรูปภาพ
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    # กำหนดชื่อเดือน
    months = ['2018-01', '2020-01', '2022-01', '2024-01']
    
    for idx, (band_num, month_name) in enumerate(zip(bands_to_show, months)):
        print(f"  กำลังประมวลผล Band {band_num} ({month_name})...")
        
        # อ่านข้อมูล band
        data = src.read(band_num)
        
        # แทนที่ค่า NoData ด้วย NaN
        data = data.astype(float)
        if src.nodata is not None:
            data[data == src.nodata] = np.nan
        
        # คำนวณสถิติ
        valid_data = data[~np.isnan(data)]
        if len(valid_data) > 0:
            vmin = np.percentile(valid_data, 2)
            vmax = np.percentile(valid_data, 98)
            mean_val = np.mean(valid_data)
            
            print(f"    Min: {vmin:.2f}, Max: {vmax:.2f}, Mean: {mean_val:.2f}")
        else:
            vmin, vmax = 0, 1
        
        # แสดงภาพ
        ax = axes[idx]
        
        # เลือก colormap ตามชื่อไฟล์
        if 'LST' in selected_file:
            cmap = 'RdYlBu_r'  # แดง = ร้อน, น้ำเงิน = เย็น
            label = 'LST (°C)'
        elif 'NDVI' in selected_file:
            cmap = 'RdYlGn'  # แดง = ไม่มีพืช, เขียว = มีพืช
            label = 'NDVI'
        elif 'Albedo' in selected_file:
            cmap = 'gray'
            label = 'Albedo'
        else:
            cmap = 'viridis'
            label = 'Value'
        
        im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, aspect='auto')
        ax.set_title(f'{month_name}\nMean: {mean_val:.2f}' if len(valid_data) > 0 else month_name, 
                     fontsize=14, fontweight='bold')
        ax.axis('off')
        
        # เพิ่ม colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(label, fontsize=10)
    
    # ตั้งชื่อรูปภาพ
    plt.suptitle(f'{selected_file}\nเปรียบเทียบข้อมูลในช่วงเวลาต่างๆ', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    # บันทึกรูปภาพ
    output_file = f'outputs/plots/visualization_{selected_file.replace(".tif", "")}.png'
    print(f"\n[3/3] กำลังบันทึกรูปภาพ...")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ บันทึกรูปภาพที่: {output_file}")
    
    # แสดงรูปภาพ
    print("\n💡 กำลังแสดงรูปภาพ... (ปิดหน้าต่างเพื่อดำเนินการต่อ)")
    plt.show()

print("\n" + "="*70)
print("=== เสร็จสิ้น ===")
print("="*70)
print(f"\n📊 รูปภาพถูกบันทึกที่: {output_file}")
print("\n💡 คุณสามารถ:")
print("  1. เปิดไฟล์รูปภาพที่บันทึกไว้")
print("  2. แก้ไขโค้ดเพื่อเลือก bands อื่นๆ")
print("  3. ใช้ QGIS สำหรับการวิเคราะห์เชิงลึก (ดูคู่มือใน คู่มือเปิดไฟล์ใน_QGIS.md)")

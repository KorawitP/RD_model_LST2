# แสดงภาพจากไฟล์ .tif ด้วย Interpolation (ทำให้เรียบขึ้น)
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import os

print("="*70)
print("=== แสดงภาพแบบเรียบ (Smooth) จากไฟล์ GeoTIFF ===")
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
    print(f"  ความละเอียด: ~1 km/pixel")
    print(f"  จำนวน bands: {src.count}")
    
    # เลือก band ที่จะแสดง
    band_num = 1  # มกราคม 2018
    
    print(f"\n[2/3] กำลังอ่านข้อมูล Band {band_num}...")
    
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
        print(f"  Min: {vmin:.2f}, Max: {vmax:.2f}, Mean: {mean_val:.2f}")
    else:
        vmin, vmax = 0, 1
    
    # สร้างรูปภาพเปรียบเทียบ
    print(f"\n[3/3] กำลังสร้างภาพเปรียบเทียบ...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    
    # เลือก colormap
    if 'LST' in selected_file:
        cmap = 'RdYlBu_r'
        label = 'LST (Kelvin)'
    elif 'NDVI' in selected_file:
        cmap = 'RdYlGn'
        label = 'NDVI'
    else:
        cmap = 'viridis'
        label = 'Value'
    
    # ตัวเลือก interpolation
    interpolations = [
        ('nearest', 'ไม่มี Interpolation\n(เห็นเป็นก้อนๆ)'),
        ('bilinear', 'Bilinear Interpolation\n(เรียบขึ้นเล็กน้อย)'),
        ('bicubic', 'Bicubic Interpolation\n(เรียบมาก)'),
        ('lanczos', 'Lanczos Interpolation\n(คุณภาพดีที่สุด)')
    ]
    
    for idx, (interp_method, title) in enumerate(interpolations):
        ax = axes[idx // 2, idx % 2]
        
        # แสดงภาพ
        im = ax.imshow(data, 
                      cmap=cmap, 
                      vmin=vmin, 
                      vmax=vmax, 
                      aspect='auto',
                      interpolation=interp_method)  # ← สำคัญ!
        
        ax.set_title(title, fontsize=14, fontweight='bold', pad=10)
        ax.axis('off')
        
        # เพิ่ม colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label(label, fontsize=10)
        
        # เพิ่มข้อความอธิบาย
        if idx == 0:
            ax.text(0.02, 0.98, 'Original\n(Pixelated)', 
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        elif idx == 3:
            ax.text(0.02, 0.98, 'Best Quality\n(Recommended)', 
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    # ตั้งชื่อรูปภาพ
    plt.suptitle(f'Comparison: Interpolation Methods\n{selected_file} - Band {band_num}', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    # บันทึกรูปภาพ
    output_file = f'visualization_smooth_{selected_file.replace(".tif", "")}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ บันทึกรูปภาพที่: {output_file}")
    
    # แสดงรูปภาพ
    print("\nกำลังแสดงรูปภาพ... (ปิดหน้าต่างเพื่อดำเนินการต่อ)")
    plt.show()

print("\n" + "="*70)
print("=== เสร็จสิ้น ===")
print("="*70)
print(f"\n📊 รูปภาพถูกบันทึกที่: {output_file}")
print("\n💡 สังเกต:")
print("  - ภาพซ้ายบน (nearest): เห็นเป็นก้อนๆ ชัดเจน")
print("  - ภาพขวาล่าง (lanczos): เรียบที่สุด แต่ยังคงความละเอียดเดิม")
print("\n⚠️ หมายเหตุ:")
print("  Interpolation ทำให้ภาพดูเรียบขึ้น แต่ไม่ได้เพิ่มข้อมูลจริง!")
print("  ถ้าต้องการละเอียดจริงๆ ต้อง export ใหม่ด้วย scale ต่ำกว่า")
print("  (ดูรายละเอียดใน ทำไมภาพไม่ละเอียด.md)")

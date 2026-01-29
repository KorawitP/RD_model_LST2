# ตรวจสอบข้อมูลตำแหน่งในไฟล์ .tif
import os

print("="*70)
print("=== ตรวจสอบข้อมูลตำแหน่งในไฟล์ GeoTIFF ===")
print("="*70)

# ตรวจสอบไฟล์ที่มี
data_folder = 'data'
tif_files = [f for f in os.listdir(data_folder) if f.endswith('.tif')]

print(f"\nพบไฟล์ .tif ทั้งหมด {len(tif_files)} ไฟล์:")
for i, f in enumerate(tif_files, 1):
    print(f"  {i}. {f}")

# ลองใช้ library ต่างๆ
print("\n" + "="*70)
print("=== ตรวจสอบ Library ที่ใช้อ่านข้อมูล Geospatial ===")
print("="*70)

libraries = []

# ตรวจสอบ rasterio
try:
    import rasterio
    libraries.append(('rasterio', rasterio.__version__))
    print("✓ rasterio: ติดตั้งแล้ว (version", rasterio.__version__, ")")
except ImportError:
    print("✗ rasterio: ยังไม่ได้ติดตั้ง")

# ตรวจสอบ GDAL
try:
    from osgeo import gdal
    libraries.append(('gdal', gdal.__version__))
    print("✓ GDAL: ติดตั้งแล้ว (version", gdal.__version__, ")")
except ImportError:
    print("✗ GDAL: ยังไม่ได้ติดตั้ง")

# ตรวจสอบ xarray
try:
    import xarray as xr
    libraries.append(('xarray', xr.__version__))
    print("✓ xarray: ติดตั้งแล้ว (version", xr.__version__, ")")
except ImportError:
    print("✗ xarray: ยังไม่ได้ติดตั้ง")

# ถ้ามี library ให้ลองอ่านไฟล์
if libraries:
    print("\n" + "="*70)
    print("=== ตรวจสอบข้อมูลตำแหน่งจากไฟล์ตัวอย่าง ===")
    print("="*70)
    
    test_file = os.path.join(data_folder, tif_files[0])
    print(f"\nไฟล์ทดสอบ: {tif_files[0]}")
    
    # ลองใช้ rasterio
    if any(lib[0] == 'rasterio' for lib in libraries):
        print("\n--- ใช้ rasterio ---")
        try:
            import rasterio
            with rasterio.open(test_file) as src:
                print(f"✓ เปิดไฟล์สำเร็จ")
                print(f"  ขนาด: {src.width} x {src.height} pixels")
                print(f"  จำนวน bands: {src.count}")
                print(f"  CRS (Coordinate Reference System): {src.crs}")
                print(f"  Bounds (ขอบเขต):")
                print(f"    - Left (ซ้าย): {src.bounds.left:.4f}")
                print(f"    - Right (ขวา): {src.bounds.right:.4f}")
                print(f"    - Top (บน): {src.bounds.top:.4f}")
                print(f"    - Bottom (ล่าง): {src.bounds.bottom:.4f}")
                print(f"  Transform (การแปลงพิกัด):")
                print(f"    {src.transform}")
                
                # ตรวจสอบว่ามีข้อมูลตำแหน่งหรือไม่
                if src.crs is not None:
                    print("\n✓ ไฟล์นี้มีข้อมูลตำแหน่ง (Georeferenced)")
                    print(f"  ระบบพิกัด: {src.crs}")
                else:
                    print("\n✗ ไฟล์นี้ไม่มีข้อมูลตำแหน่ง")
        except Exception as e:
            print(f"✗ เกิดข้อผิดพลาด: {e}")
    
    # ลองใช้ GDAL
    elif any(lib[0] == 'gdal' for lib in libraries):
        print("\n--- ใช้ GDAL ---")
        try:
            from osgeo import gdal
            ds = gdal.Open(test_file)
            if ds:
                print(f"✓ เปิดไฟล์สำเร็จ")
                print(f"  ขนาด: {ds.RasterXSize} x {ds.RasterYSize} pixels")
                print(f"  จำนวน bands: {ds.RasterCount}")
                
                # ข้อมูล GeoTransform
                geo = ds.GetGeoTransform()
                if geo:
                    print(f"  GeoTransform:")
                    print(f"    - Origin (top-left): ({geo[0]:.4f}, {geo[3]:.4f})")
                    print(f"    - Pixel size: {geo[1]:.6f} x {geo[5]:.6f}")
                
                # ข้อมูล Projection
                proj = ds.GetProjection()
                if proj:
                    print(f"  Projection: {proj[:100]}...")
                    print("\n✓ ไฟล์นี้มีข้อมูลตำแหน่ง (Georeferenced)")
                else:
                    print("\n✗ ไฟล์นี้ไม่มีข้อมูลตำแหน่ง")
                
                ds = None
        except Exception as e:
            print(f"✗ เกิดข้อผิดพลาด: {e}")
else:
    print("\n" + "="*70)
    print("⚠ ไม่พบ library สำหรับอ่านข้อมูล Geospatial")
    print("="*70)
    print("\n💡 แนะนำให้ติดตั้ง:")
    print("  pip install rasterio")
    print("  หรือ")
    print("  pip install gdal")

print("\n" + "="*70)
print("=== สรุป ===")
print("="*70)
print("\nไฟล์ .tif ที่ export จาก Google Earth Engine จะมีข้อมูลตำแหน่ง")
print("ประกอบด้วย:")
print("  1. CRS (Coordinate Reference System) - ระบบพิกัด เช่น EPSG:4326")
print("  2. GeoTransform - การแปลงจาก pixel เป็นพิกัดจริง")
print("  3. Bounds - ขอบเขตพื้นที่ (latitude/longitude)")
print("\nข้อมูลเหล่านี้ช่วยให้:")
print("  - รู้ว่าแต่ละ pixel อยู่ที่ตำแหน่งใดบนโลก")
print("  - สามารถนำไปทำ spatial analysis ได้")
print("  - แสดงผลบนแผนที่ได้ถูกต้อง")

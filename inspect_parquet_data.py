import pandas as pd

file_path = r"d:\python\RD_model_LST2\data\df_final_processed.parquet"

try:
    df = pd.read_parquet(file_path)
    print("="*60)
    print("REPORT: Parquet Data Inspection / รายงานตรวจสอบข้อมูล Parquet")
    print("="*60)
    print(f"📂 File: {file_path}")
    print(f"   📐 Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"   📋 Columns: {list(df.columns)}")
    print("\n   🔎 Sample Data (First 5 rows):")
    print(df.head().to_string())
    print("\n   📊 Data Types:")
    print(df.dtypes)
    
except Exception as e:
    print(f"Error reading parquet file: {e}")

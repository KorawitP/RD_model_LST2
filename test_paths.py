import os
import pandas as pd
import joblib

def check_paths():
    print("=== Verification Script ===")
    
    # 1. Check Data
    data_path = 'data/df_final_processed.parquet'
    if os.path.exists(data_path):
        print(f"✅ Data file found at: {data_path}")
    else:
        print(f"❌ Data file NOT found at: {data_path}")
        return

    # 2. Check Models directory
    if os.path.exists('models'):
        print("✅ Models directory exists.")
        models = [f for f in os.listdir('models') if f.endswith('.joblib')]
        if models:
            print(f"✅ Found {len(models)} models: {models}")
        else:
            print("❌ No models found in models directory!")
    else:
        print("❌ Models directory NOT found.")

    # 3. Simulate Load
    print("\nAttempting to load data (Dry Run)...")
    try:
        # Read only a few rows to be fast
        df = pd.read_parquet(data_path, columns=['LST']) 
        print(f"✅ Can load data successfully. Rows: {len(df)}")
    except Exception as e:
        print(f"❌ Failed to load data: {e}")

    print("\nAttempting to load a model (Dry Run)...")
    try:
        model_path = 'models/random_forest_model_final.joblib'
        if os.path.exists(model_path):
            # Load with mmap_mode to be fast and not consume much ram
            model = joblib.load(model_path, mmap_mode='r')
            print(f"✅ Can load model successfully: {model_path}")
        else:
             print(f"⚠️ Model file {model_path} not found to test load.")
             
    except Exception as e:
        print(f"❌ Failed to load model: {e}")

if __name__ == "__main__":
    check_paths()

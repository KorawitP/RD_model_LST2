"""
สคริปต์รวมไฟล์ Markdown และแปลงเป็น Word
พร้อมฟอนต์ TH Sarabun และจัดรูปแบบเอกสารวิจัย
"""

import os
import re
from pathlib import Path

# กำหนด path
BASE_DIR = Path(r"D:\python\RD_model_LST2\final_docs")
OUTPUT_FILE = BASE_DIR / "thesis_combined.md"

# ลำดับไฟล์ที่ต้องรวม
FILES_TO_COMBINE = [
    ("chapter_1", "chapter_1.md"),
    ("chapter_2", "chapter_2_combined.md"),
    ("chapter_3", "chapter_3_combined.md"),
    ("chapter_4", "chapter_4_combined.md"),
    ("chapter_5", "chapter_5.md"),
    (None, "references.md"),
]

def fix_image_paths(content: str, chapter_dir: str) -> str:
    """แก้ไข path รูปภาพให้เป็น relative path ที่ถูกต้อง"""
    # แก้ไข path รูปภาพ
    content = re.sub(
        r'!\[(.*?)\]\(\.\./images/',
        r'![\\1](images/',
        content
    )
    content = re.sub(
        r'!\[(.*?)\]\(images/',
        r'![\\1](images/',
        content
    )
    return content

def add_page_break() -> str:
    """เพิ่มการขึ้นหน้าใหม่"""
    return "\n\n\\newpage\n\n"

def main():
    print("=" * 60)
    print("📚 กำลังรวมไฟล์วิทยานิพนธ์...")
    print("=" * 60)
    
    # Header ของเอกสาร
    combined_content = """---
title: "การประยุกต์ใช้การเรียนรู้ของเครื่องและปัญญาประดิษฐ์ที่อธิบายได้เพื่อวิเคราะห์ความสัมพันธ์ระหว่างก๊าซเรือนกระจกกับอุณหภูมิพื้นผิวดินในประเทศไทย"
subtitle: "Application of Machine Learning and Explainable AI for Analyzing the Relationship between Greenhouse Gases and Land Surface Temperature in Thailand"
author: ""
date: "พ.ศ. 2568"
lang: th
documentclass: article
geometry: 
  - top=2.5cm
  - bottom=2.5cm
  - left=3cm
  - right=2.5cm
fontsize: 16pt
linestretch: 1.5
---

"""
    
    for chapter_dir, filename in FILES_TO_COMBINE:
        if chapter_dir:
            filepath = BASE_DIR / chapter_dir / filename
        else:
            filepath = BASE_DIR / filename
            
        if filepath.exists():
            print(f"✅ กำลังเพิ่ม: {filepath.name}")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # แก้ไข path รูปภาพ
            content = fix_image_paths(content, chapter_dir or "")
            
            # เพิ่มเนื้อหา
            combined_content += content
            combined_content += add_page_break()
        else:
            print(f"❌ ไม่พบไฟล์: {filepath}")
    
    # บันทึกไฟล์รวม
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(combined_content)
    
    print("=" * 60)
    print(f"✅ บันทึกไฟล์รวมที่: {OUTPUT_FILE}")
    print(f"📊 ขนาดไฟล์: {OUTPUT_FILE.stat().st_size / 1024:.1f} KB")
    print("=" * 60)

if __name__ == "__main__":
    main()

# To-Do List: การปรับปรุงและเรียบเรียงบทที่ 2 (Literature Review)

**เป้าหมาย:** สร้างไฟล์บทที่ 2 ฉบับสมบูรณ์ โดยการผสานจุดเด่นของ "ไฟล์หลัก" (ภาษาที่เป็นวิชาการ) และ "ไฟล์ร่าง" (เนื้อหาเชิงเทคนิค Gap Filling และ XAI)

## 1. โครงสร้างเนื้อหาใหม่ (New Structure Outline)

### 2.1 แนวคิดและทฤษฎีพื้นฐาน (Conceptual Framework)

- [x] **ความสัมพันธ์ระหว่างก๊าซเรือนกระจกและอุณหภูมิพื้นผิว**: อธิบายกลไก Greenhouse Effect และ Radiative Forcing
- [x] **ทฤษฎีการดูดกลืนรังสี**: เจาะจงคุณสมบัติของ CH₄, NO₂, CO ในช่วงคลื่นอินฟราเรด
- [x] **สมดุลพลังงานพื้นผิว (Surface Energy Balance)**: ความสัมพันธ์ระหว่าง รังสีดวงอาทิตย์, Albedo, และการถ่ายเทความร้อน

### 2.2 การตรวจวัดอุณหภูมิพื้นผิวโลกด้วยดาวเทียม (Satellite-based LST Retrieval)

- [x] **เทคโนโลยีสำรวจระยะไกล**: รายละเอียดของ MODIS, Landsat (TIRS), Sentinel-3 (SLSTR)
- [x] **การเปรียบเทียบ Spatiotemporal Resolution**: ตารางเปรียบเทียบข้อดี-ข้อเสียของแต่ละดาวเทียม
- [x] **ปัญหาและเทคนิคการจัดการข้อมูล (Crucial Update)**:
  - [x] ปัญหาเมฆ (Cloud Contamination) ในภูมิภาคเขตร้อน
  - [x] **เทคนิค Gap Filling**: ดึงเนื้อหาเชิงลึกจากไฟล์ร่าง (RF, Deep Learning, HANTS) มาขยายความ
  - [x] **Data Fusion**: การผสมผสานข้อมูลหลายแหล่งเพื่อลดข้อจำกัด

### 2.3 การตรวจวัดก๊าซเรือนกระจกด้วยดาวเทียม (Satellite-based GHG Monitoring)

- [x] **Sentinel-5P TROPOMI**: หลักการทำงาน (Spectrometer), ย่านความถี่ที่ใช้วัด GHGs, และความแม่นยำ (Validation)
- [x] **บริบทก๊าซเรือนกระจกในประเทศไทย (Thailand Context)**:
  - [x] **CH₄**: การปล่อยจากนาข้าวและการจัดการน้ำ (AWD)
  - [x] **NO₂**: ผลกระทบจากภาคขนส่งและอุตสาหกรรมในเขตเมือง
  - [x] **CO**: ปัญหาการเผาชีวมวลและ PM2.5 ในภาคเหนือ

### 2.4 Machine Learning และ Deep Learning สำหรับการวิเคราะห์สภาพภูมิอากาศ

- [ ] **Traditional ML**: Random Forest (RF), Gradient Boosting (XGBoost, CatBoost)
- [ ] **Deep Learning**: LSTM, BiLSTM (สำหรับ Time-series), CNN-LSTM (สำหรับ Spatiotemporal), Transformers
- [ ] **Ensemble Learning**: เทคนิค Stacking และ Blending เพื่อเพิ่มความแม่นยำ

### 2.5 Explainable AI (XAI) **(หัวข้อใหม่ - ต้องเพิ่ม)**

_หมายเหตุ: หัวข้อนี้ขาดหายไปในไฟล์หลัก แต่มีความสำคัญมากต่องานวิจัยนี้_

- [ ] **ความจำเป็นของ XAI**: การแกะกล่องดำ (Black-box) ของโมเดล AI ในงานวิทยาศาสตร์
- [ ] **SHAP (SHapley Additive exPlanations)**: ทฤษฎีและการแปลผล (Global vs Local interpretation)
- [ ] **Permutation Feature Importance**: การวัดความสำคัญของตัวแปร (GHGs vs LST)

### 2.6 งานวิจัยที่เกี่ยวข้องและช่องว่างทางวิชาการ (Related Research & Research Gaps)

- [ ] **งานวิจัยในเอเชียตะวันออกเฉียงใต้**: สรุปงานที่ศึกษา LST และ GHGs ในบริบทใกล้เคียง
- [ ] **สรุป Research Gap (ปรับปรุงใหม่)**:
  - [ ] เน้นการขาดการวิเคราะห์ "ความสัมพันธ์เชิงพื้นที่" โดยตรง (Concentration vs LST)
  - [ ] เน้นการขาดการประยุกต์ใช้ "XAI" เพื่ออธิบายปรากฏการณ์ในบริบทไทย

---

## 2. ขั้นตอนการดำเนินการ (Action Plan)

1.  [x] **สร้างไฟล์ `final_docs/chapter_2/chapter_2_combined.md`**
2.  [x] **Migration 1 (Base Content)**: ย้ายเนื้อหา 2.1, 2.3 จากไฟล์หลัก (หรือเขียนใหม่) เสร็จสิ้น
3.  [x] **Migration 2 (Enhancement)**: แทรกเนื้อหา Gap Filling และรายละเอียด GHG บริบทไทยแล้ว
4.  [ ] **Migration 3 (New Logic)**: เขียนหัวข้อ 2.4 (ML/DL) และ 2.5 (XAI) ใหม่
5.  [ ] **Final Polish**: ปรับปรุงบทสรุป Research Gap และตรวจสอบ Citation ให้อยู่ในฟอร์แมตเดียวกัน

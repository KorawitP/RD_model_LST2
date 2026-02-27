# อ้างอิงงานวิจัยสนับสนุนการนำตัวแปรที่มีค่าความแปรปรวนเป็นศูนย์ออก (Zero-Variance Feature Removal / Variance Thresholding Justification)

## 1. ประเด็นเรื่อง: Zero-Variance Features ไม่ให้ข้อมูลใหม่แก่โมเดล (Lack of Discriminative Power)

ในทางสถิติและ Machine Learning ตัวแปรที่มีค่าเพียงค่าเดียวตลอดทั้งชุดข้อมูล (Zero-variance) หรือมีค่าเกือบจะเป็นค่าเดียวทั้งหมด (Near-zero variance) จะไม่มีประโยชน์ในการแยกแยะความแตกต่างระหว่างตัวอย่าง (Samples) การคงตัวแปรเหล่านี้ไว้ไม่เพียงแต่ไม่เพิ่มความแม่นยำ แต่ยังอาจทำให้โมเดลเกิดความสับสนหรือมีอคติได้

**อ้างอิงที่แนะนำ:**

- **Kuhn, M., & Johnson, K. (2013).** _Applied predictive modeling_ (Vol. 26). New York: Springer. [[DOI: 10.1007/978-1-4614-6849-3]](https://doi.org/10.1007/978-1-4614-6849-3)
  - _(หนังสือเล่มนี้เป็นตำราระดับคริสเตียนของ Machine Learning อธิบายอย่างชัดเจนในบท Data Pre-processing ว่าตัวแปรประเภท Zero-variance และ Near-zero variance predictors ถือเป็น "Uninformative features" ที่ควรถูกกำจัดออกก่อนกระบวนการฝึกสอนโมเดล)_
- **Guyon, I., & Elisseeff, A. (2003).** An introduction to variable and feature selection. _Journal of machine learning research_, 3(Mar), 1157-1182. [[URL]](https://jmlr.org/papers/v3/guyon03a.html)
  - _(งานวิจัยคลาสสิกด้าน Feature Selection ระบุข้อกำหนดพื้นฐานของการคัดเลือกตัวแปร ว่าตัวแปรที่ดีต้องมีความแปรปรวน (Variance) มากพอที่จะอธิบายความแตกต่างของ Target Variable ได้ การตัดตัวแปรที่ค่าคงที่ออกจึงเป็นขั้นตอนพื้นฐาน)_

## 2. ประเด็นเรื่อง: ทฤษฎี Variance Thresholding ในฐานะกระบวนการมาตรฐานเชิงปฏิบัติ

การคัดกรองด้วยค่าความแปรปรวน (Variance Thresholding) เป็นขั้นตอนทำความสะอาดข้อมูล (Data Cleaning) ที่ถูกฝังเป็นค่าเริ่มต้น (Default Step) ในไลบรารีวิเคราะห์ข้อมูลยอดนิยมหลายตัว เช่น Scikit-Learn ของ Python

**อ้างอิงที่แนะนำ:**

- **Pedregosa, F., et al. (2011).** Scikit-learn: Machine learning in Python. _Journal of machine learning research_, 12(Oct), 2825-2830. [[URL]](https://jmlr.csail.mit.edu/papers/v12/pedregosa11a.html)
  - _(สามารถอ้างอิง Framework ของ Scikit-Learn ได้โดยตรง ว่าขั้นตอน VarianceThreshold ถูกออกแบบมาเพื่อตรวจสอบและกำจัดคุณลักษณะที่มีค่าความแปรปรวนเป็น 0 (Constant features) ออกโดยอัตโนมัติ เนื่องจากถือว่าเป็นสัญญาณรบกวน (Noise) เชิงโครงสร้างที่ไร้ประโยชน์ต่อรูปแบบสมการใดๆ)_
- **Kirasich, K., Smith, T., & Sadler, B. (2018).** Random forest vs logistic regression: binary classification for heterogeneous datasets. _SMU Data Science Review_, 1(3), 9. [[URL]](https://scholar.smu.edu/datasciencereview/vol1/iss3/9)
  - _(มีการกล่าวถึงการทำ Data Preprocessing ก่อนเข้าสู่โมเดล Random Forest รวมถึงการตรวจสอบการกระจายตัวและการกำจัดตัวแปรที่ไม่มีนัยสำคัญเชิงสถิติ หรือไม่มีความแปรปรวน)_

## 3. ประเด็นที่เกี่ยวข้องกับข้อมูลเชิงพื้นที่โดยตรง (LULC & DEM)

บ่อยครั้งในการสุ่มตัวอย่างเชิงพื้นที่ (Spatial Sampling) หากขนาดตัวอย่างไม่ใหญ่ครอบคลุมภูมิประเทศที่แตกต่างกันมากพอ อาจเกิดกรณีที่ตัวอย่างไปกระจุกในพื้นที่ราบที่มีความสูงเชิงระดับน้ำทะเล (DEM) ติดกัน หรือบนพื้นที่ที่มีการใช้ประโยชน์ที่ดิน (LULC) ประเภทเดียวกันหมด ทำให้ข้อมูลในชุดฝึกสอน (Training set) นั้นมีความแปรปรวนของภูมิประเทศเป็น 0

**อ้างอิงที่แนะนำ:**

- **Cai, L., & Gao, Y. (2024).** Application of Machine Learning Algorithms in Remote Sensing Water Quality Retrieval: A Comprehensive Review. _Water_, 16(5), 754. [[DOI: 10.3390/w16050754]](https://doi.org/10.3390/w16050754)
  - _(แม้จะเป็นเรื่องคุณภาพน้ำ แต่เปเปอร์นี้พูดถึงความสำคัญของ Data preprocessing และ Feature evaluation ในข้อมูล Remote Sensing ว่าสิ่งที่ต้องระวังคือ Feature ที่ซ้ำซ้อนและไร้การเปลี่ยนแปลงจากกระบวนการสุ่มตัวอย่างในพื้นที่ขนาดใหญ่)_

---

**สรุปการอ้างอิงในวิทยานิพนธ์ (ตัวอย่างการเขียน):**

"ในขั้นตอนการสกัดลักษณ์และคัดเลือกตัวแปร (Feature Selection) ผู้วิจัยได้ทำการตรวจสอบความแปรปรวน (Variance Thresholding) ของข้อมูลนำเข้า พบว่าในชุดข้อมูลภาพถ่ายดาวเทียมที่สุ่มตัวอย่างมานั้น ตัวแปรประเภทการใช้ประโยชน์ที่ดิน (LULC) และความสูงของภูมิประเทศ (DEM) มีค่าความแปรปรวนเป็นศูนย์ (Zero-variance) กล่าวคือมีค่าเป็นค่าคงที่ค่าเดียวทั้งหมด (Constant features) ในทางวิทยาการข้อมูลเชิงทำนาย (Predictive Data Science) ข้อมูลลักษณะนี้ถือเป็นข้อมูลที่ไม่มีนัยสำคัญ (Uninformative features) และไม่สามารถสร้างอำนาจจำแนก (Discriminative power) ให้แก่อัลกอริทึมได้ การคงตัวแปรเหล่านี้ไว้ไม่เพียงแต่ไม่ก่อให้เกิดประโยชน์ต่อการสร้างรูปแบบความสัมพันธ์ แต่ยับอาจลดทอนประสิทธิภาพและเพิ่มภาระในการประมวลผล (Computational cost) โดยไม่จำเป็น ผู้วิจัยจึงดำเนินการใช้วิธี Variance Thresholding ตัดตัวแปร LULC และ DEM ออกจากกระบวนการฝึกสอนโมเดล ซึ่งเป็นข้อปฏิบัติมาตรฐาน (Standard Pre-processing Step) ในการทำเหมืองข้อมูลและ Machine Learning (Kuhn & Johnson, 2013; Guyon & Elisseeff, 2003; Pedregosa et al., 2011)"

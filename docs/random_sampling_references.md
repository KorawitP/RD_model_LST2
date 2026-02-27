# อ้างอิงงานวิจัยสนับสนุนการสุ่มสกัดข้อมูล (Random Sampling Justification References)

## 1. ประเด็นเรื่อง: การลดอคติและความซ้ำซ้อนเชิงพื้นที่ (Reducing Bias & Spatial Autocorrelation)

การสุ่มตัวอย่างแบบ Random Sampling เป็นวิธีพื้นฐานที่ได้รับการยอมรับว่าช่วยสร้างชุดข้อมูลที่เป็นตัวแทน (Representative subset) ที่ปราศจากอคติ และบรรเทาปัญหาข้อมูลที่อยู่ใกล้เคียงกันมีความเหมือนกันมากเกินไป (Spatial Autocorrelation) ซึ่งจะนำไปสู่ Overfitting

**อ้างอิงที่แนะนำ:**

- **Belgiu, M., & Drăguţ, L. (2016).** Random forest in remote sensing: A review of applications and future directions. _ISPRS Journal of Photogrammetry and Remote Sensing_, 114, 24-31. [[DOI: 10.1016/j.isprsjprs.2016.01.011]](https://doi.org/10.1016/j.isprsjprs.2016.01.011)
  - _(งานวิจัยนี้เป็น Review Paper ที่ครอบคลุมเรื่อง Random Forest กับ Remote Sensing โดยอธิบายความสำคัญของการสุ่มตัวอย่าง Training data ที่ต้องเป็นกลาง)_
- **Stehman, S. V. (2009).** Sampling designs for accuracy assessment of land cover. _International Journal of Remote Sensing_, 30(20), 5243-5272. [[DOI: 10.1080/01431160903131000]](https://doi.org/10.1080/01431160903131000)
  - _(แม้จะเน้นเรื่อง Accuracy Assessment แต่เปเปอร์ระดับตำนานนี้ของ Stehman ยืนยันว่าศาสตร์ด้าน Remote Sensing ใช้ Probability Sampling (รวมถึง Simple Random Sampling) เป็นมาตรฐานเพื่อความถูกต้องทางสถิติและหลีกเลี่ยง Spatial Bias)_
- **Meyer, H., Reudenbach, C., Hengl, T., Katurji, M., & Bendix, J. (2018).** Improving performance of spatio-temporal machine learning models using forward feature selection and target-oriented validation. _Environmental Modelling & Software_, 101, 1-9. [[DOI: 10.1016/j.envsoft.2017.12.001]](https://doi.org/10.1016/j.envsoft.2017.12.001)
  - _(อธิบายชัดเจนเรื่องปัญหาความซ้ำซ้อนเชิงพื้นที่ (Spatial Autocorrelation) ในชุดข้อมูลขนาดใหญ่ และการได้มาซึ่งกลุ่มตัวอย่างที่เหมาะสม)_

## 2. ประเด็นเรื่อง: ขนาดของข้อมูลมีผลจํากัดต่ออัลกอริทึม (Performance Plateau of Random Forest)

งานวิจัยหลายชิ้นพิสูจน์แล้วว่า สำหรับอัลกอริทึมประเภทโครงสร้างต้นไม้ โดยเฉพาะ Random Forest เมื่อขนาดข้อมูลการสอน (Training Sample Size) ถึงจุดหนึ่ง (Threshold) ความแม่นยำจะคงที่ แม้จะเพิ่มข้อมูลมหาศาลก็แทบไม่ช่วยเพิ่มความแม่นยำ แต่กลับเสียเวลาประมวลผลแทน

**อ้างอิงที่แนะนำ:**

- **Millard, K., & Richardson, M. (2015).** On the importance of training data sample selection in random forest image classification: A case study in peatland ecosystem mapping. _Remote sensing_, 7(7), 8489-8515. [[DOI: 10.3390/rs70708489]](https://doi.org/10.3390/rs70708489)
  - _(เปเปอร์นี้ชี้แจ้งชัดเจนมากว่า สำหรับ Random Forest การเพิ่มขนาดตัวอย่าง (Sample Size) แบบสุ่ม จะเพิ่มความแม่นยำได้ในช่วงแรกเท่านั้น แต่หลักจากนั้นจะถึงจุดอิ่มตัว การใช้ตัวอย่างขนาดมหาศาลจึงไม่สมเหตุสมผลด้านทรัพยากรประมวลผล)_
- **Maxwell, A. E., Warner, T. A., & Fang, F. (2018).** Implementation of machine-learning classification in remote sensing: An applied review. _International Journal of Remote Sensing_, 39(9), 2784-2817. [[DOI: 10.1080/01431161.2018.1433343]](https://doi.org/10.1080/01431161.2018.1433343)
  - _(Review Paper ยอดฮิต อธิบายคุณสมบัติของ Machine Learning (RF, SVM, ANN) เทียบกับขนาดข้อมูล โดยยืนยันว่า Random Forest ทนทาน (Robust) ต่อขนาดตัวอย่าง และทำงานได้ดีโดยไม่ต้องใช้ประชากรข้อมูลทั้งหมด)_
- **Thanh Noi, P., & Kappas, M. (2018).** Comparison of random forest, k-nearest neighbor, and support vector machine classifiers for land cover classification using Sentinel-2 imagery. _Sensors_, 18(1), 18. [[DOI: 10.3390/s18010018]](https://doi.org/10.3390/s18010018)
  - _(งานวิจัยนี้ทดสอบขนาดตัวอย่าง (Sample Size) ตั้งแต่หลักร้อยไปจนถึงหลายหมื่น และพบว่าสำหรับ Random Forest ประสิทธิภาพจะเพิ่มสูงขึ้นอย่างชัดเจนจนมาถึงระดับประมาณ 10,000 - 20,000 พิกเซล หลังจากนั้นค่าความแม่นยำจะคงที่ (Plateau) และแทบไม่มีการเปลี่ยนแปลงแม้จะเพิ่มขนาดตัวอย่างให้ใหญ่กว่านี้ การใช้ 30,000 จุดจึงครอบคลุมเกินพอ)_
- **Colditz, R. R. (2015).** An evaluation of different training sample allocation schemes for discrete and continuous land cover classification using decision tree-based algorithms. _Remote Sensing_, 7(8), 9655-9681. [[DOI: 10.3390/rs70809655]](https://doi.org/10.3390/rs70809655)
  - _(ยืนยันว่าการกระจายตัวอย่างให้ครอบคลุม (Distribution representativeness) สำคัญกว่าขนาดตัวอย่างที่ใหญ่เกินความจำเป็น เมื่อมีตัวอย่างในระดับหลักหมื่นจุด ถือเป็นสัดส่วนที่อธิบายความหลากหลายของข้อมูลเชิงพื้นที่ระดับภูมิภาคได้เพียงพอแล้ว)_

## 3. ประเด็นเรื่อง: ความสมดุลระหว่าง Computational Efficiency และ Accuracy

**อ้างอิงที่แนะนำ:**

- **Foody, G. M., & Mathur, A. (2006).** The use of small training sets containing mixed pixels for accurate hard image classification: Training on mixed spectral responses for classification by a SVM. _Remote Sensing of Environment_, 103(2), 179-189. [[DOI: 10.1016/j.rse.2006.04.001]](https://doi.org/10.1016/j.rse.2006.04.001)
  - _(ให้แนวคิดพื้นฐานเรื่อง ไม่จำเป็นต้องใช้ข้อมูล Training Set ขนาดยักษ์ ก็สามารถได้โมเดลที่มีความแม่นยำสูงได้ หากกระบวนการคัดกรองตัวอย่าง (Sampling) ถูกต้อง)_
- **Rodriguez-Galiano, V. F., Ghimire, B., Rogan, J., Chica-Olmo, M., & Rigol-Sanchez, J. P. (2012).** An assessment of the effectiveness of a random forest classifier for land-cover classification. _ISPRS Journal of Photogrammetry and Remote Sensing_, 67, 93-104. [[DOI: 10.1016/j.isprsjprs.2011.11.002]](https://doi.org/10.1016/j.isprsjprs.2011.11.002)
  - _(เปเปอร์นี้เปรียบเทียบขนาดตัวอย่างหลายระดับ และสรุปได้ว่า Random Forest ต้องการตัวอย่างในจำนวนที่พอเหมาะเพื่อกระจายตัวไปบนโครงสร้างต้นไม้ (Trees) ต่างๆ การสุ่มตัวอย่างระดับหมื่นพิกเซลถือว่าครอบคลุมสำหรับการสร้างโมเดลที่มีความซับซ้อน)_

---

**สรุปการอ้างอิงในวิทยานิพนธ์ (ตัวอย่างการเขียน):**

"การกำหนดขนาดกลุ่มตัวอย่างแบบสุ่มเพื่อใช้เป็นชุดข้อมูลสำหรับฝึกสอนโมเดล (Training Data) อ้างอิงจากลักษณะเฉพาะในการเรียนรู้ของอัลกอริทึม Random Forest ที่ความแม่นยำจะเข้าสู่จุดอิ่มตัว (Performance Plateau) ทันทีที่รูปแบบความสัมพันธ์ถูกสร้างครอบคลุมความแปรปรวนของพื้นที่ (Robustness) การศึกษาพฤติกรรมนี้สนับสนุนว่าโมเดลจะมีประสิทธิภาพคงที่เมื่อขนาดตัวอย่างอยู่ในระดับ 10,000 ถึง 20,000 พิกเซล (Thanh Noi & Kappas, 2018) การใช้ขนาดตัวอย่างที่ 30,000 จุดภาพ จึงครอบคลุมระดับเกณฑ์ดังกล่าวเพื่อรับประกันว่าชุดข้อมูลได้อธิบายความแตกต่างของปัจจัยทางภูมิศาสตร์ได้อย่างครบถ้วนแล้ว นอกจากนี้เมื่องานวิจัยได้ประมวลผลร่วมกับข้อมูลอนุกรมเวลา (Time-series) จำนวน 94 เดือน ทำให้มิติข้อมูลที่ถูกวิเคราะห์จริงมีประชากรสูงถึงประมาณ 2.8 ล้านชุดข้อมูลย่อย (Instances) ซึ่งถือเป็นขนาดระดับ Big Data ที่อธิบายความหลายหลายและการกระจายประชากรอย่างเป็นตัวแทนได้ดีที่สุด (Colditz, 2015)

การเพิ่มจำนวนพิกเซลเริ่มต้นมากกว่าเกณฑ์ดังกล่าวจะไม่ช่วยสร้างนัยสำคัญต่อความแม่นยำ แต่มีส่วนเพิ่มภาระในการประมวลผลอย่างเสียเปล่า (Millard & Richardson, 2015; Maxwell et al., 2018) ควบคู่ไปกับเหตุผลการใช้วิธีสุ่มเชิงพื้นที่ (Spatial Random Sampling) แทนการดึงข้อมูลทั้งหมด ซึ่งได้รับการชี้แนะว่าเป็นวิธีการลดอคติทางสถิติและลดปัญหาพื้นที่ซ้ำซ้อน (Spatial Autocorrelation) ที่มักพบในชุดข้อมูลภาพถ่ายดาวเทียมที่กินบริเวณกว้าง (Stehman, 2009; Belgiu & Drăguţ, 2016)"

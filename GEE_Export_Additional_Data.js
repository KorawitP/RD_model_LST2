// ============================================================================================
// 🌍 Google Earth Engine Script สำหรับดึงข้อมูลสิ่งแวดล้อม
// ============================================================================================
// 📝 คำอธิบายสำหรับมือใหม่:
// สคริปต์นี้ทำหน้าที่เหมือน "หุ่นยนต์เก็บรวบรวมข้อมูล" จากดาวเทียมหลายดวง
// โดยเราจะสั่งให้มันไปดึงข้อมูลสภาพอากาศและสิ่งแวดล้อมในประเทศไทย ย้อนหลังตั้งแต่ปี 2018-2025
// เพื่อนำมาใช้เป็น "ตัวแปรต้น (Features)" ในการพยากรณ์อุณหภูมิพื้นผิว (LST)
// ============================================================================================

// --------------------------------------------------------------------------------------------
// 📍 ส่วนที่ 1: กำหนดพื้นที่และเวลา (Where & When)
// --------------------------------------------------------------------------------------------

// 1. กำหนดพื้นที่ศึกษา (Area of Interest)
// เราเลือก 'Thailand' จากฐานข้อมูลประเทศทั่วโลก (LSIB)
var thailand = ee
  .FeatureCollection("USDOS/LSIB_SIMPLE/2017")
  .filter(ee.Filter.eq("country_na", "Thailand")); // กรองเอาเฉพาะประเทศไทย

var geometry = thailand.geometry(); // แปลงเป็นรูปทรงเรขาคณิตเพื่อใช้ตัดขอบเขตข้อมูล

// 2. กำหนดช่วงเวลา (Time Range)
// เราต้องการข้อมูลรายเดือน ตั้งแต่ ม.ค. 2018 ถึง ต.ค. 2025 (รวม 94 เดือน)
var startDate = "2018-01-01";
var endDate = "2025-10-31";

// 3. ตั้งค่าการ Export (การบันทึกไฟล์)
var exportParams = {
  region: geometry, // พื้นที่ที่ต้องการบันทึก (ไทย)
  scale: 1000, // ความละเอียดของภาพ (Resolution) 1000 เมตร = 1 กิโลเมตร/พิกเซล
  crs: "EPSG:4326", // ระบบพิกัดแผนที่ (Latitude/Longitude มาตรฐานโลก)
  maxPixels: 1e13, // อนุญาตให้ประมวลผลพิกเซลจำนวนมากได้ (กัน Error)
  folder: "GEE_Research_Export", // ชื่อโฟลเดอร์ที่จะไปโผล่ใน Google Drive ของเรา
};

// ============================================================================================
// 🛰️ ส่วนที่ 2: การดึงข้อมูลทีละตัวแปร (Data Collection)
// ============================================================================================

// ---------------------------------------------------
// 1️⃣ Aerosol Optical Depth (AOD) - ฝุ่นละอองในอากาศ
// ---------------------------------------------------
// แหล่งข้อมูล: ดาวเทียม MODIS
// ทำไมต้องใช้? : ฝุ่นละอองช่วยบังแสงแดด อาจทำให้อุณหภูมิลดลง หรือเก็บความร้อนไว้ได้

print("Processing AOD... (กำลังประมวลผลข้อมูลฝุ่น AOD)");

var aod = ee
  .ImageCollection("MODIS/006/MOD08_M3")
  .select("Aerosol_Optical_Depth_Land_Mean") // เลือกเฉพาะค่าความหนาแน่นของฝุ่นบนบก
  .filterDate(startDate, endDate) // เลือกช่วงเวลา
  .filterBounds(geometry); // เลือกเฉพาะพื้นที่ไทย

// แปลงข้อมูลให้เป็นรายเดือนและตัดขอบเขตให้พอดีประเทศไทย
var aodMonthly = aod.map(function (img) {
  return img.clip(geometry).rename("AOD");
});

// รวมทุกเดือนเข้าด้วยกันเป็นไฟล์เดียว (Stack)
var aodStack = aodMonthly.toBands();

// สั่งให้บันทึกลง Google Drive
Export.image.toDrive({
  image: aodStack,
  description: "Monthly_AOD_2018-2025", // ชื่อไฟล์ที่จะบันทึก
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 2️⃣ Precipitation - ปริมาณน้ำฝน
// ---------------------------------------------------
// แหล่งข้อมูล: CHIRPS (ข้อมูลฝนรายวันความละเอียดสูง)
// ทำไมต้องใช้? : ฝนทำให้พื้นดินเปียกและเย็นลง ส่งผลโดยตรงต่อ LST

print("Processing Precipitation... (กำลังประมวลผลข้อมูลน้ำฝน)");

var precip = ee
  .ImageCollection("UCSB-CHG/CHIRPS/DAILY")
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// รวมข้อมูลรายวันให้เป็น "ผลรวมรายเดือน" (Monthly Sum)
var precipMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function (m) {
    var start = ee.Date(startDate).advance(m, "month");
    var end = start.advance(1, "month");

    return precip
      .filterDate(start, end)
      .sum() //.sum() คือการรวมปริมาณฝนทั้งเดือน
      .clip(geometry)
      .rename("Precipitation")
      .set("system:time_start", start.millis());
  }),
);

var precipStack = precipMonthly.toBands();

Export.image.toDrive({
  image: precipStack,
  description: "Monthly_Precipitation_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 3️⃣ Soil Moisture - ความชื้นในดิน
// ---------------------------------------------------
// แหล่งข้อมูล: ดาวเทียม SMAP (NASA)
// ทำไมต้องใช้? : ดินที่ชื้นจะระเหยน้ำได้ดี ช่วยลดอุณหภูมิพื้นผิว

print("Processing Soil Moisture... (กำลังประมวลผลความชื้นในดิน)");

var soilMoisture = ee
  .ImageCollection("NASA_USDA/HSL/SMAP10KM_soil_moisture")
  .select("ssm") // ssm = surface soil moisture (ความชื้นผิวดิน)
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// หาค่าเฉลี่ยรายเดือน (Monthly Mean)
var soilMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function (m) {
    var start = ee.Date(startDate).advance(m, "month");
    var end = start.advance(1, "month");

    return soilMoisture
      .filterDate(start, end)
      .mean() // .mean() คือหาค่าเฉลี่ยของทั้งเดือน
      .clip(geometry)
      .rename("Soil_Moisture")
      .set("system:time_start", start.millis());
  }),
);

var soilStack = soilMonthly.toBands();

Export.image.toDrive({
  image: soilStack,
  description: "Monthly_Soil_Moisture_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 4️⃣ Wind Speed - ความเร็วลม
// ---------------------------------------------------
// แหล่งข้อมูล: ERA5 (ECMWF) โมเดลสภาพอากาศระดับโลก
// ทำไมต้องใช้? : ลมช่วยพัดพาความร้อนออกจากพื้นผิว ทำให้เย็นลง (Wind Cooling Effect)

print("Processing Wind Speed... (กำลังประมวลผลความเร็วลม)");

var wind = ee
  .ImageCollection("ECMWF/ERA5/MONTHLY")
  .select(["u_component_of_wind_10m", "v_component_of_wind_10m"]) // ลมแกน U (ตะวันออก-ตก) และ V (เหนือ-ใต้)
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// คำนวณความเร็วลมรวม (Magnitude) จากสูตร Pythagoras: sqrt(u² + v²)
var windSpeed = wind.map(function (img) {
  var u = img.select("u_component_of_wind_10m");
  var v = img.select("v_component_of_wind_10m");
  var speed = u.pow(2).add(v.pow(2)).sqrt(); // สูตรคำนวณความเร็วลมรวม
  return speed.clip(geometry).rename("Wind_Speed");
});

var windStack = windSpeed.toBands();

Export.image.toDrive({
  image: windStack,
  description: "Monthly_Wind_Speed_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 5️⃣ Relative Humidity - ความชื้นสัมพัทธ์
// ---------------------------------------------------
// แหล่งข้อมูล: ERA5
// ทำไมต้องใช้? : ความชื้นในอากาศสูงจะเก็บความร้อนได้ดี (Greenhouse effect ย่อยๆ)

print("Processing Relative Humidity... (กำลังประมวลผลความชื้นสัมพัทธ์)");

var humidity = ee
  .ImageCollection("ECMWF/ERA5/MONTHLY")
  .select(["mean_2m_air_temperature", "dewpoint_2m_temperature"])
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// คำนวณความชื้นสัมพัทธ์จากสูตรทางอุตุนิยมวิทยา (August-Roche-Magnus approximation)
var rh = humidity.map(function (img) {
  var temp = img.select("mean_2m_air_temperature").subtract(273.15); // แปลง Kelvin เป็น Celsius
  var dewpoint = img.select("dewpoint_2m_temperature").subtract(273.15);

  // สูตรคำนวณ Vapor Pressure
  var es = temp.multiply(17.27).divide(temp.add(237.3)).exp().multiply(6.112);
  var e = dewpoint
    .multiply(17.27)
    .divide(dewpoint.add(237.3))
    .exp()
    .multiply(6.112);
  var relHumidity = e.divide(es).multiply(100); // หน่วยเป็น %

  return relHumidity.clip(geometry).rename("Relative_Humidity");
});

var rhStack = rh.toBands();

Export.image.toDrive({
  image: rhStack,
  description: "Monthly_Relative_Humidity_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 6️⃣ Evapotranspiration (ET) - การคายระเหยน้ำ
// ---------------------------------------------------
// แหล่งข้อมูล: MODIS (MOD16A2)
// ทำไมต้องใช้? : การคายน้ำของพืชช่วยลดอุณหภูมิ (เหมือนเหงื่อออกแล้วเย็น)

print("Processing Evapotranspiration... (กำลังประมวลผลการคายระเหยน้ำ)");

var et = ee
  .ImageCollection("MODIS/006/MOD16A2")
  .select("ET") // Evapotranspiration
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// หาค่าเฉลี่ยรายเดือน
var etMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function (m) {
    var start = ee.Date(startDate).advance(m, "month");
    var end = start.advance(1, "month");

    return et
      .filterDate(start, end)
      .mean()
      .clip(geometry)
      .rename("Evapotranspiration")
      .set("system:time_start", start.millis());
  }),
);

var etStack = etMonthly.toBands();

Export.image.toDrive({
  image: etStack,
  description: "Monthly_Evapotranspiration_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ---------------------------------------------------
// 7️⃣ Cloud Cover - ปริมาณเมฆ
// ---------------------------------------------------
// แหล่งข้อมูล: ERA5
// ทำไมต้องใช้? : เมฆบังแดดตอนกลางวัน (เย็นลง) และกักเก็บความร้อนตอนกลางคืน

print("Processing Cloud Cover... (กำลังประมวลผลปริมาณเมฆ)");

var cloud = ee
  .ImageCollection("ECMWF/ERA5/MONTHLY")
  .select("total_cloud_cover")
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

var cloudMonthly = cloud.map(function (img) {
  return img.clip(geometry).rename("Cloud_Cover");
});

var cloudStack = cloudMonthly.toBands();

Export.image.toDrive({
  image: cloudStack,
  description: "Monthly_Cloud_Cover_2018-2025",
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels,
});

// ============================================================================================
// ✅ สรุปการทำงาน (Summary)
// ============================================================================================
print("========================================");
print("Export Tasks Created: (สร้างงานเตรียมบันทึกไฟล์เรียบร้อย)");
print("1. ฝุ่น (AOD)");
print("2. น้ำฝน (Precipitation)");
print("3. ความชื้นในดิน (Soil Moisture)");
print("4. ความเร็วลม (Wind Speed)");
print("5. ความชื้นสัมพัทธ์ (Relative Humidity)");
print("6. การคายระเหยน้ำ (Evapotranspiration)");
print("7. ปริมาณเมฆ (Cloud Cover)");
print("----------------------------------------");
print("👉 วิธีการเซฟไฟล์จริง:");
print('1. ไปที่แท็บ "Tasks" (ด้านขวาของหน้าจอ)');
print('2. กดปุ่ม "RUN" สีฟ้า หลังรายชื่อไฟล์แต่ละอัน');
print('3. ไฟล์จะถูกส่งไปที่ Google Drive ในโฟลเดอร์ "GEE_Research_Export"');
print("========================================");

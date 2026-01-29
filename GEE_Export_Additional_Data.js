// ========================================
// Google Earth Engine Script
// Export Additional Variables for LST Prediction
// ========================================

// 1. กำหนดพื้นที่ศึกษา (ประเทศไทย)
var thailand = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
  .filter(ee.Filter.eq('country_na', 'Thailand'));

var geometry = thailand.geometry();

// 2. กำหนดช่วงเวลา
var startDate = '2018-01-01';
var endDate = '2025-10-31';

// 3. กำหนดพารามิเตอร์ Export
var exportParams = {
  region: geometry,
  scale: 1000,  // 1 km resolution
  crs: 'EPSG:4326',
  maxPixels: 1e13,
  folder: 'GEE_Research_Export'  // โฟลเดอร์ใน Google Drive
};

// ========================================
// 1. Aerosol Optical Depth (AOD) - MODIS
// ========================================
print('Processing AOD...');

var aod = ee.ImageCollection('MODIS/006/MOD08_M3')
  .select('Aerosol_Optical_Depth_Land_Mean')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Resample to monthly
var aodMonthly = aod.map(function(img) {
  return img.clip(geometry).rename('AOD');
});

var aodStack = aodMonthly.toBands();

Export.image.toDrive({
  image: aodStack,
  description: 'Monthly_AOD_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('AOD bands:', aodStack.bandNames());

// ========================================
// 2. Precipitation (ปริมาณฝน) - CHIRPS
// ========================================
print('Processing Precipitation...');

var precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Aggregate to monthly
var precipMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function(m) {
    var start = ee.Date(startDate).advance(m, 'month');
    var end = start.advance(1, 'month');
    
    return precip
      .filterDate(start, end)
      .sum()
      .clip(geometry)
      .rename('Precipitation')
      .set('system:time_start', start.millis());
  })
);

var precipStack = precipMonthly.toBands();

Export.image.toDrive({
  image: precipStack,
  description: 'Monthly_Precipitation_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Precipitation bands:', precipStack.bandNames());

// ========================================
// 3. Soil Moisture (ความชื้นในดิน) - SMAP
// ========================================
print('Processing Soil Moisture...');

var soilMoisture = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture')
  .select('ssm')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Aggregate to monthly mean
var soilMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function(m) {
    var start = ee.Date(startDate).advance(m, 'month');
    var end = start.advance(1, 'month');
    
    return soilMoisture
      .filterDate(start, end)
      .mean()
      .clip(geometry)
      .rename('Soil_Moisture')
      .set('system:time_start', start.millis());
  })
);

var soilStack = soilMonthly.toBands();

Export.image.toDrive({
  image: soilStack,
  description: 'Monthly_Soil_Moisture_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Soil Moisture bands:', soilStack.bandNames());

// ========================================
// 4. Wind Speed (ความเร็วลม) - ERA5
// ========================================
print('Processing Wind Speed...');

var wind = ee.ImageCollection('ECMWF/ERA5/MONTHLY')
  .select(['u_component_of_wind_10m', 'v_component_of_wind_10m'])
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Calculate wind speed magnitude
var windSpeed = wind.map(function(img) {
  var u = img.select('u_component_of_wind_10m');
  var v = img.select('v_component_of_wind_10m');
  var speed = u.pow(2).add(v.pow(2)).sqrt();
  return speed.clip(geometry).rename('Wind_Speed');
});

var windStack = windSpeed.toBands();

Export.image.toDrive({
  image: windStack,
  description: 'Monthly_Wind_Speed_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Wind Speed bands:', windStack.bandNames());

// ========================================
// 5. Relative Humidity (ความชื้นสัมพัทธ์) - ERA5
// ========================================
print('Processing Relative Humidity...');

var humidity = ee.ImageCollection('ECMWF/ERA5/MONTHLY')
  .select(['mean_2m_air_temperature', 'dewpoint_2m_temperature'])
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Calculate relative humidity
var rh = humidity.map(function(img) {
  var temp = img.select('mean_2m_air_temperature').subtract(273.15); // K to C
  var dewpoint = img.select('dewpoint_2m_temperature').subtract(273.15);
  
  // Simplified RH calculation
  var es = temp.multiply(17.27).divide(temp.add(237.3)).exp().multiply(6.112);
  var e = dewpoint.multiply(17.27).divide(dewpoint.add(237.3)).exp().multiply(6.112);
  var relHumidity = e.divide(es).multiply(100);
  
  return relHumidity.clip(geometry).rename('Relative_Humidity');
});

var rhStack = rh.toBands();

Export.image.toDrive({
  image: rhStack,
  description: 'Monthly_Relative_Humidity_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Relative Humidity bands:', rhStack.bandNames());

// ========================================
// 6. Evapotranspiration (การคายน้ำ) - MODIS
// ========================================
print('Processing Evapotranspiration...');

var et = ee.ImageCollection('MODIS/006/MOD16A2')
  .select('ET')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

// Aggregate to monthly
var etMonthly = ee.ImageCollection(
  ee.List.sequence(0, 93).map(function(m) {
    var start = ee.Date(startDate).advance(m, 'month');
    var end = start.advance(1, 'month');
    
    return et
      .filterDate(start, end)
      .mean()
      .clip(geometry)
      .rename('Evapotranspiration')
      .set('system:time_start', start.millis());
  })
);

var etStack = etMonthly.toBands();

Export.image.toDrive({
  image: etStack,
  description: 'Monthly_Evapotranspiration_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Evapotranspiration bands:', etStack.bandNames());

// ========================================
// 7. Cloud Cover (ปริมาณเมฆ) - ERA5
// ========================================
print('Processing Cloud Cover...');

var cloud = ee.ImageCollection('ECMWF/ERA5/MONTHLY')
  .select('total_cloud_cover')
  .filterDate(startDate, endDate)
  .filterBounds(geometry);

var cloudMonthly = cloud.map(function(img) {
  return img.clip(geometry).rename('Cloud_Cover');
});

var cloudStack = cloudMonthly.toBands();

Export.image.toDrive({
  image: cloudStack,
  description: 'Monthly_Cloud_Cover_2018-2025',
  folder: exportParams.folder,
  region: exportParams.region,
  scale: exportParams.scale,
  crs: exportParams.crs,
  maxPixels: exportParams.maxPixels
});

print('Cloud Cover bands:', cloudStack.bandNames());

// ========================================
// สรุป
// ========================================
print('========================================');
print('Export Tasks Created:');
print('1. Monthly_AOD_2018-2025.tif');
print('2. Monthly_Precipitation_2018-2025.tif');
print('3. Monthly_Soil_Moisture_2018-2025.tif');
print('4. Monthly_Wind_Speed_2018-2025.tif');
print('5. Monthly_Relative_Humidity_2018-2025.tif');
print('6. Monthly_Evapotranspiration_2018-2025.tif');
print('7. Monthly_Cloud_Cover_2018-2025.tif');
print('========================================');
print('Go to Tasks tab and click RUN for each export');
print('Files will be saved to Google Drive folder: GEE_Research_Export');

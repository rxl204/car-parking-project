-- BigQuery SQL

-- get total lots
SELECT DISTINCT carpark_number, total_lots
FROM `car-parking-project-419309.sg_car_parking.car_parking_availability`
WHERE DATE(timestamp) = '2024-04-11'

-- get hourly lots
SELECT  
  carpark_number,
  address,
  hour,
  average_lots_available,
  total_lots,
  (total_lots-average_lots_available)/total_lots AS utilisation_rate
FROM(
SELECT  
  carpark_number,
  address,
  FORMAT_TIMESTAMP('%H', TIMESTAMP(timestamp)) AS hour,
  ROUND(AVG(lots_available)) as average_lots_available,
  AVG(total_lots) as total_lots
FROM `car-parking-project-419309.sg_car_parking.car_parking_availability` 
WHERE DATE(timestamp) = '2024-04-09'
GROUP BY carpark_number, address, hour)
hourly_lots
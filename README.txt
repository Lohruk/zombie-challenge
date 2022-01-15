API Endpoints:

GET localhost:8000/survivors/ -> List of all non-infected survivors.

POST localhost:8000/survivors/ -> Add a new survivor. 
Mandatory Fields: name, age, last_location_lat, last_location_long. 
Important: Add inventory items here. fiji_water = water supply, campbell_soup = food supply, first_aid_pouch = healing supply, ak_47 = gun supply

PUT localhost:800/survivors/infected/id -> Flag survivor as infected (requires 5 flags to be infected)

PUT localhost:8000/survivors/coordinates/id -> Change survivor current coordinates.
Important: Must send on Body -> last_location_lat, last_location_long. 

PUT localhost:8000/survivors/trade/1/ -> Create a new trade.
Mandatory Fields: survivor_1_id, survivor_2_id, survivor_1_water, survivor_2_water, survivor_1_soup, survivor_2_soup
survivor_1_first_aid, survivor_2_first_aid, survivor_1_gun, survivor_2_gun
Important: Trades must have equal values. Infected survivors can't trade.

POST localhost:8000/report/ -> generate a new report with all necessary info.

GET localhost:8000/report/ -> display the last generated report.

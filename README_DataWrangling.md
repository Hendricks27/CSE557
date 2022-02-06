# README.md


# Data Wrangling Process
Feb 6, 2022


## There were three parts of the data wrangling results.

## CSV TABLES

### The gps_anno.csv file documented the mapped GPS data. 
#### The dataframe in the script was called log  
  log.loc[0]  
| column|value |annotation |
|-------|------|-----------|
|name|                                    WillemVasco-Pais  |      [whole name of the employee]  |
|date |                                         01/06/2014   |     [the date from the timestamp of the GPS data, used to merge the credit/loyalty card records]|  
|hour  |                                                 6    |    [the hour from the timestamp of the GPS data, used to merge the credit card records]  |
|loc    |                                              NaN     |   [the mapped location of the the restaurants/cafes/diners where employees had ever paid with credit/loyalty cards]|  
|LastName|                                      Vasco-Pais  | |
|FirstName|                                         Willem  | |
|id        |                                          35.0   |     [the CarID, used to merge the car assignment table for employee personal details]  |
|CurrentEmploymentType |                         Executive  | |
|CurrentEmploymentTitle |     Environmental Safety Advisor  | |
|Timestamp   |                         01/06/2014 06:28:01  | |
|lat          |                                  36.076225  | |
|long          |                                 24.874689  | |
|min            |                                       28   |     [the minute from the timestamp of the GPS data]  |
|sec             |                                       1    |    [the second from the timestamp of the GPS data]  |
|geometry         |         POINT (24.87468932 36.0762253)     |   [generated from lat and long, for the GeoPandas plots] | 
|Name: 0, dtype: object | 
  
  
### The home_anno.csv documented the longitudes and the latitudes of employees' home addresses.  
The dataframe in the script was called home (Pandas DataFrame) and home1 (GeoPandas GeoDataFrame, home + 1 column ('geometry')).  
The home addresses were extracted from each employee's last GPS entry every night and first GPS entry every morning.  
  home1.head()  
| |   id  |      lat    |   long  |                 geometry  |
|-|-------|------------|----------|---------------------------|
|0|  35.0 | 36.076225  |24.874666 | POINT (24.87467 36.07623)  |
|1|   4.0 | 36.078193  |24.872124 | POINT (24.87212 36.07819)  |
|2|  19.0  |36.087839  |24.856341  |POINT (24.85634 36.08784)  |
|3|  10.0  |36.076844 | 24.865886  |POINT (24.86589 36.07684)  |
|4|   7.0  |36.084427|  24.864195  |POINT (24.86419 36.08443)  |
  
  
### The locations_anno.csv documented the longitudes and the latitudes of the restaurants/cafes/diners where employees had ever paid with credit/loyalty cards.  
The dataframe in the script was called locations (Pandas DataFrame) and locations1 (GeoPandas GeoDataFrame, locations + 1 column ('geometry')).  
The locations were extracted from the last GPS entry before employees paid with their credit cards or the first GPS entry after they paid.  
  locations1.head()  
|  |                     loc|        lat|       long|                   geometry|
|--|------------------------|-----------|-----------|---------------------------|
|0|    Brew've Been Served|  36.054044|  24.901206|  POINT (24.90121 36.05404)|  
|1|       Hallowed Grounds|   36.04803|  24.879575|  POINT (24.87957 36.04803)|  
|2|        Coffee Cameleon|  36.048024|  24.879576|  POINT (24.87958 36.04802)|  
|10|  Bean There Done That|  36.065827|  24.852365|  POINT (24.85237 36.06583)|  
|11|     Brewed Awakenings|  36.054488|  24.899954|  POINT (24.89995 36.05449)|  
  





  
## INTERMEDIATE PLOTS
The plots were placed in two folders, Car_Date, and Loc_Date.  
  
### The Car_Date was to answer the first question: 
      Describe common daily routines for GAStech employees. What does a day in the life of a typical GAStech employee look like?  
####    The plots were based on employee and date, colored by hour, and named with the rule ID|CAR_ID|_|DATE|.jpg.
By looking at the plots for the same employee, the routine and the outliners were identified.  
#### To-do: 
a) Add individual home addresses and locations of the cafes/diners/restaurants to the map?  
b) Make the plots from different dates automatedly play as a video after choosing a specific employee?  
c) Is this the best or most direct way to show the routine?  


### The Loc_Date was a trial to help answer the second question:
      Identify up to twelve unusual events or patterns that you see in the data.  
#### The plots were based on location, date and hour, colored by employee, and named with the rule |LOCATION NAME|_|DATE|_|HOUR|.jpg.
Only events in unusual hours (before 9 AM and after 16 PM) and events with no less than 2 people in the same location and hour were included.  
#### To-do: 
a) Add individual home addresses and locations of the cafes/diners/restaurants to the map?  
b) There were many data which did not get mapped to the credit/loyalty card records, e.g., the data of the trucks and truck drivers.  
c) More ways for visualization.  





  
## PYTHON SCRIPT
The script was named 'main.py'.  
The annotations were also done.  
  
  
  

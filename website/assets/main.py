import numpy as np
import matplotlib.pyplot as plt
import shapefile
import pandas as pd
import geopandas as gpd

loc = {"Brew've Been Served": 0, "Hallowed Grounds": 1, "Coffee Cameleon": 2, "Abila Airport": 3,
       "Kronos Pipe and Irrigation": 4, "Nationwide Refinery": 5, "Maximum Iron and Steel": 6,
       "Stewart and Sons Fabrication": 7, "Carlyle Chemical Inc.": 8, "Coffee Shack": 9, "Bean There Done That": 10,
       "Brewed Awakenings": 11, "Jack's Magical Beans": 12, "Katerinas Café": 13, "Hippokampos": 14,
       "Abila Zacharo": 15, "Gelatogalore": 16, "Kalami Kafenion": 17, "Ouzeri Elian": 18, "Guy's Gyros": 19,
       "U-Pump": 20, "Frydos Autosupply n' More": 21, "Albert's Fine Clothing": 22, "Shoppers' Delight": 23,
       "Abila Scrapyard": 24, "Frank's Fuel": 25, "Chostus Hotel": 26, "General Grocer": 27, "Kronos Mart": 28,
       "Octavio's Office Supplies": 29, "Roberts and Sons": 30, "Ahaggo Museum": 31, "Desafio Golf Course": 32,
       "Daily Dealz": 33}
loc_re = {0: "Brew've Been Served", 1: "Hallowed Grounds", 2: "Coffee Cameleon", 3: "Abila Airport",
          4: "Kronos Pipe and Irrigation", 5: "Nationwide Refinery", 6: "Maximum Iron and Steel",
          7: "Stewart and Sons Fabrication", 8: "Carlyle Chemical Inc.", 9: "Coffee Shack", 10: "Bean There Done That",
          11: "Brewed Awakenings", 12: "Jack's Magical Beans", 13: "Katerinas Café", 14: "Hippokampos",
          15: "Abila Zacharo", 16: "Gelatogalore", 17: "Kalami Kafenion", 18: "Ouzeri Elian", 19: "Guy's Gyros",
          20: "U-Pump", 21: "Frydos Autosupply n' More", 22: "Albert's Fine Clothing", 23: "Shoppers' Delight",
          24: "Abila Scrapyard", 25: "Frank's Fuel", 26: "Chostus Hotel", 27: "General Grocer", 28: "Kronos Mart",
          29: "Octavio's Office Supplies", 30: "Roberts and Sons", 31: "Ahaggo Museum", 32: "Desafio Golf Course",
          33: "Daily Dealz"}


def read_shapefile(shapefile):
    fields = [x[0] for x in shapefile.fields][1:]
    records = shapefile.records()
    shps = [s.points for s in shapefile.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df


def plot_map(shapefile):
    # plot the kronos and abila as background based on the shapefile
    plt.figure(figsize=(11, 9))
    for shape in shapefile.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'gray', alpha=0.5)


def deal_time(df, col):
    # split the timestamp to hours, minutes and seconds
    df['date'] = df[col].str.split(' ', expand=True)[0]
    df['time'] = df[col].str.split(' ', expand=True)[1]
    df['time'] = pd.to_datetime(df['time'])
    df['hour'] = df['time'].dt.hour
    df['min'] = df['time'].dt.minute
    df['sec'] = df['time'].dt.second
    df = df.drop(columns='time')
    return df


def time_zeros(df, col):
    # deal with the date format: convert from 1/6/2014 to 01/06/2014
    for i in range(0, len(df)):
        day = df.loc[i, col].split('/')[1]
        others = df.loc[i, col].split('/')[2]
        if int(day) < 10:
            string = '01/0' + day + '/' + others
        else:
            string = '01/' + day + '/' + others
        df.loc[i, col] = string
    return df


if __name__ == '__main__':
    file_path = '/Users/haofan/Library/CloudStorage/OneDrive-WashingtonUniversityinSt.Louis/22Spring/AdViz/'

    # ---------------------------------------------------------------------------------------------------------------- #
    # the first parts
    # ---------------------------------------------------------------------------------------------------------------- #

    # read kronos map from shapefiles
    kronos_dbf = gpd.read_file(file_path + 'Assignment2 Data/Geospatial/Kronos_Island.dbf')
    kronos_shp = gpd.read_file(file_path + 'Assignment2 Data/Geospatial/Kronos_Island.shp')
    kronos_shx = gpd.read_file(file_path + 'Assignment2 Data/Geospatial/Kronos_Island.shx')
    print(kronos_shp.total_bounds)      # array([23.4315, 35.7095, 26.0324, 36.3932])
    print(kronos_shp.crs)
    # <Geographic 2D CRS: EPSG:4326>
    # Name: WGS 84
    # Axis Info [ellipsoidal]:
    # - Lat[north]: Geodetic latitude (degree)
    # - Lon[east]: Geodetic longitude (degree)
    # Area of Use:
    # - name: World.
    # - bounds: (-180.0, -90.0, 180.0, 90.0)
    # Datum: World Geodetic System 1984 ensemble
    # - Ellipsoid: WGS 84
    # - Prime Meridian: Greenwich
    print(kronos_shp.shape)     # (1, 2)

    kronos = shapefile.Reader(file_path + 'Assignment2 Data/Geospatial/Kronos_Island')
    k_shapes = kronos.shapes()

    # read abila map from shapefiles
    abila = shapefile.Reader(file_path + 'Assignment2 Data/Geospatial/Abila')
    a_df = read_shapefile(abila)

    # read credit card records, and deal with timestamp formatting and locations
    cc = pd.read_csv(file_path + 'Assignment2 Data/cc_data.csv', encoding='latin-1')
    cc = deal_time(cc, 'timestamp')
    cc = cc.drop(columns='sec')
    cc = time_zeros(cc, 'date')
    cc = time_zeros(cc, 'timestamp')
    for i in range(0, len(cc)):
        cc.loc[i, 'loc'] = loc[cc.loc[i, 'location']]

    # read loyalty card records, and deal with date formatting and locations
    lc = pd.read_csv(file_path + 'Assignment2 Data/loyalty_data.csv', encoding='latin-1')
    lc = lc.rename({'timestamp': 'date'}, axis='columns')
    lc = time_zeros(lc, 'date')
    for i in range(0, len(lc)):
        lc.loc[i, 'loc'] = loc[lc.loc[i, 'location']]

    # read the gps data, and deal with timestamp formatting
    # join the longitude and latitude to GeoPandas Point format
    gps = pd.read_csv(file_path + 'Assignment2 Data/gps.csv')
    gps = deal_time(gps, 'Timestamp')
    gps = gpd.GeoDataFrame(gps, geometry=gpd.points_from_xy(gps.long, gps.lat))
    gps.crs = 'EPSG:4326'

    # read car assignment data, and map the records of cards to the car assignments and employees
    car = pd.read_csv(file_path + 'Assignment2 Data/car-assignments.csv')
    car['name'] = car['FirstName'] + car['LastName']
    car = car.rename({'CarID': 'id'}, axis='columns')
    cc = cc.merge(car, how='left', on=['LastName', 'FirstName'])
    lc = lc.merge(car, how='left', on=['LastName', 'FirstName'])
    cc = cc.rename({'CarID': 'id'}, axis='columns')
    print(cc['name'].isnull().sum() / len(cc))      # 20.59%
    cc['name'] = cc['FirstName'] + cc['LastName']
    lc = lc.rename({'CarID': 'id'}, axis='columns')
    print(lc['name'].isnull().sum() / len(lc))      # 20.39%
    lc['name'] = lc['FirstName'] + lc['LastName']

    # group the card records and join them based on employee, date and hour in the records
    # call them events
    events = pd.DataFrame(cc.groupby(by=['name', 'date', 'hour'])['loc'].unique()).reset_index()
    events = events.explode('loc')
    events_lc = pd.DataFrame(lc.groupby(by=['name', 'date'])['loc'].unique()).reset_index()
    events_lc = events_lc.explode('loc')
    events_full = events.merge(events_lc, how='outer', on=['name', 'date', 'loc'])
    events_full = events_full.merge(car, how='left', on='name')

    # join the events with gps data
    log = events_full.merge(gps, how='right', on=['id', 'date', 'hour'])

    # fill in the NaN values based on the car assignments
    for i in range(0, len(log)):
        if (not np.isnan(log.loc[i, 'id'])) & (log.loc[i, 'name'] is np.nan):
            if log.loc[i, 'id'] in range(0, 36):
                log.loc[i, 'name'] = car.loc[car['id'] == log.loc[i, 'id'], 'name'].values[0]
                log.loc[i, 'FirstName'] = car.loc[car['id'] == log.loc[i, 'id'], 'FirstName'].values[0]
                log.loc[i, 'LastName'] = car.loc[car['id'] == log.loc[i, 'id'], 'LastName'].values[0]
                log.loc[i, 'CurrentEmploymentType'] = car.loc[car['id'] == log.loc[i, 'id'],
                                                              'CurrentEmploymentType'].values[0]
                log.loc[i, 'CurrentEmploymentTitle'] = car.loc[car['id'] == log.loc[i, 'id'],
                                                               'CurrentEmploymentTitle'].values[0]
    log['hour'] = log['hour'].astype('int64')

    log.to_csv(file_path + 'Assignment2/gps_anno.csv')

    # recognize their homes, plot the homes and locations of diners, cafes, etc.
    home = {}
    for i, id in enumerate(log['id'].unique()):
        log_per = gpd.GeoDataFrame(log[log['id'] == id][['id','hour', 'min', 'sec', 'lat', 'long']])
        night = log_per[log_per['hour'] == max(log_per['hour'])]
        night = night[night['min'] == max(night['min'])]
        night = night[night['sec'] == max(night['sec'])]
        # morn = log_per[log_per['hour'] == min(log_per['hour'])]
        # morn = morn[morn['min'] == min(morn['min'])]
        # morn = morn[morn['sec'] == min(morn['sec'])]
        # print(id, ' ', night.distance(morn))
        home[i] = {'id': night['id'].values[0], 'lat': night['lat'].values[0], 'long': night['long'].values[0]}
    home = pd.DataFrame(home).T
    geometry = gpd.points_from_xy(home['long'], home['lat'])
    home1 = gpd.GeoDataFrame(home, geometry=geometry)
    plot_map(abila)
    ax = plt.subplot()
    ax.set_aspect('equal')
    home1.plot(ax=ax, marker='o', c=home1['id'], cmap='tab20', markersize=8)
    plt.legend()
    plt.savefig(file_path + 'Assignment2/home.jpg')
    home1.to_csv(file_path + 'Assignment2/home_anno.csv')

    locations = {}
    for i in range(0, 34):
        location = loc_re[i]
        log_loc = gpd.GeoDataFrame(log[log['loc'] == i][['Timestamp', 'id', 'lat', 'long']])
        for id in log_loc['id'].unique():
            time = cc[(cc['id'] == id) & (cc['loc'] == i)]['timestamp']
            if len(time) > 0:
                break
        if not isinstance(time, str):
            for num in range(0, len(time)):
                t = time.iloc[num]
                if t in log_loc:
                    break
        if len(t) == 0:
            t = log_loc[log_loc['Timestamp'] == min(log_loc['Timestamp'])]['Timestamp']
            print(t)
        record = gpd.GeoDataFrame(log_loc[(log_loc['id'] == id) & (log_loc['Timestamp'] <= t)])
        if len(record) > 1:
            record = record[record['Timestamp'] == max(record['Timestamp'])]
        if len(record) > 0:
            locations[i] = {'loc': location, 'lat': record['lat'].values[0], 'long': record['long'].values[0]}
        else:
            record = gpd.GeoDataFrame(log_loc[(log_loc['id'] == id) & (log_loc['Timestamp'] >= t)])
            if len(record) > 1:
                record = record[record['Timestamp'] == min(record['Timestamp'])]
            if len(record) > 0:
                locations[i] = {'loc': location, 'lat': record['lat'].values[0], 'long': record['long'].values[0]}
    locations = pd.DataFrame(locations).T
    geometry = gpd.points_from_xy(locations['long'], locations['lat'])
    locations1 = gpd.GeoDataFrame(locations, geometry=geometry)
    plot_map(abila)
    ax = plt.subplot()
    ax.set_aspect('equal')
    locations1.plot(ax=ax, marker='*', c=i, cmap='tab20', markersize=20)
    plt.savefig(file_path + 'Assignment2/locations.jpg')
    locations1.to_csv(file_path + 'Assignment2/locations_anno.csv')

    # ---------------------------------------------------------------------------------------------------------------- #
    # the third parts
    # ---------------------------------------------------------------------------------------------------------------- #

    # plot based on employee + date, color by hour
    # these plots show employees' day routines, and show abnormal events if unique
    for i, id in enumerate(log['id'].unique()):
        for num, day in enumerate(log['date'].unique()):
            print(id, ' ', day)
            log_per = gpd.GeoDataFrame(log[(log['id'] == id) & (log['date'] == day)][['hour', 'geometry']])
            plot_map(abila)
            if len(log_per) > 0:
                ax = plt.subplot()
                ax.set_aspect('equal')
                log_per.plot(ax=ax, marker='o', c='hour', cmap='tab10', markersize=3)
            plt.savefig(file_path + 'Assignment2/Car_Date/ID' + str(id) + '_' + day[3:5] + '.jpg')

    # plot based on location + date + hour, color by employee
    # these plots show if employees gather outside office hours
    for i in range(0, 34):
        location = loc_re[i]
        for num, day in enumerate(log['date'].unique()):
            log_loc = log[(log['loc'] == i) & (log['date'] == day)][['Timestamp', 'id', 'hour', 'min', 'lat', 'long']]
            if len(log_loc) > 0:
                # group by hour, to see if there are gatherings
                log_lochour = pd.DataFrame(log_loc.groupby(by=['hour'])['id'].unique()).reset_index()

                # pick the gatherings before 9 AM and after 16 PM
                gather = log_lochour[((log_lochour['hour'] < 9) | (log_lochour['hour'] > 16))]
                drop_ind = []
                for ind in gather.index:
                    if len(gather.loc[ind, 'id']) <= 1:
                        drop_ind.append(ind)
                gather = gather.drop(index=drop_ind)
                if len(gather) > 0:
                    for line in gather.index:
                        gather_loc = log_loc[(log_loc['hour'] == gather.loc[line, 'hour']) &
                                             (log_loc['id'].isin(gather.loc[line, 'id']))][['hour', 'id',
                                                                                              'lat', 'long']]
                        geometry = gpd.points_from_xy(gather_loc['long'], gather_loc['lat'])
                        gather1 = gpd.GeoDataFrame(gather_loc, geometry=geometry)
                        plot_map(abila)
                        ax = plt.subplot()
                        ax.set_aspect('equal')
                        gather1.plot(ax=ax, marker='o', c='id', cmap='tab20', markersize=5)
                        plt.savefig(file_path + 'Assignment2/Loc_Date/' + location + '_'
                                    + day[3:5] + '_' + str(gather.loc[line, 'hour']) + '.jpg')
                else:
                    print(location, ' ', day)
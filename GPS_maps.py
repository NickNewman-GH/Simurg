import h5py
import time
import pytz
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timezone

def get_sites(file):
    sites = [site for site in file]
    return sites

def get_sats(file, site):
    if site in file:
        sats = [sat for sat in file[site]]
    return sats

def get_data(file, site, sat, field):
    if site in file and sat in file[site]:
        times = file[site][sat][field][:]
    return times

def get_series(file, site, sat, field):
    ts = get_data(file, site, sat, 'timestamp')
    data = get_data(file, site, sat, field)
    return ts, data

def get_map(data, time, value):
    timestamp = time.timestamp()
    return np.array(data[int(int(timestamp) % 86400 / 30)])

def save_map_data(file, field):
    results = [[] for i in range(int(86400 / 30))]
    sites = get_sites(file)
    for site in sites:
        print(str(sites.index(site)/len(sites)*100) + '%', end='\r')
        lat = np.degrees(file[site].attrs['lat'])
        lon = np.degrees(file[site].attrs['lon'])
        sats = get_sats(file, site)
        for sat in sats:
            timestamps, data = get_series(file, site, sat, field)
            for i in range(len(timestamps)):
                results[int(int(timestamps[i]) % 86400 / 30)].append((data[i], lon, lat))
    return results

path_to_file = '2020-05-20.h5'
file = h5py.File(path_to_file, 'r')
field = 'dtec_20_60'
before = time.time()
data = save_map_data(file, field)
print(f'It took {time.time() - before} sec. to save map data')


time_hr_min_sec = [[12, 30, 0], [13, 30, 0], [14, 30, 0]]
for t in time_hr_min_sec:
    epoch = datetime(2020, 5, 20, t[0], t[1], t[2], tzinfo=timezone.utc)
    before = time.time()
    map = get_map(data, epoch, field)
    print(f'It took {time.time() - before} sec. to retrieve a map')

    val = map[:, 0]
    x = map[:, 1]
    y = map[:, 2]
    plt.scatter(x, y, c=val)
    plt.xlim(-180, 180)
    plt.ylim(-90, 90)
    plt.show()
from ee_downloader import SentinelDownloader
import random
from model import Coor


MAX_LAT = 0.8167
MIN_LAT = -6.7262
MAX_LONG = -67.6043
MIN_LONG = -53.5858
RECORD_NUM = 425

coors = []
for _ in range(RECORD_NUM):
    random_lat = random.uniform(MIN_LAT, MAX_LAT)
    random_long = random.uniform(MIN_LONG, MAX_LONG)
    coors.append(Coor(long=random_long, lat=random_lat))
    
print(coors)


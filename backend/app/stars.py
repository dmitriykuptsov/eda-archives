from geopy.geocoders import Nominatim
from skyfield.api import Star, load, Topos
from skyfield.data import hipparcos
from skyfield.api import Star
from skyfield.api import utc
import pandas as pd
import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import base64
import io
import matplotlib.pyplot as plt
import random
from datetime import datetime, timezone
import astroquery
from astroquery.simbad import Simbad

stars = pd.read_csv(
    "/storage/data/hip_main.dat",
    #"hip_main.dat",
    sep="|",
    header=None,
    skipinitialspace=True
)

hip_to_name_mag = [
    (32349, "Sirius", -1.46),
    (30438, "Canopus", -0.74),
    (69673, "Arcturus", -0.05),
    (91262, "Vega", 0.03),
    (24608, "Capella", 0.08),
    (24436, "Rigel", 0.12),
    (37279, "Procyon", 0.38),
    (27989, "Betelgeuse", 0.42),
    (7588, "Achernar", 0.46),
    (68702, "Hadar", 0.61),
    (71683, "Alpha Centauri", -0.27),
    (97649, "Altair", 0.77),
    (21421, "Aldebaran", 0.85),
    (80763, "Antares", 1.06),
    (113368, "Fomalhaut", 1.16),
    (65474, "Spica", 0.98),
    (37826, "Pollux", 1.14),
    (113881, "Deneb", 1.25),
    (102098, "Enif", 2.38),
    (54061, "Regulus", 1.35),
    (80763, "Antares", 1.06),
    (85927, "Shaula", 1.62),
    (28360, "Bellatrix", 1.64),
    (11767, "Mirfak", 1.79),
    (112158, "Markab", 2.49),
    (100453, "Alnair", 1.73),
    (102488, "Sadalmelik", 2.95),
    (113963, "Alpheratz", 2.06),
    (49669, "Alphard", 1.98),
    (2081, "Caph", 2.28),
    (15863, "Menkar", 2.54),
    (3419, "Ankaa", 2.40),
    (62434, "Menkent", 2.06),
    (17702, "Hamal", 2.00),
    (9640, "Schedar", 2.24),
    (107315, "Sadalsuud", 2.87),
    (21421, "Aldebaran", 0.85),
    (113136, "Deneb Algedi", 2.85),
    (109268, "Peacock", 1.94),
    (33579, "Alhena", 1.93),
    (72607, "Kaus Australis", 1.79),
    (25930, "Mintaka", 2.25),
    (26311, "Alnilam", 1.69),
    (26727, "Alnitak", 1.74),
    (100751, "Alsephina", 1.99),
    (45238, "Avior", 1.86),
    (41037, "Miaplacidus", 1.67),
    (31681, "Naos", 2.25),
    (39429, "Wezen", 1.83),
    (39953, "Adhara", 1.50),
]

stars = stars[[1, 5, 6, 8]]
stars.columns = ["hip", "ra_degrees", "dec_degrees", "magnitude"]
stars = stars.apply(pd.to_numeric, errors="coerce")

def get_stars():
    star_objects = []
    for _, row in stars.iterrows():
        if row['hip'] in [x[0] for x in hip_to_name_mag]:
            star = Star(ra_hours=float(row['ra_degrees']) / 15,
                        dec_degrees=float(row['dec_degrees']))
            for h, n, m in hip_to_name_mag:
                if h == row['hip']:
                    star_objects.append((star, n, row['magnitude']))
    return star_objects

def plot_stars(num, stars, date_str, lat, lng):
    planets = load('de421.bsp')
    location = Topos(latitude_degrees=lat, longitude_degrees=lng)
    earth = planets['earth']
    observer = earth + location
    x, y, names, mags = [], [], [], []
    counter = 1

    for star, name, mag in stars:
        for hour in range(18, 24):
            ts = load.timescale()
            t = datetime.strptime(date_str + f" {hour}:00:00", "%d.%m.%Y %H:%M:%S")
            t = t.replace(tzinfo=timezone.utc)
            t = ts.from_datetime(t)
            astrometric = observer.at(t).observe(star)
            alt, az, distance = astrometric.apparent().altaz()
            if alt.degrees > 0:
                x.append(az.degrees)
                y.append(alt.degrees)
                names.append(name)
                mags.append(mag)
                counter += 1
                break;
        if counter > num:
            break
    buf = io.BytesIO()
    #plt.figure(figsize=(10, 4))
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    ax.margins(0)

    ax.set_xlim(min(x) - 0.3, max(x) + 0.3)
    ax.set_ylim(min(y) - 0.3, max(y) + 0.3)

    img = mpimg.imread("/storage/templates/star.png")
    #img = mpimg.imread("star.png")

    for xi, yi, name, mag in zip(x, y, names, mags):
        print(f"DOING ....{xi} {yi}")
        x, y = xi, yi
        print(f"X={x}")
        print(f"Y={y}")
        print(f"mag={mag}")
        w, h = 0.2, 0.2   # size
        ax.imshow(img, extent=(x - w/2, x + w/2, y - h/2, y + h/2))
        ax.text(x, y, name, color="black", fontsize=18)
    plt.axis('off')
    #plt.savefig("/storage/data/test.png", format='png', dpi=1000, transparent=True, bbox_inches='tight', pad_inches=0)
    #plt.savefig("test.png", format='png', dpi=300, transparent=True)
    plt.savefig(buf, format='png', dpi=1000, transparent=True, bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def get_coordinates(location: str):
    geolocator = Nominatim(user_agent="eda-archives.com")
    location = geolocator.geocode(location)
    return (location.latitude, location.longitude)

#(lat, lng) = get_coordinates("Tashkent, Uzbekistan")
#print(lat)
#print(lng)
#stars = get_stars()
#plot_stars(5, stars, "18.12.1984", lat, lng)

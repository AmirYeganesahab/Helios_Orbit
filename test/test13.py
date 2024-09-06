import matplotlib.pyplot as plt
import astropy.units as u
from astropy.coordinates import EarthLocation, SkyCoord
from pytz import timezone
from astropy.time import Time

from astroplan import Observer
from astroplan import FixedTarget
from astroplan.plots import plot_sky

# Set up Observer, Target and observation time objects.
longitude = '-155d28m48.900s'
latitude = '+19d49m42.600s'
elevation = 4163 * u.m
location = EarthLocation.from_geodetic(longitude, latitude, elevation)

observer = Observer(name='Subaru Telescope',
               location=location,
               pressure=0.615 * u.bar,
               relative_humidity=0.11,
               temperature=0 * u.deg_C,
               timezone=timezone('US/Hawaii'),
               description="Subaru Telescope on Maunakea, Hawaii")

coordinates = SkyCoord('02h31m49.09s', '+89d15m50.8s', frame='icrs')
polaris = FixedTarget(name='Polaris', coord=coordinates)
polaris_style = {'color': 'k'}

coordinates = SkyCoord('19h50m47.6s', '+08d52m12.0s', frame='icrs')
altair = FixedTarget(name='Altair', coord=coordinates)

coordinates = SkyCoord('18h36m56.5s', '+38d47m06.6s', frame='icrs')
vega = FixedTarget(name='Vega', coord=coordinates)
vega_style = {'color': 'g'}

coordinates = SkyCoord('20h41m25.9s', '+45d16m49.3s', frame='icrs')
deneb = FixedTarget(name='Deneb', coord=coordinates)
deneb_style = {'color': 'r'}

# Note that this is not a scalar.
observe_time = Time(['2000-03-15 15:30:00'])

plot_sky(polaris, observer, observe_time, style_kwargs=polaris_style)
plot_sky(altair, observer, observe_time)
plot_sky(vega, observer, observe_time, style_kwargs=vega_style)
plot_sky(deneb, observer, observe_time, style_kwargs=deneb_style)

# Note that you don't need this code block to produce the plot.
# It reduces the plot size for the documentation.
ax = plt.gca()
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height * 0.75])

plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5))
plt.tight_layout()
plt.show()
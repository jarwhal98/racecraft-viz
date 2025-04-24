import fastf1
from fastf1 import plotting
from fastf1.core import Laps

# Enable cache (faster data access)
fastf1.Cache.enable_cache('cache')  # creates a "cache" folder

# Load a session (2024 British GP Qualifying)
session = fastf1.get_session(2024, 'Silverstone', 'R')
session.load()

# Get all laps
laps = session.laps

# Show best lap per driver
fastest_laps = laps.pick_quicklaps().pick_fastest()
print(fastest_laps[['Driver', 'Team', 'LapTime']])
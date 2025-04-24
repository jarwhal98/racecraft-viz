import fastf1
import pandas as pd
import plotly.express as px

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')

# Load race session
session = fastf1.get_session(2024, 'Silverstone', 'R')
session.load()

# Pick quick laps
laps = session.laps.pick_quicklaps()
fastest_laps_idx = laps.groupby("Driver")["LapTime"].idxmin()
laps_df = laps.loc[fastest_laps_idx][['Driver', 'Team', 'LapTime']].copy()
laps_df['LapTime (s)'] = laps_df['LapTime'].dt.total_seconds()

# Sort by lap time (fastest first)
laps_df = laps_df.sort_values('LapTime (s)', ascending=True)
driver_order = laps_df['Driver'].tolist()

# Zoom in on lap time range
min_lap = laps_df['LapTime (s)'].min()
max_lap = laps_df['LapTime (s)'].max()
margin = 0.5  # zoom margin in seconds
x_range = [min_lap - margin, max_lap + margin]

# Official F1 team colors
TEAM_COLORS = {
    'Red Bull Racing': '#1E41FF',
    'Ferrari': '#DC0000',
    'Mercedes': '#00D2BE',
    'McLaren': '#FF8700',
    'Aston Martin': '#006F62',
    'Alpine': '#0090FF',
    'Williams': '#005AFF',
    'Haas F1 Team': '#B6BABD',
    'Kick Sauber': '#52E252',
    'RB': '#6692FF',
}

# Plot horizontal bar chart
fig = px.bar(
    laps_df,
    y='Driver',
    x='LapTime (s)',
    color='Team',
    color_discrete_map=TEAM_COLORS,
    category_orders={'Driver': driver_order},
    orientation='h',
    title='Fastest Lap per Driver - 2024 British GP (Zoomed)',
    hover_data=['LapTime', 'Team']
)

fig.update_layout(
    xaxis_title='Lap Time (seconds)',
    yaxis_title='Driver',
    xaxis_range=x_range,
    bargap=0.2,
    height=700,
)

fig.show()
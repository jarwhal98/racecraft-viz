import fastf1
import pandas as pd
import plotly.express as px

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')

# Load the race session
session = fastf1.get_session(2024, 'Silverstone', 'R')
session.load()

# Get quick laps and fastest lap per driver
laps = session.laps.pick_quicklaps()
fastest_laps_idx = laps.groupby("Driver")["LapTime"].idxmin()
laps_df = laps.loc[fastest_laps_idx][['Driver', 'Team', 'LapTime']].copy()
laps_df['LapTime (s)'] = laps_df['LapTime'].dt.total_seconds()

# Get total race laps and last lap per driver
total_laps = session.total_laps
last_laps = session.laps.groupby('Driver')['LapNumber'].max().reset_index()
last_laps.rename(columns={'LapNumber': 'LastLap'}, inplace=True)

# Get race results (Status info)
results = session.results[['Abbreviation', 'Position', 'Status']]

# Merge last laps and results into laps_df
laps_df = laps_df.merge(last_laps, on='Driver', how='left')
laps_df = laps_df.merge(results, left_on='Driver', right_on='Abbreviation', how='left')

# Define statuses that count as DNFs
dnf_keywords = ['Accident', 'Mechanical', 'Collision', 'Water', 'DNF', 'Retired', 'Electrical', 'Power', 'Hydraulic']

# Mark DNF if status contains one of those keywords
def is_dnf(status):
    if not isinstance(status, str):
        return False
    return any(keyword.lower() in status.lower() for keyword in dnf_keywords)

laps_df['DNF'] = laps_df['Status'].apply(lambda x: '❌ DNF' if is_dnf(x) else '')

# Add hover info for DNF lap if driver didn't finish
laps_df['DNF Lap Info'] = laps_df.apply(
    lambda row: f"❌ DNF on Lap {row['LastLap']} of {total_laps}" if is_dnf(row['Status']) else '',
    axis=1
)

# Find delta to session’s fastest lap
fastest_lap_time = laps_df['LapTime (s)'].min()
laps_df['Delta to Fastest (s)'] = laps_df['LapTime (s)'] - fastest_lap_time

# Sort by delta (fastest first)
laps_df = laps_df.sort_values('Delta to Fastest (s)', ascending=False)
driver_order = laps_df['Driver'].tolist()

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

# Stroke color = always full-opacity team color
laps_df['StrokeColor'] = laps_df['Team'].map(TEAM_COLORS).fillna('#888888')

# Lighten team color for DNFs using 50% opacity HEX
def hex_to_rgba(hex_color, alpha=1.0):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return f'rgba({r}, {g}, {b}, {alpha})'

def get_bar_color(team, status):
    base_hex = TEAM_COLORS.get(team, '#888888')
    alpha = 0.4 if is_dnf(status) else 1.0  # Use same DNF logic here
    return hex_to_rgba(base_hex, alpha)

laps_df['BarColor'] = laps_df.apply(
    lambda row: get_bar_color(row['Team'], row['Status']),
    axis=1
)



# Plot: bar chart with delta to fastest lap
import plotly.graph_objects as go

fig = go.Figure()

for _, row in laps_df.iterrows():
    fig.add_trace(go.Bar(
        y=[row['Driver']],
        x=[row['Delta to Fastest (s)']],
        name=row['Driver'],
        orientation='h',
        marker=dict(
            color=row['BarColor'],  # your dimmed fill
            line=dict(
                color='red' if is_dnf(row['Status']) else 'rgba(0,0,0,0)',
                width=1 if is_dnf(row['Status']) else 0
            )
        ),
        hovertemplate=(
            f"<b>{row['Driver']}</b><br>" +
            f"Team: {row['Team']}<br>" +
            f"Lap Time: {row['LapTime']}<br>" +
            f"Delta: {row['Delta to Fastest (s)']:.3f}s<br>" +
            f"Status: {row['Status']}<br>" +
            f"{row['DNF Lap Info']}<extra></extra>"
        )
    ))


fig.update_layout(
    title='Lap Time Delta to Fastest Lap - 2024 British GP',
    xaxis_title='Delta to Fastest Lap (s)',
    yaxis_title='Driver',
    yaxis=dict(categoryorder='array', categoryarray=driver_order),
    bargap=0.2,
    height=700,
    showlegend=False
)

fig.show()
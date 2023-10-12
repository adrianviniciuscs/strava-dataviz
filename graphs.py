import pandas as pd
import requests
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource

with open('token.txt', 'r') as file:
    authorization_token = file.read().strip()

url = 'https://www.strava.com/api/v3/athlete/activities?per_page=30'
headers = {
    'accept': 'application/json',
    'authorization': f'Bearer {authorization_token}'
}

response = requests.get(url, headers=headers)


data = response.json()


df = pd.DataFrame(data)
columns_to_drop = ['athlete_count', 'workout_type', 'athlete', 'resource_state', 'type','kudos_count', 'comment_count', 'has_kudoed', 'total_photo_count', 'from_accepted_tag', 'external_id', 'upload_id_str', 'display_hide_heartrate_option',
'heartrate_opt_out', 'has_heartrate', 'end_latlng', 'start_latlng', 'gear_id', 'flagged', 'visibility', 'manual', 'private', 'trainer', 'commute', 'map', 'photo_count', 'upload_id'                 
]
df = df.drop(columns=columns_to_drop)
df['start_date_local'] = pd.to_datetime(df['start_date_local'])

source = ColumnDataSource(data=dict(distance=df['distance'], elevation_gain=df['total_elevation_gain']))

p1 = figure(title="Elevation Gain vs. Distance", x_axis_label='Distance (in meters)', y_axis_label='Elevation Gain (in meters)')

p1.circle('distance', 'elevation_gain', source=source, size=8, color='blue', alpha=0.5)

source = ColumnDataSource(data=dict(elev_high=df['elev_high'], avg_speed=df['average_speed']))

p2 = figure(title="Average Speed vs. Elevation High", x_axis_label='Elevation High (in meters)', y_axis_label='Average Speed (in m/s)')

p2.circle('elev_high', 'avg_speed', source=source, size=8, color='red', alpha=0.5)

source = ColumnDataSource(data=dict(max_speed=df['max_speed'], elevation_gain=df['total_elevation_gain']))

p3 = figure(title="Max Speed vs. Total Elevation Gain", x_axis_label='Max Speed (in m/s)', y_axis_label='Elevation Gain (in meters)')

p3.circle('max_speed', 'elevation_gain', source=source, size=8, color='purple', alpha=0.5)

df['hour'] = df['start_date_local'].dt.hour
df['minute'] = df['start_date_local'].dt.minute

df['minute'] = df['minute'].apply(lambda x: 30 if x >= 30 else 0)

df['time_30min'] = df['hour'] + df['minute']/60

avg_distance_30min = df.groupby('time_30min')['distance'].mean().reset_index()

source = ColumnDataSource(data=dict(time_30min=avg_distance_30min['time_30min'], distance=avg_distance_30min['distance']))

p4 = figure(title="Time of Day vs. Average Distance", x_axis_label='Time of Day (in 30-minute intervals)', y_axis_label='Average Distance (in meters)')

p4.circle('time_30min', 'distance', source=source, size=8, color='green', alpha=0.5)

output_notebook()
grid = gridplot([[p1, p2], [p3, p4]], width=500, height=500)

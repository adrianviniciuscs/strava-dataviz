import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.embed import components


def plotGraphs(data): 
       
        #Loading data and deleting unimportant columns
        df = pd.DataFrame(data)
        columns_to_drop = ['athlete_count', 'workout_type', 'athlete', 
                           'resource_state', 'type','kudos_count', 'comment_count', 'has_kudoed', 
                           'total_photo_count', 'from_accepted_tag', 'external_id', 'upload_id_str', 
                           'display_hide_heartrate_option', 'heartrate_opt_out', 
                           'has_heartrate', 'end_latlng', 'start_latlng', 'gear_id', 'flagged', 'visibility', 'manual', 'private', 'trainer', 'commute', 'map', 'photo_count', 'upload_id'                 
                           ]
        df = df.drop(columns=columns_to_drop)
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])
        source = ColumnDataSource(data=dict(distance=df['distance'], elevation_gain=df['total_elevation_gain']))
        # Elevation Gain vs Distance Graph
        p1 = figure(title="Elevation Gain vs. Distance", x_axis_label='Distance (in meters)', y_axis_label='Elevation Gain (in meters)')

        p1.circle('distance', 'elevation_gain', source=source, size=8, color='blue', alpha=0.5)

        source = ColumnDataSource(data=dict(elev_high=df['elev_high'], avg_speed=df['average_speed']))

        # Average Speed vs Elevation High Graph
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

        p5 = figure(title="Average Speed Distribution", x_axis_label="Average Speed (m/s)", y_axis_label="Frequency", height=450)

        p5.quad(top=np.histogram(df['average_speed'], bins=20)[0], bottom=0, left=np.histogram(df['average_speed'], bins=20)[1][:-1], 
                right=np.histogram(df['average_speed'], bins=20)[1][1:], line_color="white", alpha=0.7)

        p6 = figure(title="Distance vs. Average Speed", x_axis_label="Distance (meters)", y_axis_label="Average Speed (m/s)", height=450)

        p6.circle(df['distance'], df['average_speed'], size=8, color='blue', alpha=0.5)
       

        plots = [p1, p2, p3, p4, p5, p6]
        titles = ["Elevation Gain vs. Distance",
              "Average Speed vs. Elevation High",
              "Max Speed vs. Total Elevation Gain",
              "Time of Day vs. Average Distance",
              "Average Speed Distribution",
              "Distance vs. Average Speed"]

        components_list = []

        for i in range(len(plots)):
            script, div = components(plots[i])
            components_list.append((script, div, titles[i]))
        return components_list

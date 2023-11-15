import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.embed import components


def plotGraphs(data):
    # Loading data and deleting unimportant columns
        df = pd.DataFrame(data)


        df['avg_pace'] = 1 / ((df['average_speed'] * 60) / 1000)
        df['max_pace'] = 1 / ((df['max_speed'] * 60) / 1000) 


        columns_to_drop = ['max_speed', 'average_speed', 'athlete_count', 'workout_type', 'athlete', 
                           'resource_state', 'type','kudos_count', 'comment_count', 'has_kudoed', 
                           'total_photo_count', 'from_accepted_tag', 'external_id', 'upload_id_str', 
                           'display_hide_heartrate_option', 'heartrate_opt_out', 
                           'has_heartrate', 'end_latlng', 'start_latlng', 'gear_id', 'flagged', 'visibility', 'manual', 'private', 'trainer', 'commute', 'map', 'photo_count', 'upload_id'                 
                           ]
        df = df.drop(columns=columns_to_drop)
        df['start_date_local'] = pd.to_datetime(df['start_date_local'])


        # Create a ColumnDataSource
        source = ColumnDataSource(data=dict(distance=df['distance'], elevation_gain=df['total_elevation_gain']))

        # Create a figure
        p1 = figure(title="Ganho de Elevação vs. Distância", x_axis_label='Distância (em metros)', y_axis_label='Ganho de Elevação (em metros)')

        # Add a circle glyph
        p1.circle('distance', 'elevation_gain', source=source, size=8, color='blue', alpha=0.5)

        # Create a ColumnDataSource
        source = ColumnDataSource(data=dict(elev_high=df['elev_high'], avg_pace=df['avg_pace']))


        # Create a figure
        p2 = figure(title="Velocidade Média vs. Elevação Máxima", x_axis_label='Elevação Máxima (em metros)', y_axis_label='Velocidade Média (pace, em km/min)')

        # Add a circle glyph
        p2.circle('elev_high', 'avg_pace', source=source, size=8, color='red', alpha=0.5)

        # Create a ColumnDataSource
        source = ColumnDataSource(data=dict(max_pace=df['max_pace'], elevation_gain=df['total_elevation_gain']))

        # Create a figure
        p3 = figure(title="Velocidade Máxima vs. Ganho de Elevação Total", x_axis_label='Velocidade Máxima (pace, em km/min)', y_axis_label='Ganho de Elevação (em metros)')

        # Add a circle glyph
        p3.circle('max_pace', 'elevation_gain', source=source, size=8, color='purple', alpha=0.5)

        # Extract hour and minute of day
        df['hour'] = df['start_date_local'].dt.hour
        df['minute'] = df['start_date_local'].dt.minute

        # Round minutes to the nearest 30
        df['minute'] = df['minute'].apply(lambda x: 30 if x >= 30 else 0)

        # Combine hour and minute to get time in 30-minute intervals
        df['time_30min'] = df['hour'] + df['minute']/60

        # Group by time in 30-minute intervals and calculate average distance
        avg_distance_30min = df.groupby('time_30min')['distance'].mean().reset_index()

        # Create a ColumnDataSource
        source = ColumnDataSource(data=dict(time_30min=avg_distance_30min['time_30min'], distance=avg_distance_30min['distance']))

        # Create a figure
        p4 = figure(title="Hora do Dia vs. Distância Média", x_axis_label='Hora do Dia (em intervalos de 30min)', y_axis_label='Distância Média (em metros)')

        # Add a circle glyph
        p4.circle('time_30min', 'distance', source=source, size=8, color='green', alpha=0.5)

        p5 = figure(title="Distribuição de Velocidade Média", x_axis_label="Velocidade Média (pace, em km/min)", y_axis_label="Frequência", height=450)

        p5.quad(top=np.histogram(df['avg_pace'], bins=20)[0], bottom=0, left=np.histogram(df['avg_pace'], bins=20)[1][:-1], 
        right=np.histogram(df['avg_pace'], bins=20)[1][1:], line_color="white", alpha=0.7)

        p6 = figure(title="Distância vs. Velocidade Média", x_axis_label="Distância (metros)", y_axis_label="Velocidade Média (pace, em km/min)", height=450)

        p6.circle(df['distance'], df['avg_pace'], size=8, color='blue', alpha=0.5)

        plots = [p1, p2, p3, p4, p5, p6]
        components_list = []

        for i in range(len(plots)):
            script, div = components(plots[i])
            components_list.append((script, div))
        return components_list

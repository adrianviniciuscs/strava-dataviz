import pandas as pd

# Creates a dataframe (and export it to CSV) using the data returned from the Strava API


def createCSV(data):
    df = pd.DataFrame(data)

    df['avg_pace'] = 1 / ((df['average_speed'] * 60) / 1000)
    df['max_pace'] = 1 / ((df['max_speed'] * 60) / 1000)

    columns_to_drop = ['max_speed', 'average_speed', 'athlete_count', 'workout_type', 'athlete',
                       'resource_state', 'type', 'kudos_count', 'comment_count', 'has_kudoed',
                       'total_photo_count', 'from_accepted_tag', 'external_id', 'upload_id_str',
                       'display_hide_heartrate_option', 'heartrate_opt_out',
                       'has_heartrate', 'end_latlng', 'start_latlng', 'gear_id', 'flagged', 'visibility', 'manual', 'private', 'trainer', 'commute', 'map', 'photo_count', 'upload_id'
                       ]
    df = df.drop(columns=columns_to_drop)
    df['start_date_local'] = pd.to_datetime(df['start_date_local'])
    df.to_csv("./data.csv", index=False)

    return df

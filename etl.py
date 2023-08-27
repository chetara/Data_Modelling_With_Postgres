import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def process_song_file(cur, filepath):  
    """
    Process songs files and insert records into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
     
    # open song file
    print("test")
    df = pd.DataFrame([pd.read_json(filepath, typ='series', convert_dates=False)])

    for value in df.values:
        # i used unpacking tuples that allows me to assign variables without access them one by one (assign multiples variable)
        num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year = value

        # insert artist record
        artist_data = (artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
        cur.execute(artist_table_insert, artist_data)

        # insert song record
        song_data = (song_id, title, artist_id, year, duration)
        cur.execute(song_table_insert, song_data)
    print(f"Records inserted for file {filepath}")

    

def process_log_file(cur, filepath):
    """
    Process Event log files and insert records into the Postgres database.
    :param cur: cursor reference
    :param filepath: complete file path for the file to load
    """
    try:
        # open log file
        df = pd.read_json(filepath, lines=True)

        # filter by NextSong action
        df = df[df['page'] == "NextSong"].astype({'ts': 'datetime64[ms]'})

        # convert timestamp column to datetime
        t = pd.Series(df['ts'], index=df.index)
        
        # insert time data records
        column_labels = ["timestamp", "hour", "day", "weelofyear", "month", "year", "weekday"]
        time_data = []
        for data in t:
            time_data.append([data ,data.hour, data.day, data.weekofyear, data.month, data.year, data.day_name()])

        time_df = pd.DataFrame.from_records(data=time_data, columns=column_labels)
        
        for i, row in time_df.iterrows():
            # The list(row) call converts the data in the current row to a list format that can be 
            # used to supply values to the placeholders in the SQL query.
            cur.execute(time_table_insert, list(row))

        # load user table
        user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

        # insert user records
        for i, row in user_df.iterrows():
            cur.execute(user_table_insert, row)
            
        # fact table : insert songplay records
        for index, row in df.iterrows():
            # get songid and artistid from song and artist tables
            params = (row.song, row.artist, row.length)
            print("Query Parameters:", params)  # Print the parameters before executing the query
            cur.execute(song_select, params)
            results = cur.fetchone()
            
            if results:
                song_id, artist_id = results
            else:
                song_id, artist_id = None, None
            print("Results of song_select query:", results, " | Length:", row.length)
            # insert songplay record
            songplay_data = (row.ts, row.userId, row.level, song_id, artist_id, row.sessionId, row.location, row.userAgent)
            cur.execute(songplay_table_insert, songplay_data)
    
    except Exception as e:
        print("An error occurred:", str(e))


def process_data(cur, conn, filepath, func):
    """
    Driver function to load data from songs and event log files into Postgres database.
    :param cur: a database cursor reference
    :param conn: database connection reference
    :param filepath: parent directory where the files exists
    :param func: function to call
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Driver function for loading songs and log data into Postgres database
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=music user=postgres password=chetara1995")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
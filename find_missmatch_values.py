import os
import glob
import pandas as pd

def compare_data():
    """
    Compare song and artist data between JSON files and log data.
    """
    # Get unique song and artist information from JSON files
    unique_json_songs = set()
    unique_json_artists = set()

    json_files = glob.glob('data/song_data/{A,B}/*.json')  # Replace with the actual path to your JSON files
    for filepath in json_files:
        df = pd.read_json(filepath, lines=True)
        for index, row in df.iterrows():
            unique_json_songs.add(row.title)
            unique_json_artists.add(row.artist_name)

    # Get unique song and artist information from log data
    unique_log_songs = set()
    unique_log_artists = set()

    log_files = glob.glob('data/log_data/*.json')  # Replace with the actual path to your log data files
    for filepath in log_files:
        df = pd.read_json(filepath, lines=True)
        for index, row in df.iterrows():
            if row.page == 'NextSong':
                unique_log_songs.add(row.song)
                unique_log_artists.add(row.artist)

    # Compare the unique song and artist information
    missing_songs = unique_log_songs - unique_json_songs
    missing_artists = unique_log_artists - unique_json_artists

    print("Missing songs in JSON files:")
    print(missing_songs)

    print("\nMissing artists in JSON files:")
    print(missing_artists)

def main():
    """
    Main function for troubleshooting song and artist data consistency.
    """
    compare_data()

if __name__ == "__main__":
    main()

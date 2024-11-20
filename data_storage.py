import csv
from typing import List, Dict, Union

class DataStorage:
    def __init__(self):
        self.library_path = "storage/music_library.csv"
        self.playlists_path = "storage/playlists.csv"
        self.queue_path = "storage/queue.csv"

    def read_csv(self, filepath: str) -> List[Dict[str, str]]:
        """Read data from a CSV file."""
        try:
            with open(filepath, mode="r", newline="") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    def write_csv(self, filepath: str, data: List[Dict[str, Union[str, int]]], fieldnames: List[str]):
        """Write data to a CSV file."""
        with open(filepath, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    # Music Library Operations
    def load_music_library(self) -> List[Dict[str, str]]:
        """Load tracks from the music library."""
        return self.read_csv(self.library_path)

    def save_music_library(self, tracks: List[Dict[str, str]]):
        """Save tracks to the music library."""
        fieldnames = ["Title", "Artist", "Album", "Duration"]
        self.write_csv(self.library_path, tracks, fieldnames)

    # Playlist Operations
    def load_playlists(self) -> List[Dict[str, str]]:
        """Load playlists."""
        return self.read_csv(self.playlists_path)

    def save_playlists(self, playlists: List[Dict[str, str]]):
        """Save playlists."""
        fieldnames = ["Name", "Tracks"]  # Tracks stored as comma-separated values
        self.write_csv(self.playlists_path, playlists, fieldnames)

    # Queue Operations
    def load_queue(self) -> List[Dict[str, str]]:
        """Load the playback queue."""
        return self.read_csv(self.queue_path)

    def save_queue(self, queue: List[Dict[str, str]]):
        """Save the playback queue."""
        fieldnames = ["Title", "Artist", "Album", "Duration"]
        self.write_csv(self.queue_path, queue, fieldnames)

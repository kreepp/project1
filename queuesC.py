import random
from Tracks import Tracks
from Playlist import Playlist
import json

class Queue:
    def __init__(self):
        self.tracks = []
        self.current_index = 0
        self.is_repeat = False
        self.is_shuffled = False
        self.original_order = []  # To preserve the original order when shuffling

    def enqueue(self, track: Tracks):
        """Adds a track to the queue."""
        self.tracks.append(track)
        if not self.is_shuffled:
            self.original_order.append(track)

    def enqueue_playlist(self, playlist: Playlist):
        """Adds all tracks from a playlist to the queue."""
        for track in playlist.tracks:
            self.enqueue(track)

    def dequeue(self):
        """Removes the current track from the queue."""
        if self.tracks:
            self.tracks.pop(self.current_index)
            self.original_order = self.tracks.copy()
            self.current_index = min(self.current_index, len(self.tracks) - 1)

    def toggle_repeat(self):
        """Toggles the repeat state."""
        self.is_repeat = not self.is_repeat

    def shuffle_queue(self):
        """Shuffles the queue but preserves the original order."""
        if not self.is_shuffled:
            random.shuffle(self.tracks)
            self.is_shuffled = True
        else:
            self.tracks = self.original_order.copy()
            self.is_shuffled = False

    def next_track(self):
        """Moves to the next track in the queue."""
        if not self.tracks:
            return None

        self.current_index += 1
        if self.current_index >= len(self.tracks):
            if self.is_repeat:
                self.current_index = 0
            else:
                self.current_index -= 1  # Stay at the last track
                return None

        return self.tracks[self.current_index]

    def previous_track(self):
        """Moves to the previous track in the queue."""
        if not self.tracks:
            return None

        self.current_index -= 1
        if self.current_index < 0:
            if self.is_repeat:
                self.current_index = len(self.tracks) - 1
            else:
                self.current_index += 1  # Stay at the first track
                return None

        return self.tracks[self.current_index]

    def display_queue(self, page=1, items_per_page=10):
        """Displays the queue with pagination."""
        start = (page - 1) * items_per_page
        end = start + items_per_page

        current_track = self.tracks[self.current_index] if self.tracks else None
        tracks_to_display = self.tracks[start:end]

        print(f"\nQueue (Page {page}):")
        print(f"Repeat: {'On' if self.is_repeat else 'Off'}")
        print(f"Shuffled: {'Yes' if self.is_shuffled else 'No'}")
        print(f"Currently Playing: {current_track.getTitle() if current_track else 'None'}\n")

        for i, track in enumerate(tracks_to_display, start=start + 1):
            print(f"{i}. {track.getTitle()} - {track.getArtist()} ({track.getDuration()})")

        print(f"\n<Page {page} of {len(self.tracks) // items_per_page + 1}>")

    def save_queue(self, filename="QueueState.json"):
        """Saves the current queue to a file."""
        with open(filename, "w") as f:
            data = {
                "tracks": [track.newTrack for track in self.tracks],
                "current_index": self.current_index,
                "is_repeat": self.is_repeat,
                "is_shuffled": self.is_shuffled,
            }
            json.dump(data, f, indent=4)

    def load_queue(self, filename="QueueState.json"):
        """Loads a queue from a file."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)

            self.tracks = [Tracks(**track) for track in data["tracks"]]
            self.original_order = self.tracks.copy()
            self.current_index = data["current_index"]
            self.is_repeat = data["is_repeat"]
            self.is_shuffled = data["is_shuffled"]

            if self.is_shuffled:
                random.shuffle(self.tracks)
        except FileNotFoundError:
            print("No saved queue found.")

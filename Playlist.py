import json
from Tracks import Tracks

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.total_duration = [0, 0]  # [minutes, seconds]

    def add_track(self, track: Tracks):
        """Add a unique track to the playlist."""
        if track not in self.tracks:
            self.tracks.append(track)
            self._update_duration(track.getNumericDuration())
            self.save_playlist()
            return True
        return False

    def remove_track(self, track: Tracks):
        """Remove a track from the playlist."""
        if track in self.tracks:
            self.tracks.remove(track)
            self._update_duration(track.getNumericDuration(), remove=True)
            self.save_playlist()
            return True
        return False

    def _update_duration(self, duration, remove=False):
        """Update the total duration of the playlist."""
        minutes, seconds = self.total_duration
        delta_min, delta_sec = duration

        total_seconds = minutes * 60 + seconds
        delta_seconds = delta_min * 60 + delta_sec
        total_seconds = total_seconds - delta_seconds if remove else total_seconds + delta_seconds

        self.total_duration = [total_seconds // 60, total_seconds % 60]

    def get_total_duration(self):
        """Return the total duration in 'mm:ss' format."""
        return f"{self.total_duration[0]:02}:{self.total_duration[1]:02}"

    def save_playlist(self):
        """Save the playlist to Playlist.json."""
        try:
            with open("Playlist.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data[self.name] = {
            "Playlist Name": self.name,
            "Total Duration": f"{self.total_duration[0]} min {self.total_duration[1]} sec",
            "Tracks": [track.newTrack for track in self.tracks]
        }

        with open("Playlist.json", "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_playlist(name):
        """Load a playlist by name from Playlist.json."""
        try:
            with open("Playlist.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No saved playlists found.")
            return None

        if name in data:
            playlist_data = data[name]
            playlist = Playlist(playlist_data["Playlist Name"])
            playlist.tracks = [
                Tracks(
                    title=track_data["Title"],
                    artist=track_data["Artist"],
                    album=track_data["Album"],
                    duration=track_data["Duration"]
                )
                for track_data in playlist_data["Tracks"]
            ]
            total_duration = playlist_data["Total Duration"].split(" min ")
            playlist.total_duration = [int(total_duration[0]), int(total_duration[1].replace(" sec", ""))]
            return playlist
        else:
            print(f"Playlist '{name}' not found.")
            return None

    def __str__(self):
        """Return a string representation of the playlist."""
        track_list = "\n".join([str(track) for track in self.tracks])
        return f"Playlist: {self.name}\nTotal Duration: {self.get_total_duration()}\nTracks:\n{track_list}"
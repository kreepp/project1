import json
import random

class Tracks:
    def __init__(self, title, artist, album, duration, additional_artists=None):
        self.__title = title
        self.__artist = artist 
        self.__album = album 
        self.__duration = duration
        self.__additional_artists = additional_artists if additional_artists is not None else []

        self.newTrack = {
        "Title": self.__title,
        "Artist": self.__artist,
        "Additional Artists": self.__additional_artists,
        "Album": self.__album,
        "Duration": self.__duration
        }

    def getTitle(self) -> str:
        """
            returns track title
        """
        return self.__title
    
    def getArtist(self) -> str:
        """Returns a formatted string of the primary artist and additional artists."""
        if self.__additional_artists:
            # Join all artists into a single string
            artists = [self.__artist] + self.__additional_artists
            return ", ".join(artists)
        else:
            return self.__artist
    
    def addAdditionalArtist(self, artist: str):
        """
            Add an additional artist to the track.
        """
        if artist not in self.__additional_artists:
            self.__additional_artists.append(artist)
    
    def getAlbumName(self) -> str:
        """
            returns track album name
        """
        return self.__album
    
    def getDuration(self) -> str:
        """
            returns track str duration
        """
        return self.__duration

    def getNumericDuration(self):
        """
            returns track duration in list form integers
        """
        #mm:ss
        colon = self.getDuration().index(":")
        minutes = int(self.getDuration()[0:colon])
        seconds = int(self.getDuration()[colon+1:])
        return [minutes, seconds]   

    def CompareTrack(track1: 'Tracks', track2: 'Tracks', comparison: int=0):
        """Compares the names of two different contacts. 
        
        Args:
            c1 (Contact): Contact 1
            c2 (Contact): Contact 2
            comparison_type (int): 0 to compare last names. 1 to compare first names. Defaults to 0.
 
        Returns:
            int: 1 if name value of c1 > c2.
            0 if both contacts have same name value.
            -1 if name value of c1 < c2.
        """

        """
                - using the logical comparison operator

                - True is 1
                - False is 0

                - returns 1 if (c1 name value > c2 name value) is True since 1 - 0 == 1
                on the other hand
                - returns -1 if (c1 name value < c2 name value) is True since 1 - 0 == 1
                - return 0 if they are both false since 0 - 0 == 0
        """

        #compare last names
        if comparison == 0:
            return (track1.getTitle()> track2.getTitle()) - (track1.getTitle()< track2.getTitle())
        #compare first names
        elif comparison == 1:
            return (track1.getArtist()> track2.getArtist()) - (track1.getArtist() < track2.getArtist())
        elif comparison == 2:
            return (track1.getAlbumName()> track2.getAlbumName()) - (track1.getAlbumName() < track2.getAlbumName())
        elif comparison == 3:
            return (track1.getNumericDuration()[0]> track2.getNumericDuration()[0]) - (track1.getNumericDuration()[0] < track2.getNumericDuration()[0])
        return -1

    def __str__(self):
        return f"\n\tTitle: {self.getTitle()}"\
               f"\n\tArtist(s): {self.getArtist()}"\
               f"\n\tAlbum: {self.getAlbumName()}"\
               f"\n\tDuration: {self.getDuration()}"

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

class MusicLibrary:
    def __init__(self):
        self.__library = []
        self.loadLibrary()

    def loadLibrary(self):
        with open("MusicLibrary.json", "r") as f:
            data = json.loads(f.read())

        # for i in range(0, len(data)):
        #     self.getMusicLibrary().append(Tracks(data[i]["Title"],data[i]["Artist"],data[i]["Album"],data[i]["Duration"]))
        for track_data in data:
            self.getMusicLibrary().append(
                Tracks(
                    track_data["Title"],
                    track_data["Artist"],
                    track_data["Album"],
                    track_data["Duration"],
                    track_data.get("Additional Artists", [])  # Default to empty list
                )
            )

    def getMusicLibrary(self) -> list:
        return self.__library

    def isEmpty(self) -> bool:
        return len(self.getMusicLibrary()) == 0

    def getSize(self):
        return len(self.getMusicLibrary())
    
    def getFirst(self):
        return self.getMusicLibrary()[0] if not self.isEmpty() else None
    
    def getLast(self):
        return self.getMusicLibrary()[-1] if not self.isEmpty() else None
    
    def insertTrackToLibrary(self, track: Tracks):
        index = self.findIndexInsertion(track)
        self.getMusicLibrary().insert(index, track)

        data = []
        for track in self.getMusicLibrary():
            if track.newTrack not in data:
                data.append(track.newTrack)
        with open("MusicLibrary.json", "w") as f:
            newjson = json.dumps(data, indent=4)
            f.write(newjson)

    def findIndexInsertion(self, track: Tracks):
        left = 0
        right = self.getSize() - 1
        
        while left <= right:
            mid = (left + right) // 2
            existing_contact = self.getMusicLibrary()[mid]

            #comparing the titles of the tracks to be stored and the existing contact
            compare_result = Tracks.CompareTrack(track,existing_contact,0)

            #if new tracks title is less than the existing tracks title
            if compare_result < 0:
                right = mid - 1
            
            #if new tracks title is greater than the existing tracks title
            elif compare_result > 0:
                left = mid + 1

            else:
                #if titles are equal, then we will compare the artist Names
                compare_result = Tracks.CompareTrack(track,existing_contact,1)

                if compare_result < 0:
                    right = mid - 1
            
                
                elif compare_result > 0:
                    left = mid + 1

                else:
                    compare_result = Tracks.CompareTrack(track,existing_contact,2)
                    
                    if compare_result < 0:
                        right = mid - 1
                    
                    elif compare_result > 0:
                        left = mid + 1

                    else:
                        compare_result = Tracks.CompareTrack(track,existing_contact,3)
                        if compare_result < 0:
                            right = mid - 1

                        else: 
                            left = mid + 1

        return left
    
    def getTrack(self, trackTitle) -> list['Tracks']:
        """
            Finding all tracks with title that matches with the given track title.
            Using binary search to narrow the search range and then performs a linear scan to collect all matching tracks.

            Returns:
                list[Tracks]: A list of tracks with the matching title.
                to be able to handle cases where there are multiple tracks that have same track title
        """
        if self.isEmpty():
            return result
        
        left = 0
        right = self.getSize() - 1
        lib = self.getMusicLibrary() 
        result = []

        while left <= right:
            mid = (left + right) // 2
            midTitle = lib[mid].getTitle().strip().lower()
            targetTitle = trackTitle.strip().lower()

            if midTitle > targetTitle:
                right = mid - 1
            elif midTitle < targetTitle:
                left = mid + 1
            else:
                # Match found, now reduce the search range
                break

        # If no match is found during binary search
        if left > right:
            return result

        # Linear scan backward to find all matching titles before mid
        start = mid
        while start >= 0 and lib[start].getTitle().strip().lower() == trackTitle.strip().lower():
            start -= 1

        # Linear scan forward to find all matching titles after mid
        end = mid
        while end < len(lib) and lib[end].getTitle().strip().lower() == trackTitle.strip().lower():
            end += 1

        # Collect all matching tracks
        result.extend(lib[start + 1:end])

        return result
 
             
    def searchTrack(self, trackTitle) -> int:
        left = 0
        right = len(self.getMusicLibrary()) - 1
        lib = self.getMusicLibrary()
        while left <= right:
            mid = (left + right) // 2

            if lib[mid].getTitle().strip().lower() > trackTitle.strip().lower():
                right = mid - 1
            elif lib[mid].getTitle().strip().lower() < trackTitle.strip().lower():
                left = mid + 1
            elif lib[mid].getTitle().strip().lower() == trackTitle.strip().lower():
                return mid
        return -1

def validate_duration(duration: str) -> bool:
    """
    Validates the track duration format as mm:ss and checks for reasonable values.
    """
    try:
        minutes, seconds = map(int, duration.split(":"))
        return 0 <= minutes and 0 <= seconds < 60
    except:
        return False

def receiveTrackInfo() -> Tracks:
    """
    Cast several prompts for user to input about the Tracks data.
    Includes validation for duration.
    Returns:
       Tracks: Tracks object created based on data.
    """
    title = input("Enter track title: ").strip()
    artist = input("Enter artist: ").strip()
    album = input("Enter album: ").strip()

    while True:
        duration = input("Enter duration (mm:ss): ").strip()
        if validate_duration(duration):
            break
        else:
            print("Invalid duration format. Please use mm:ss with seconds less than 60.")

    additional_artists_input = input("Enter additional artists (comma-separated, or 'None'): ").strip()
    additional_artists = (additional_artists_input.split(",") if additional_artists_input.lower() != "none" else [])
    return Tracks(title, artist, album, duration, additional_artists)

MENUS = {
    "main": {
        1: "View Music Library",
        2: "Search Track",
        3: "Add Track",
        4: "Manage Playlists",
        5: "Manage Queue",
        6: "Exit"
    },
    "playlist": {
        1: "Create Playlist",
        2: "View Playlists",
        3: "Delete Playlist",
        4: "Add Track to Playlist",
        5: "Remove Track from Playlist",
        6: "Back to Main Menu"
    },
    "queue": {
        1: "Add Track to Queue",
        2: "Add Playlist to Queue",
        3: "Shuffle Queue",
        4: "Toggle Repeat",
        5: "Next Track",
        6: "Previous Track",
        7: "View Queue",
        8: "Save and Exit Queue"
    }
}

def showMenu(menu_name):
    """
    Displays the menu based on the provided name.
    """
    print("\n<----- Menu ----->")
    for key, value in MENUS[menu_name].items():
        print(f"[{key}] {value}")

def mainMenu():
    """
    Entry point for the program: displays the main menu.
    """
    library = MusicLibrary()
    queue = Queue()

    while True:
        showMenu("main")
        try:
            choice = int(input("Select Operation: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            viewMusicLibrary(library)
        elif choice == 2:
            searchTrack(library)
        elif choice == 3:
            addTrack(library)
        elif choice == 4:
            managePlaylists(library)
        elif choice == 5:
            manageQueue(queue, library)
        elif choice == 6:
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

def viewMusicLibrary(library):
    print("\n<----- Music Library ----->")
    if library.isEmpty():
        print("The music library is empty.")
    else:
        for track in library.getMusicLibrary():
            print(track)

def searchTrack(library):
    title = input("Enter track title to search: ")
    results = library.getTrack(title)
    if not results:
        print(f"No tracks found for '{title}'.")
    else:
        print("\nSearch Results:")
        for track in results:
            print(track)

def addTrack(library):
    track = receiveTrackInfo()
    library.insertTrackToLibrary(track)
    print("Track added successfully!")

def display_playlist_details(playlist_data):
    """
    Displays the details of a selected playlist.

    Args:
        playlist_data (dict): Details of the playlist, including tracks, total duration, etc.
    """
    print(f"\nPlaylist Name: {playlist_data['Playlist Name']}")
    print(f"Total Duration: {playlist_data['Total Duration']}")
    print("Tracks:")
    for track in playlist_data["Tracks"]:
        title = track["Title"]
        artist = track["Artist"]
        duration = track["Duration"]
        print(f"    {title} – {artist} ({duration})")
    print("\n")

def display_playlists_with_pagination(playlists, page=1, items_per_page=10):
    """
    Displays the list of playlists with pagination.

    Args:
        playlists (list[str]): List of playlist names.
        page (int): Current page number.
        items_per_page (int): Number of playlists to display per page.
    """
    total_playlists = len(playlists)
    total_pages = (total_playlists + items_per_page - 1) // items_per_page  # Ceiling division

    # Validate and adjust the current page
    page = max(1, min(page, total_pages))

    # Calculate the range of playlists to display
    start_index = (page - 1) * items_per_page
    end_index = min(start_index + items_per_page, total_playlists)
    playlists_to_display = playlists[start_index:end_index]

    print("\n<----- List of Playlists ----->")
    for idx, playlist in enumerate(playlists_to_display, start=start_index + 1):
        print(f"[{idx}] {playlist}")

    print(f"\n<Page {page} of {total_pages}>")
    print("[11] Previous Page")
    print("[12] Next Page")
    print("[0] Exit to Main Menu")

    return page, total_pages  # Return current state to handle navigation

def managePlaylists(library):
    while True:
        showMenu("playlist")
        choice = int(input("Select Operation: "))

        if choice == 1:
            name = input("Enter playlist name: ")
            if Playlist.load_playlist(name):
                print("Playlist with this name already exists.")
            else:
                playlist = Playlist(name)
                playlist.save_playlist()
                print(f"Playlist '{name}' created successfully!")

        elif choice == 2:
            """
            Handles playlist management with pagination and details display functionality.
            """
            try:
                with open("Playlist.json", "r") as f:
                    data = json.load(f)  # Load JSON data
                playlists = list(data.keys())  # Extract playlist names
            except FileNotFoundError:
                print("No playlists found.")
                return
            except json.JSONDecodeError:
                print("Error decoding Playlist.json file.")
                return

            page = 1
            while True:
                page, total_pages = display_playlists_with_pagination(playlists, page)

                # Add "Search Playlist" as an option
                print("[13] Search Playlist")
                print("[0] Exit to Main Menu")

                # Navigation and details logic
                try:
                    choice = int(input("Select an option: "))
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue

                if choice == 0:
                    break
                elif choice == 11 and page > 1:  # Previous page
                    page -= 1
                elif choice == 12 and page < total_pages:  # Next page
                    page += 1
                elif choice == 13:  # Search Playlist
                    search_query = input("Enter playlist name to search: ").strip()
                    matching_playlists = [name for name in playlists if search_query.lower() in name.lower()]
                    if matching_playlists:
                        print("\nSearch Results:")
                        for idx, playlist in enumerate(matching_playlists, start=1):
                            print(f"[{idx}] {playlist}")
                    else:
                        print(f"No playlists found matching '{search_query}'.")
                elif 1 <= choice <= len(playlists):  # Select a playlist
                    # Get the selected playlist name
                    selected_playlist = playlists[choice - 1]

                    # Display details of the selected playlist
                    display_playlist_details(data[selected_playlist])
                else:
                    print("Invalid option. Please try again.")

        elif choice == 3:
            name = input("Enter playlist name to delete: ")
            try:
                with open("Playlist.json", "r") as f:
                    data = json.load(f)
                if name in data:
                    del data[name]
                    with open("Playlist.json", "w") as f:
                        json.dump(data, f, indent=4)
                    print(f"Playlist '{name}' deleted successfully!")
                else:
                    print("Playlist not found.")
            except FileNotFoundError:
                print("No playlists available.")

        elif choice == 4:
            name = input("Enter playlist name: ")
            playlist = Playlist.load_playlist(name)
            if playlist:
                title = input("Enter track title to add: ")
                track = library.getTrack(title)
                if track:
                    playlist.add_track(track[0])  # Add the first match
                    print("Track added to playlist!")
                else:
                    print("Track not found in library.")
            else:
                print("Playlist not found.")

        elif choice == 5:
            name = input("Enter playlist name: ")
            playlist = Playlist.load_playlist(name)
            if playlist:
                title = input("Enter track title to remove: ")
                track = library.getTrack(title)
                if track:
                    playlist.remove_track(track[0])
                    print("Track removed from playlist!")
                else:
                    print("Track not found in playlist.")
            else:
                print("Playlist not found.")

        elif choice == 6:
            break
        else:
            print("Invalid option. Please try again.")

def manageQueue(queue, library):
    while True:
        showMenu("queue")
        choice = int(input("Select Operation: "))

        if choice == 1:
            title = input("Enter track title to add: ")
            track = library.getTrack(title)
            if track:
                queue.enqueue(track[0])
                print("Track added to queue!")
            else:
                print("Track not found in library.")

        elif choice == 2:
            name = input("Enter playlist name to add: ")
            playlist = Playlist.load_playlist(name)
            if playlist:
                queue.enqueue_playlist(playlist)
                print(f"Playlist '{name}' added to queue!")
            else:
                print("Playlist not found.")

        elif choice == 3:
            queue.shuffle_queue()
            print("Queue shuffled!")

        elif choice == 4:
            queue.toggle_repeat()
            print(f"Repeat {'enabled' if queue.is_repeat else 'disabled'}!")

        elif choice == 5:
            track = queue.next_track()
            if track:
                print(f"Now playing: {track}")
            else:
                print("End of queue.")

        elif choice == 6:
            track = queue.previous_track()
            if track:
                print(f"Now playing: {track}")
            else:
                print("Start of queue.")

        elif choice == 7:
            queue.display_queue()

        elif choice == 8:
            queue.save_queue()
            print("Queue saved. Exiting queue management.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    mainMenu()
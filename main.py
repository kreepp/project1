from MusicLibrary import MusicLibrary
from Playlist import Playlist
from queuesC import Queue
from Tracks import Tracks
import json


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
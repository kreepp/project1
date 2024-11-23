from MusicLibrary import MusicLibrary
from Playlist import Playlist
from queuesC import Queue
from Tracks import Tracks
import json


def receiveTrackInfo() -> Tracks:
    """Cast several prompts for user to input about the
    Tracks data.

    Returns:
       Track: Tracks object created based from data.
    """

    title = input("Enter track title: ")
    artist = input("Enter artist: ")
    album = input("Enter album: ")
    duration = input("Enter duration (mm:ss): ")
    additional_artists = input("Enter additional artist if there is any (Type and Enter None if there isn't any): ")
    if additional_artists == None or additional_artists == "":
        additional_artists = None
    return Tracks(title,artist,album,duration,additional_artists)

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
    print("\n<----- Menu ----->")
    for key, value in MENUS[menu_name].items():
        print(f"[{key}] {value}")


def mainMenu():
    library = MusicLibrary()
    queue = Queue()

    while True:
        showMenu("main")
        choice = int(input("Select Operation: "))
        
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
            try:
                with open("Playlist.json", "r") as f:
                    data = json.load(f)
                for name, details in data.items():
                    print(f"Playlist: {details['Playlist Name']}\nTotal Duration: {details['Total Duration']}\n")
            except FileNotFoundError:
                print("No playlists available.")

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
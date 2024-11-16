from music_library import MusicLibrary
from playlist_manager import PlaylistManager
from queue_manager import QueueManager

def main():
    library = MusicLibrary()
    playlist_manager = PlaylistManager(library)
    queue_manager = QueueManager(library, playlist_manager)

    while True:
        print("\nMain Menu:")
        print("[1] Manage Music Library")
        print("[2] Manage Playlists")
        print("[3] Play Queue")
        print("[4] Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            library.manage_library()
        elif choice == "2":
            playlist_manager.manage_playlists()
        elif choice == "3":
            queue_manager.manage_queue()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
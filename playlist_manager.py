class PlaylistManager:
    def __init__(self, storage, library):
        self.storage = storage
        self.library = library
        self.playlists = self.storage.load_playlists()

    def add_playlist(self):
        name = input("Enter playlist name: ")
        if any(pl["Name"] == name for pl in self.playlists):
            print("Playlist with this name already exists.")
            return

        tracks = []
        while True:
            track_title = input("Enter track title to add (or 'done' to finish): ")
            if track_title.lower() == "done":
                break
            track = self.library.search_track(track_title)
            if track:
                tracks.append(track[0])
            else:
                print("Track not found in library.")

        self.playlists.append({"Name": name, "Tracks": ", ".join([track["Title"] for track in tracks])})
        self.storage.save_playlists(self.playlists)
        print("Playlist created successfully.")

    def manage_playlists(self):
        while True:
            print("\nPlaylists:")
            print("[1] Add Playlist")
            print("[2] View Playlists")
            print("[3] Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_playlist()
            elif choice == "2":
                for playlist in self.playlists:
                    print(playlist)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

class MusicLibrary:
    def __init__(self, storage):
        self.storage = storage
        self.tracks = self.storage.load_music_library()

    def add_track(self):
        title = input("Enter track title: ")
        artist = input("Enter artist: ")
        album = input("Enter album: ")
        duration = input("Enter duration (mm:ss): ")
        self.tracks.append({"Title": title, "Artist": artist, "Album": album, "Duration": duration})
        self.storage.save_music_library(self.tracks)
        print("Track added successfully.")

    def search_track(self, title):
        return [track for track in self.tracks if track["Title"].lower() == title.lower()]

    def manage_library(self):
        while True:
            print("\nMusic Library:")
            print("[1] Add Track")
            print("[2] View Tracks")
            print("[3] Search Track")
            print("[4] Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_track()
            elif choice == "2":
                for track in self.tracks:
                    print(track)
            elif choice == "3":
                title = input("Enter track title to search: ")
                results = self.search_track(title)
                if results:
                    for track in results:
                        print(track)
                else:
                    print("No track found.")
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")

class QueueManager:
    def __init__(self, library, playlist_manager):
        self.library = library
        self.playlist_manager = playlist_manager
        self.queue = []

    def add_to_queue(self):
        track_title = input("Enter track title to add to queue: ")
        track = self.library.search_track(track_title)
        if track:
            self.queue.append(track[0])
            print("Track added to queue.")
        else:
            print("Track not found.")

    def manage_queue(self):
        while True:
            print("\nQueue:")
            print("[1] Add Track to Queue")
            print("[2] View Queue")
            print("[3] Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_to_queue()
            elif choice == "2":
                for track in self.queue:
                    print(track)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")
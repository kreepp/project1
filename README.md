# Project 1 Files

project1/
│
├── music_library.py      # Handles adding and searching tracks in the library
├── playlist_manager.py   # Manages playlists
├── queue_manager.py      # Manages playback queue
├── data_storage.py       # Handles data persistence to CSV
├── main.py               # Entry point of the program
├── storage/
│   ├── music_library.csv # Stores tracks
│   ├── playlists.csv     # Stores playlists
│   └── queue.csv         # Stores playback queue


other stuffs:
music_library.csv
    Columns: Title, Artist, Album, Duration
playlists.csv
    Columns: Name, Tracks (comma-separated)
queue.csv
    Columns: Title, Artist, Album, Duration

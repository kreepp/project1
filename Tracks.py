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

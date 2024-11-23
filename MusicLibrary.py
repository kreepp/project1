import json
from Tracks import Tracks

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
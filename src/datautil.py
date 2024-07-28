import heapq
import ast

class leaderboard():
    def __init__(self, file="") -> None:
        """
        File parameter is path to file with past data or where data will be saved.
        If not specified it will still run however without persistence of the data.
        """

        self.data = []
        self.score_finder = {}
        self.filename = file

        if file == "":
            self.counter = 0
            return
        
        with open(f".\\{file}", "a+") as f: 
            f.seek(0)
            file_data = f.readlines()
            if file_data == []:
                self.counter = 0
                return
            
            self.data = ast.literal_eval(file_data[0])
            self.counter = int(file_data[1])
            self.score_finder = ast.literal_eval(file_data[2])
            heapq.heapify(self.data)

        return
        
    def add_score(self, score: int, discordID: int) -> None:
        """
        Adds score and associated discordID to the datastore
        """
        # Only replace entry if higher score
        if discordID in self.score_finder:
            duplicate_entry = self.score_finder.pop(discordID)
            if duplicate_entry[0] < score:
                self.data.remove(duplicate_entry)
                heapq.heapify(self.data)
            else:
                self.score_finder[discordID] = duplicate_entry
                return

        count = self.counter
        self.counter -= 1
        entry = [score, count, discordID]
        self.score_finder[discordID] = entry
        heapq.heappush(self.data, entry)

        self._update_file()

        return
        
    def _update_file(self) -> None:
        """Saves the needed variables in a file, should not need to be manually called"""
        
        if self.filename == "":
            return
        with open(f".\\{self.filename}", "w", buffering=1) as f:
            f.write(str(self.data) + "\n")
            f.write(str(self.counter) + "\n")
            f.write(str(self.score_finder))

        return

    def top_scores(self, amount: int) -> list[tuple]:
        """Returns a list of tuple (score, discordID) of the top amount scores"""

        # Ensures amount is valid and there is data, and caps amount to amount of scores
        if (self.data == []) or (amount < 1):
            return None
        amount = len(self.data) if amount > len(self.data) else amount

        top = heapq.nlargest(amount, self.data)
        output = [(entry[0], entry[-1]) for entry in top] 

        return output
    
    def get_score(self, discordID: int) -> int:
        """
        Returns a list of the tuple of the discordID and score, otherwise raise KeyError if not found
        """
        
        if discordID not in self.score_finder:
            raise KeyError("DiscordID not found")
        
        output = self.score_finder[discordID][0]
        return output


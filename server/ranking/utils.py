import random

class RankingTournament:
    def __init__(self, entries):
        self.uid = random.randrange(1,pow(2,16-1))
        self.entries = { entry:0 for entry in entries}
        self.count = len(entries)
        self.expected_sum = int(self.count * ((self.count+1)/2))

    def get_candidates(self):
        return list(self.entries.keys())

    def cast_vote(self, votes):
        if len(votes) != self.count:
            return ({
                "status": "Error",
                "body": f"Expected {self.count} votes"
            })
        sum = 0
        visited = []
        for candidate in votes.keys():
            if candidate not in self.entries.keys():
                return ({
                    "status": "Error",
                    "body": f"{candidate} not a valid candidate"
                })
            if candidate in visited:
                return ({
                    "status": "Error",
                    "body": f"Found {candidate} multiple times"
                })
            visited.append(candidate)
            sum+=int(votes[candidate])
        if sum != self.expected_sum:
            return ({
                "status": "Error",
                "body": f"Expected {self.expected_sum} total value but got {sum}"
            })
        
        for candidate in votes.keys():
            self.entries[candidate] += int(votes[candidate])

        return ({
            "status": "Success",
            "body": "Votes cast",
            "votes": self.entries
        })

    def end(self):
        results = sorted(self.entries.items(), key=lambda x:x[1], reverse=True)
        return({
            "winner": results[0][0],
            "results": results
        })
        

active_rounds = {}

def new(entries):
    new = RankingTournament(entries)
    active_rounds[new.uid] = new
    print(new.entries)
    return new.uid

def vote(uid, votes):
    try:
        return active_rounds[uid].cast_vote(votes)
    except KeyError:
        return(f"uid {uid} not an ongoing vote")

def getCandidates(uid):
    try:
        return active_rounds[uid].get_candidates()
    except KeyError as e:
        print(e)
        return(f"uid {uid} not an ongoing vote")


def endVoting(uid):
    try:
        response = active_rounds[uid].end()
        active_rounds.pop(uid)
        return response
    except KeyError as e:
        print(e)
        return(f"uid {uid} not an ongoing vote")
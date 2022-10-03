
import random
from pprint import pprint

#Constants
CANDIDATES = 'CANDIDATES'
RESULTS = 'RESULTS'
MATCHUP = 'MATCHUP'
ROUND = 'ROUND'
CURRENT_MATCHES = 'CURRENT_MATCHES'

#TODO: Do I delete the data after a while?
#TODO: Check connectivity

class VoteUtils():
    
    def __init__(self, table) -> None:
        self.table = table

    
    def new_tournament(self, entries):
        #TODO: Ensure no duplicates in entries
        #TODO: Ensure no entries are reserved keywords like CURRENT_ROUND
        uid = random.randrange(1,pow(2,16-1)) #Create uniqueID

        response = self.table.put_item (
            Item = {
                'uid': uid,
                RESULTS: {ROUND: 1},
                CANDIDATES: entries,
                MATCHUP: {},
                CURRENT_MATCHES: []
            },
            ConditionExpression = "attribute_not_exists(uid)"
        )
        
        print(response)
        #TODO: Handle response appropriately 
        return uid


    def generate_matchups(self, uid):
        matchups = {}
        rounds = []
        #TODO: Do a try/except for connectivity error here
        candidates = self.table.get_item(Key={"uid":uid})['Item'][CANDIDATES]

        while len(candidates) > 1:
            a = random.choice(candidates)
            candidates.remove(a)
            b = random.choice(candidates)
            candidates.remove(b)
            match_name = f"{a}:{b}"
            
            
            matchups[match_name] = {a: 0, b:0}
            rounds.append(match_name)

        response = self.table.update_item(
            Key={'uid': uid},
            UpdateExpression=f"SET {MATCHUP} = :newMatchup, {CURRENT_MATCHES} = :newRounds",
            ExpressionAttributeValues={
                ':newMatchup': matchups,
                ':newRounds': rounds
            },
        )
        return matchups

    def get_current_round(self, uid):
        #TODO: Error handling for if there is no current round
        item = self.table.get_item(Key={"uid":int(uid)})['Item']
        ref = item[CURRENT_MATCHES][-1]
        current_round = item[MATCHUP][item[CURRENT_MATCHES][-1]]
        pprint(item)
        return (ref, current_round)

    def get_candidates(self, uid):
        return self.table.get_item(Key={"uid":int(uid)})['Item'][CANDIDATES]

    def get_results(self, uid):
        return self.table.get_item(Key={"uid":int(uid)})['Item'][RESULTS]

    def verify_vote(self, item: dict, ref: str, vote: str):
        #Need to do some checking here because its not moving through
        if not(ref == item[CURRENT_MATCHES][-1]): # Check if reference is active round
            return(False, 'Round not currently active.', item[CURRENT_MATCHES][-1])
        
        voting_options = item[MATCHUP][ref].keys()
        if not(vote in voting_options):
            return(False, 'Vote not a valid option in current round.', voting_options)

        return(True, "Valid vote")


    def submit_vote(self, uid: str, ref: str, vote: str):
        item = self.table.get_item(Key={"uid":int(uid)})['Item']
        
        valid = self.verify_vote(item, ref, vote)
        if not valid[0]:
            return(valid)


        response = self.table.update_item(
            Key={'uid': int(uid)},
            UpdateExpression=f"SET {MATCHUP}.#ref.#vote = :score",
            ExpressionAttributeValues={
                ':score': item[MATCHUP][ref][vote]+1
            },
            ExpressionAttributeNames={  
                '#ref': ref,
                '#vote': vote
            }, 
            ReturnValues='ALL_NEW'
        )
        return(True, {key: int(value) for key, value in response['Attributes'][MATCHUP][ref].items()})

    def end_round(self, uid: str, ref: str):
        item = self.table.get_item(Key={"uid":int(uid)})['Item']
        if not(ref == item[CURRENT_MATCHES][-1]): # Check if reference is active round
            return(False, 'Round not currently active.', item[CURRENT_MATCHES][-1])
        
        results = item[MATCHUP][ref]
        majority = 0
        winner = None

        for candidate in results.keys():
            if int(results[candidate]) > majority:
                majority = int(results[candidate])
                winner = candidate
            elif int(results[candidate]) == majority:
                winner = None

        candidates = item[CANDIDATES]
        overall_results = item[RESULTS]
        
        current_matches = item[CURRENT_MATCHES]
        matchup = item[MATCHUP]

        if(winner): #If not a tie
            results.pop(winner)
            #Get the loser
            loser = results.popitem()[0] 
            #Remove loser from candidates
            candidates.remove(loser)
            #Add loser result
            overall_results[loser] = item[RESULTS][ROUND]
    
        overall_win = False
        #Remove round from list
        current_matches.remove(ref)
        matchup.pop(ref)
        overall_results[ROUND] += 1

        if len(item[CURRENT_MATCHES])-1 == 0 and len(candidates) < 2:
            print("Winner found")
            overall_win = True
            overall_results['Winner'] = winner
        
        
        response = self.table.update_item(
            Key={'uid': int(uid)},
            UpdateExpression=f"SET {CANDIDATES} = :candidates, {MATCHUP} = :matchup, {RESULTS} = :results, {CURRENT_MATCHES} = :matches",
            ExpressionAttributeValues={
                ':matchup': matchup,
                ':results': overall_results,
                ':candidates': candidates,
                ':matches': current_matches

            },  
            ReturnValues='ALL_NEW'
        )

        pprint(response)
        if len(candidates) > 1 and len(item[CURRENT_MATCHES])-1 == 0:
            self.generate_matchups(int(uid))
        return (True, winner, overall_win)
        
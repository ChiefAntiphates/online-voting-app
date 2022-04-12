import random
from redis_utils import decode_redis

IN_USE = 'IDS_IN_USE'
#Field standard names
CURRENT_ROUND = 'CURRENT_ROUND'
CANDIDATES = 'candidates'
RESULTS = 'results'
MATCHUP = 'matchup'
MATCHUP_LOOKUP = 'matchup_lookup'


def new_tournament(r, entries):
    #TODO: Ensure no duplicates in entries
    #TODO: Ensure no entries are reserved keywords lik CURRENT_ROUND
    uid = random.randrange(1,pow(2,32-1)) #Create uniqueID
    while str(uid).encode() in r.smembers(IN_USE): #Check to see if uniqueID being used
        uid = random.randrange(1,pow(2,32-1)) #Regenerate if in use
    r.sadd(IN_USE, uid) #Register as being used
    

    r.hset(f"{RESULTS}:{uid}", CURRENT_ROUND, 1) #Init new results hash with current_round = 0
    for entry in entries:
        r.sadd(f"{CANDIDATES}:{uid}", entry) #Add all entries
        #r.hset(f"{RESULTS}:{uid}", entry, 0) #We only need to post result on loss

    return uid

def generate_matchups(r, uid):
    matchups = []
    candidates = [x.decode() for x in list(r.smembers(f"{CANDIDATES}:{uid}"))]
    while len(candidates) > 1:
        a = random.choice(candidates)
        candidates.remove(a)
        b = random.choice(candidates)
        candidates.remove(b)
        hash_name = f"{MATCHUP}:{uid}:{a}:{b}"
        r.hset(hash_name, a, 0)
        r.hset(hash_name, b, 0)
        r.rpush(f"{MATCHUP_LOOKUP}:{uid}", hash_name)
        matchups.append([a, b])
    return matchups

def get_current_round(r, uid):
    #TODO: Error handling for if there is no current round
    #if r.llen(f"{MATCHUP_LOOKUP}:{uid}") == 0:
    return r.lindex(f"{MATCHUP_LOOKUP}:{uid}", 0).decode()
    

def get_round_details(r, ref):
    return decode_redis(r.hgetall(ref))


def get_candidates(r, uid):
    return [x.decode() for x in list(r.smembers(f"{CANDIDATES}:{uid}"))]

def get_results(r, uid):
    return decode_redis(r.hgetall(f"{RESULTS}:{uid}"))

#TODO: Get whole bracket at current point

def verify_vote(r, uid: str, ref: str, vote: str):
    current_round = r.lindex(f"{MATCHUP_LOOKUP}:{uid}", 0).decode()

    if not(ref == current_round): # Check if reference is active round
        return(False, 'Round not currently active.', current_round)

    voting_options = r.hkeys(current_round)
    
    if not(vote.encode() in voting_options):
        return(False, 'Vote not a valid option in current round.', decode_redis(voting_options))

    return(True, "Valid vote")


def submit_vote(r, uid: str, ref: str, vote: str):
    valid = verify_vote(r, uid, ref, vote)
    if not valid[0]:
        return(valid)

    amount = r.hincrby(ref, vote, 1) #Cast vote
    return(True, f"Vote cast for {vote} which now has {amount} votes")

def end_round(r, uid: str, ref: str):
    current_round = get_current_round(r, uid)
    if not(current_round == ref):
        return (False, "Round not active", current_round) 
    
    results = get_round_details(r, ref)
    majority = 0
    winner = None
    for candidate in results.keys():
        if int(results[candidate]) > majority:
            majority = int(results[candidate])
            winner = candidate
        elif int(results[candidate]) == majority:
            winner = None
    
    if(winner): #If not a tie
        results.pop(winner)
        #Get the loser
        loser = results.popitem()[0] 
        #Remove loser from candidates
        r.srem(f"{CANDIDATES}:{uid}", loser) 
        #Add loser result
        r.hset(f"{RESULTS}:{uid}", loser, r.hget(f"{RESULTS}:{uid}", CURRENT_ROUND))
   
    #Remove round from list
    r.lpop(f"{MATCHUP_LOOKUP}:{uid}")
    if r.llen(f"{MATCHUP_LOOKUP}:{uid}") == 0:
        if len(list(r.smembers(f"{CANDIDATES}:{uid}"))) < 2:
            print("Winner found")
            #TODO: Move these bits into function...
            r.hset(f"{RESULTS}:{uid}", winner, 'Winner')
            r.srem(IN_USE, uid)
        else:
            generate_matchups(r, uid)
            r.hincrby(f"{RESULTS}:{uid}", CURRENT_ROUND, 1) #Increment round by 1
    return (True, f"{winner} wins with {majority} votes", results)
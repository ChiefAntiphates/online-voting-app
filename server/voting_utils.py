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
    return r.lindex(f"{MATCHUP_LOOKUP}:{uid}", 0).decode()
    

def get_round_details(r, ref):
    return decode_redis(r.hgetall(ref))


def verify_vote(r, uid: str, ref: str, vote: str):
    current_round = r.lindex(f"{MATCHUP_LOOKUP}:{uid}", 0).decode()

    if not(ref == current_round): # Check if reference is active round
        return(False, 'Round not currently active.', current_round)

    voting_options = r.hkeys(current_round)
    
    if not(vote.encode() in voting_options):
        return(False, 'Vote not a valid option in current round.', decode_redis(voting_options))

    return(True)


def submit_vote(r, uid: str, ref: str, vote: str):
    valid = verify_vote(r, uid, ref, vote)
    if not valid[0]:
        return(valid)

    print(r.hincrby(ref, vote, 1)) #Cast vote
    return(True, f"Vote cast for {vote}")
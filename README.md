# online-voting-app


# Voting Backend Logic
1. Check that uid not in use and register uid.
2. Create a candidates set of all the entries.
3. Create a results hash with current_round initialised to 0.
4. Randomly generate matchup pairs from the candidates set, save a hash for each pair 
and create a reference list to save the key of each matchup.
5. Take the leftmost matchup from the reference list and start taking votes.
6. Once voting is finished remove the entry with least votes from the candidates set and add it
to the results hash as a key with the current round as the value. Pop the round from the
reference list.
7. Repeat steps 5-6 until the reference list is empty, then increment the current_round value in the results hash by 1.
8. Repeat steps 4-7 until only one entry remains.
9. Drop all assets and remove uid from registry. 
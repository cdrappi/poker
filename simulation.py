import poker
import itertools
import csv
import time

num_players = 8
mc = 400
denom_of_frac = 1000
deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']


num_wins = {'flop': {}, 'turn': {}, 'river': {}}
num_appearances = {}
win_pct = {}
stages = ['flop', 'turn', 'river']

for hand in itertools.combinations(deck, 2):
	num_appearances[poker.pocket_in_words(hand)] = 0
	for stage in stages:
		num_wins[stage][poker.pocket_in_words(hand)] = 0

start = time.clock()
for i in range(mc):
	pockets, community = poker.holdem_deal(num_players)
	best_hands = {}
	winners = {}
	for stage in stages:
		# best_hands: {stages: {best_hands: pockets}}
		best_hands[stage] = {}
		# winners: {stages: [winners]}
		winners[stage] = []
	# decide best hand per each stage per each pocket
	for p in pockets:
		num_appearances[poker.pocket_in_words(p)] += 1
		for j, stage in enumerate(stages):
			# compute the current pool of cards
			hand_pool = p + community[0:(3+j)]
			# compute each player's best hand from hand_pool
			bh = max(itertools.combinations(hand_pool, 5), key=poker.hand_rank)
			best_hands[stage][poker.tuple_to_str(bh)] = poker.list_to_str(p)
	# decide which pocket wins
	for stage in stages:
		winners[stage] = poker.poker(poker.str_to_tuple(hand) for hand in best_hands[stage])
		for w in winners[stage]:
			pocket_won = poker.pocket_in_words(poker.str_to_list(best_hands[stage][poker.tuple_to_str(w)]))
			num_wins[stage][pocket_won] += 1.0/len(winners[stage])
	# we print our progress every so often (goverened by denom_of_frac)
	# if i % (mc/denom_of_frac) == 0 and i != 0:
	if i == (mc/denom_of_frac) or i == (mc/2):
		# using a distance = rate * time formula
		# since time is in minutes, we divide by 60
		delta_mins = (time.clock() - start)/60.0
		rate = float(i)/delta_mins
		mins_left = str(round(float(mc - i)/rate, 3))
		print("Estimated time to completion: " + mins_left + " min")

for hand in itertools.combinations(deck, 2):
	for stage in stages:
		win_pct[poker.pocket_in_words(hand)] = [0,0,0]
		if num_appearances[poker.pocket_in_words(hand)] > 0:
			for n, stage in enumerate(stages):
				win_pct[poker.pocket_in_words(hand)][n] = float(num_wins[stage][poker.pocket_in_words(hand)]) / num_appearances[poker.pocket_in_words(hand)]

sorted_win_pct = sorted(win_pct.items(), key=lambda x: x[1][2], reverse=True)
write_file = str(num_players) + "players_" + str(mc) + "samples.csv"
with open(write_file, 'w+') as f:
	writer = csv.writer(f)
	writer.writerow(["hand"]+stages)
	for hand, prob in sorted_win_pct:
		writer.writerow([hand, str(round(prob[0], 6)), str(round(prob[1], 6)), str(round(prob[2], 6))])




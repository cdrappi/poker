import poker
import itertools
import csv
import time

num_players = 4
mc = 20000000
denom_of_frac = 1000
deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

# for reading purposes
def pocket_in_words(pocket):
	ret = ""
	if pocket[0][0] == pocket[1][0]:
		ret = "Pair of " + card_to_words(pocket[0][0]) + "s"
	else:
		ranks = poker.card_ranks(pocket)
		ret = card_to_words(ranks[0]) + "-" + card_to_words(ranks[1])
		if pocket[0][1] == pocket[1][1]:
			ret += " suited"
		else:
			ret += " offsuit"
	return ret

def list_to_str(l):
	return " ".join(l)

def str_to_list(s):
	return s.split()

def card_to_words(card):
	if card == "A" or card == 14:
		return "Ace"
	elif card == "K" or card == 13:
		return "King"
	elif card == "Q" or card == 12:
		return "Queen"
	elif card == "J" or card == 11:
		return "Jack"
	elif card == "T" or card == 10:
		return "10"
	else:
		return str(card)

def tuple_to_str(t):
	return ' '.join(map(str,t))

def str_to_tuple(s):
	l = s.split()
	return tuple(l)


num_wins = {'flop': {}, 'turn': {}, 'river': {}}
num_appearances = {}
win_pct = {}
stages = ['flop', 'turn', 'river']

for hand in itertools.combinations(deck, 2):
	num_appearances[pocket_in_words(hand)] = 0
	for stage in stages:
		num_wins[stage][pocket_in_words(hand)] = 0

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
		num_appearances[pocket_in_words(p)] += 1
		for j, stage in enumerate(stages):
			# compute the current pool of cards
			hand_pool = p + community[0:(3+j)]
			# compute each player's best hand from hand_pool
			bh = max(itertools.combinations(hand_pool, 5), key=poker.hand_rank)
			best_hands[stage][tuple_to_str(bh)] = list_to_str(p)
	# decide which pocket wins
	for stage in stages:
		winners[stage] = poker.poker(str_to_tuple(hand) for hand in best_hands[stage])
		for w in winners[stage]:
			pocket_won = pocket_in_words(str_to_list(best_hands[stage][tuple_to_str(w)]))
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
		win_pct[pocket_in_words(hand)] = [0,0,0]
		if num_appearances[pocket_in_words(hand)] > 0:
			for n, stage in enumerate(stages):
				win_pct[pocket_in_words(hand)][n] = float(num_wins[stage][pocket_in_words(hand)]) / num_appearances[pocket_in_words(hand)]

sorted_win_pct = sorted(win_pct.items(), key=lambda x: x[1], reverse=True)
write_file = str(num_players) + "players_" + str(mc) + "samples.csv"
with open(write_file, 'w+') as f:
	writer = csv.writer(f)
	writer.writerow(["hand"]+stages)
	for hand, prob in sorted_win_pct:
		writer.writerow([hand, str(round(prob[0], 6)), str(round(prob[1], 6)), str(round(prob[2], 6))])




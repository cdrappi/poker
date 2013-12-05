import poker
import itertools
import csv
import time

deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

num_players = 5
sessions = 10000
hands_per_hour = 30
hours_per_session = 6
# hand_to_beat = ["9c", "8c", "7c", "6c", "Tc"]
hand_to_beat = ["9c", "9h", "9s", "As", "Ac"]


hothands_per_session = []
for s in range(sessions):
    hothand = []
    for i in range(hours_per_session):
        for h in range(hands_per_hour):
            hothands_hour = []
            pockets, community = poker.holdem_deal(num_players)
            tablehands = []
            for p in pockets:
                # compute each player's best hand from hand_pool
                playershands = [p+list(c) for c in itertools.combinations(community, 3)]
                playersbest = max(playershands, key=poker.hand_rank)
                tablehands.append(playersbest)
            tablebest = max(tablehands, key=poker.hand_rank)
            if poker.hand_rank(tablebest) > poker.hand_rank(hand_to_beat):
                hothands_hour.append(tablebest)
        hothand.append(hothands_hour)
    has_hothand = [0 if not h else 1 for h in hothand]
    num_hothands = sum(has_hothand)
    hothands_per_session.append(num_hothands)

with(open("hothands.csv", "w+")) as f:
    writer = csv.writer(f)
    for h in hothands_per_session:
        writer.writerow([h])
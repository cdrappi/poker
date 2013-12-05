import random
import csv

max_splits = 9
mc = 1000000 

cards_to_come = [1,2,5]
outs = list(range(0,21))
redraws = list(range(0,10))
play_ahead = [[[0 for r in redraws] for o in outs] for c in cards_to_come]
play_behind = [[[0 for r in redraws] for o in outs] for c in cards_to_come]

for c, n_cards in enumerate(cards_to_come):
    for o in outs:
        for r in redraws:
            equity = [None]*max_splits
            for i in range(max_splits):
                ahead_wins = 0
                for j in range(mc):
                    S = [1]*(o+1) + [2]*r + [0]*(43+n_cards-(r+o+1))
                    for run_count in range(i+1):
                        y = random.sample(S, n_cards)
                        for el in y:
                            S.remove(el)
                        if ((2 in y) or (1 not in y)):
                            ahead_wins += 1
                equity[i] = ahead_wins/(mc*(i+1))
            print(equity)
            ahead_runs = equity.index(max(equity))
            behind_runs = equity.index(min(equity))
            play_ahead[c][o][r] = ahead_runs+1
            play_behind[c][o][r] = behind_runs+1
    with open(str(n_cards)+"_to_come_ahead_max"+str(max_splits)+".csv", 'w+') as f:
        fw = csv.writer(f)
        fw.writerow(["outs/redraws"]+redraws)
        for o,o_list in enumerate(play_ahead[c]):
            fw.writerow([(o+1)] + play_ahead[c][o])
    with open(str(n_cards)+"_to_come_behind_max"+str(max_splits)+".csv", 'w+') as f:
        fw = csv.writer(f)
        fw.writerow(["outs/redraws"]+redraws)
        for o, o_list in enumerate(play_behind[c]):
            fw.writerow([(o+1)] + play_behind[c][o])
        